package com.receiptledger.v1.commodity;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogKind;
import com.receiptledger.v1.identity.IdentityKnowledgeV2;
import com.receiptledger.v1.product.ProductNameNormalizer;
import com.receiptledger.v1.semantics.ReceiptProductSemantics;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/** Conservative CP26 resolver for grouping observations under an existing NON_STANDARD commodity ID. */
public final class CommodityResolverV2 {
    public CommodityGroupingDecisionV2 resolve(
            String rawAlias,
            String merchantKey,
            ReceiptProductSemantics semantics,
            IdentityKnowledgeV2 knowledge) {
        if (knowledge == null) throw new IllegalArgumentException("knowledge");
        String raw = rawAlias == null ? "" : rawAlias.trim();
        if (raw.isEmpty()) return CommodityGroupingDecisionV2.unresolved("empty raw alias");

        AliasContext merchant = merchantContextOrNull(merchantKey);
        if (merchant != null) {
            String id = knowledge.exactAliasCatalogEntryId(merchant, raw);
            if (id != null) {
                return aliasDecision(id, CommodityGroupingDecisionV2.Authority.MERCHANT_EXACT_ALIAS,
                        knowledge, "confirmed MERCHANT exact alias");
            }
        }

        String global = knowledge.exactAliasCatalogEntryId(AliasContext.global(), raw);
        if (global != null) {
            return aliasDecision(global, CommodityGroupingDecisionV2.Authority.GLOBAL_EXACT_ALIAS,
                    knowledge, "confirmed GLOBAL exact alias");
        }

        return semanticDecision(semantics, knowledge);
    }

    private CommodityGroupingDecisionV2 aliasDecision(
            String id,
            CommodityGroupingDecisionV2.Authority authority,
            IdentityKnowledgeV2 knowledge,
            String reason) {
        CatalogEntryV2 entry = knowledge.catalogEntry(id);
        if (entry == null) {
            return CommodityGroupingDecisionV2.review(null,
                    CommodityGroupingDecisionV2.Authority.CROSS_KIND_CONFLICT,
                    Collections.<String>emptyList(), "confirmed alias points to missing catalog entry: " + id);
        }
        if (entry.kind != CatalogKind.NON_STANDARD_COMMODITY) {
            List<String> ids = new ArrayList<>();
            ids.add(entry.id);
            return CommodityGroupingDecisionV2.review(entry.id,
                    CommodityGroupingDecisionV2.Authority.CROSS_KIND_CONFLICT,
                    ids, "confirmed alias targets a STANDARD product, not a commodity");
        }
        return CommodityGroupingDecisionV2.autoGroup(entry.id, authority, reason);
    }

    private CommodityGroupingDecisionV2 semanticDecision(
            ReceiptProductSemantics semantics, IdentityKnowledgeV2 knowledge) {
        if (semantics == null || semantics.productName == null) {
            return CommodityGroupingDecisionV2.unresolved("no semantic commodity-name evidence");
        }
        String semanticKey = ProductNameNormalizer.key(semantics.productName.value);
        if (semanticKey.isEmpty()) return CommodityGroupingDecisionV2.unresolved("empty semantic commodity name");

        List<CatalogEntryV2> commodities = commodityEntries(knowledge.catalogEntries());
        List<CatalogEntryV2> exact = new ArrayList<>();
        for (CatalogEntryV2 entry : commodities) {
            if (entry.canonicalKey.equals(semanticKey)) exact.add(entry);
        }
        if (exact.size() == 1) {
            CatalogEntryV2 only = exact.get(0);
            if (hasStrongStandardProductCue(semantics)) {
                return CommodityGroupingDecisionV2.review(only.id,
                        CommodityGroupingDecisionV2.Authority.COMMODITY_SUGGESTION,
                        ids(exact), "exact commodity name exists but current semantics contain STANDARD-product cues");
            }
            return CommodityGroupingDecisionV2.autoGroup(only.id,
                    CommodityGroupingDecisionV2.Authority.EXACT_COMMODITY_NAME,
                    "unique exact commodity canonical-name match; purchase form does not define identity");
        }
        if (exact.size() > 1) {
            return CommodityGroupingDecisionV2.review(null,
                    CommodityGroupingDecisionV2.Authority.COMMODITY_SUGGESTION,
                    ids(exact), "multiple commodity IDs share exact semantic name");
        }

        List<CatalogEntryV2> suggestions = new ArrayList<>();
        for (CatalogEntryV2 entry : commodities) {
            if (containsWholePhrase(semanticKey, entry.canonicalKey)) suggestions.add(entry);
        }
        if (suggestions.isEmpty()) {
            return CommodityGroupingDecisionV2.unresolved("no existing commodity exact or safe token suggestion");
        }
        return CommodityGroupingDecisionV2.review(
                suggestions.size() == 1 ? suggestions.get(0).id : null,
                CommodityGroupingDecisionV2.Authority.COMMODITY_SUGGESTION,
                ids(suggestions),
                "modifier-bearing commodity name requires confirmation; suggestion is not grouping authority");
    }

    private static boolean hasStrongStandardProductCue(ReceiptProductSemantics semantics) {
        if (semantics.brand != null || semantics.variant != null) return true;
        return semantics.specification != null && !semantics.measureAmbiguous;
    }

    private static AliasContext merchantContextOrNull(String merchantKey) {
        return ProductNameNormalizer.key(merchantKey).isEmpty() ? null : AliasContext.merchant(merchantKey);
    }

    private static List<CatalogEntryV2> commodityEntries(List<CatalogEntryV2> entries) {
        List<CatalogEntryV2> out = new ArrayList<>();
        if (entries != null) for (CatalogEntryV2 entry : entries) {
            if (entry != null && entry.kind == CatalogKind.NON_STANDARD_COMMODITY) out.add(entry);
        }
        Collections.sort(out, new Comparator<CatalogEntryV2>() {
            @Override public int compare(CatalogEntryV2 a, CatalogEntryV2 b) {
                return a.id.compareTo(b.id);
            }
        });
        return out;
    }

    private static boolean containsWholePhrase(String textKey, String phraseKey) {
        if (textKey.equals(phraseKey)) return true;
        String paddedText = " " + textKey + " ";
        String paddedPhrase = " " + phraseKey + " ";
        return paddedText.contains(paddedPhrase);
    }

    private static List<String> ids(List<CatalogEntryV2> entries) {
        List<String> out = new ArrayList<>();
        for (CatalogEntryV2 entry : entries) out.add(entry.id);
        return out;
    }
}
