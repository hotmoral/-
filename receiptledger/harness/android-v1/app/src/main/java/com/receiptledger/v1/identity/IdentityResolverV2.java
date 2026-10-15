package com.receiptledger.v1.identity;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.CatalogKind;
import com.receiptledger.v1.catalog.ProductSpecification;
import com.receiptledger.v1.product.ProductNameNormalizer;
import com.receiptledger.v1.semantics.ReceiptProductSemantics;
import com.receiptledger.v1.semantics.SemanticCandidate;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/** Deterministic CP24 resolver. It resolves only to existing stable catalog IDs. */
public final class IdentityResolverV2 {

    public IdentityDecisionV2 resolve(
            String rawAlias,
            String merchantKey,
            ReceiptProductSemantics semantics,
            IdentityKnowledgeV2 knowledge) {
        if (knowledge == null) throw new IllegalArgumentException("knowledge");
        String raw = rawAlias == null ? "" : rawAlias.trim();
        if (raw.isEmpty()) return IdentityDecisionV2.unresolved("empty raw alias");

        String merchantId = null;
        AliasContext merchantContext = merchantContextOrNull(merchantKey);
        if (merchantContext != null) {
            merchantId = knowledge.exactAliasCatalogEntryId(merchantContext, raw);
            if (merchantId != null) {
                String global = knowledge.exactAliasCatalogEntryId(AliasContext.global(), raw);
                String extra = global != null && !global.equals(merchantId)
                        ? "; merchant-specific mapping overrides different GLOBAL mapping"
                        : "";
                return aliasDecision(merchantId, IdentityDecisionV2.Authority.MERCHANT_EXACT_ALIAS,
                        semantics, knowledge, "confirmed MERCHANT exact alias" + extra);
            }
        }

        String globalId = knowledge.exactAliasCatalogEntryId(AliasContext.global(), raw);
        if (globalId != null) {
            return aliasDecision(globalId, IdentityDecisionV2.Authority.GLOBAL_EXACT_ALIAS,
                    semantics, knowledge, "confirmed GLOBAL exact alias");
        }

        return semanticDecision(semantics, knowledge);
    }

    private IdentityDecisionV2 aliasDecision(
            String id,
            IdentityDecisionV2.Authority authority,
            ReceiptProductSemantics semantics,
            IdentityKnowledgeV2 knowledge,
            String reason) {
        CatalogEntryV2 entry = knowledge.catalogEntry(id);
        if (entry == null) {
            return IdentityDecisionV2.review(null, IdentityDecisionV2.Authority.ALIAS_CONFLICT,
                    Collections.<String>emptyList(), "confirmed alias points to missing catalog entry: " + id);
        }
        String contradiction = explicitAliasContradiction(semantics, entry);
        if (contradiction != null) {
            List<String> ids = new ArrayList<>();
            ids.add(entry.id);
            return IdentityDecisionV2.review(entry.id, IdentityDecisionV2.Authority.ALIAS_CONFLICT,
                    ids, "confirmed alias contradicted by current explicit evidence: " + contradiction);
        }
        return IdentityDecisionV2.autoLink(entry.id, authority, reason);
    }

    private IdentityDecisionV2 semanticDecision(ReceiptProductSemantics semantics, IdentityKnowledgeV2 knowledge) {
        if (semantics == null || semantics.productName == null) {
            return IdentityDecisionV2.unresolved("no semantic product-name evidence");
        }

        List<ScoredCandidate> ranked = new ArrayList<>();
        for (CatalogEntryV2 entry : safeEntries(knowledge.catalogEntries())) {
            ScoredCandidate scored = score(entry, semantics);
            if (scored != null) ranked.add(scored);
        }
        Collections.sort(ranked, new Comparator<ScoredCandidate>() {
            @Override public int compare(ScoredCandidate a, ScoredCandidate b) {
                if (a.score > b.score) return -1;
                if (a.score < b.score) return 1;
                return a.entry.id.compareTo(b.entry.id);
            }
        });

        List<ScoredCandidate> strict = new ArrayList<>();
        for (ScoredCandidate candidate : ranked) if (candidate.strictAutoEligible) strict.add(candidate);
        if (strict.size() == 1) {
            ScoredCandidate only = strict.get(0);
            return IdentityDecisionV2.autoLink(only.entry.id,
                    IdentityDecisionV2.Authority.STRICT_SEMANTIC_EXACT,
                    "unique exact confirmed productName/specification identity evidence");
        }
        if (strict.size() > 1) {
            return IdentityDecisionV2.review(null, IdentityDecisionV2.Authority.SEMANTIC_AMBIGUOUS,
                    ids(strict), "multiple stable IDs share the same strict confirmed semantics");
        }
        if (ranked.isEmpty()) {
            return IdentityDecisionV2.unresolved("no existing STANDARD catalog candidate matches confirmed productName");
        }

        int topScore = ranked.get(0).score;
        List<ScoredCandidate> top = new ArrayList<>();
        for (ScoredCandidate candidate : ranked) {
            if (candidate.score == topScore) top.add(candidate);
        }
        if (top.size() > 1) {
            return IdentityDecisionV2.review(null, IdentityDecisionV2.Authority.SEMANTIC_AMBIGUOUS,
                    ids(ranked), "semantic evidence leaves multiple equally ranked existing identities");
        }
        return IdentityDecisionV2.review(ranked.get(0).entry.id,
                IdentityDecisionV2.Authority.SEMANTIC_SUGGESTION, ids(ranked),
                "existing product suggested but automatic identity authority is incomplete");
    }

    private static ScoredCandidate score(CatalogEntryV2 entry, ReceiptProductSemantics semantics) {
        if (entry == null || entry.kind != CatalogKind.STANDARD_PRODUCT) return null;
        if (!entry.productName.isConfirmed()) return null;
        if (!sameText(entry.productName.value, semantics.productName.value)) return null;

        int score = 100;
        if (semanticConflicts(semantics.brand, entry.brand)) return null;
        if (semanticConflicts(semantics.variant, entry.variant)) return null;
        if (specConflicts(semantics.specification, entry.specification)) return null;

        if (semanticExactConfirmed(semantics.brand, entry.brand)) score += 20;
        if (semanticExactConfirmed(semantics.variant, entry.variant)) score += 15;
        if (specExactConfirmed(semantics.specification, entry.specification)) score += 40;

        boolean strict = !semantics.reviewRequired
                && !semantics.measureAmbiguous
                && specExactConfirmed(semantics.specification, entry.specification)
                && optionalIdentityFieldStrict(semantics.brand, entry.brand)
                && optionalIdentityFieldStrict(semantics.variant, entry.variant);
        return new ScoredCandidate(entry, score, strict);
    }

    private static String explicitAliasContradiction(ReceiptProductSemantics semantics, CatalogEntryV2 entry) {
        if (semantics == null || entry == null) return null;
        if (semanticConflicts(semantics.brand, entry.brand)) return "brand";
        if (semanticConflicts(semantics.variant, entry.variant)) return "variant";
        if (!semantics.measureAmbiguous && specConflicts(semantics.specification, entry.specification)) return "specification";
        return null;
    }

    private static boolean semanticConflicts(SemanticCandidate<String> semantic, CatalogField<String> catalog) {
        return semantic != null && catalog != null && catalog.isConfirmed()
                && !sameText(semantic.value, catalog.value);
    }

    private static boolean specConflicts(
            SemanticCandidate<ProductSpecification> semantic,
            CatalogField<ProductSpecification> catalog) {
        return semantic != null && catalog != null && catalog.isConfirmed()
                && !sameSpec(semantic.value, catalog.value);
    }

    private static boolean semanticExactConfirmed(SemanticCandidate<String> semantic, CatalogField<String> catalog) {
        return semantic != null && catalog != null && catalog.isConfirmed() && sameText(semantic.value, catalog.value);
    }

    private static boolean specExactConfirmed(
            SemanticCandidate<ProductSpecification> semantic,
            CatalogField<ProductSpecification> catalog) {
        return semantic != null && catalog != null && catalog.isConfirmed() && sameSpec(semantic.value, catalog.value);
    }

    private static boolean optionalIdentityFieldStrict(SemanticCandidate<String> semantic, CatalogField<String> catalog) {
        boolean semanticPresent = semantic != null;
        boolean catalogPresent = catalog != null && catalog.isPresent();
        if (!semanticPresent && !catalogPresent) return true;
        return semanticPresent && catalogPresent && catalog.isConfirmed() && sameText(semantic.value, catalog.value);
    }

    private static boolean sameText(String a, String b) {
        return ProductNameNormalizer.key(a).equals(ProductNameNormalizer.key(b));
    }

    private static boolean sameSpec(ProductSpecification a, ProductSpecification b) {
        return a != null && b != null && a.candidateToken().equals(b.candidateToken());
    }

    private static AliasContext merchantContextOrNull(String merchantKey) {
        if (ProductNameNormalizer.key(merchantKey).isEmpty()) return null;
        return AliasContext.merchant(merchantKey);
    }

    private static List<CatalogEntryV2> safeEntries(List<CatalogEntryV2> entries) {
        return entries == null ? Collections.<CatalogEntryV2>emptyList() : entries;
    }

    private static List<String> ids(List<ScoredCandidate> candidates) {
        List<String> out = new ArrayList<>();
        for (ScoredCandidate candidate : candidates) out.add(candidate.entry.id);
        return out;
    }

    private static final class ScoredCandidate {
        final CatalogEntryV2 entry;
        final int score;
        final boolean strictAutoEligible;
        ScoredCandidate(CatalogEntryV2 entry, int score, boolean strictAutoEligible) {
            this.entry = entry;
            this.score = score;
            this.strictAutoEligible = strictAutoEligible;
        }
    }
}
