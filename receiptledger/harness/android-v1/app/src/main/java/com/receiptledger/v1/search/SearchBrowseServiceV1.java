package com.receiptledger.v1.search;

import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.CategoryRef;
import com.receiptledger.v1.catalog.PackageMeasure;
import com.receiptledger.v1.catalog.ProductSpecification;
import com.receiptledger.v1.catalog.SalesUnitCode;
import com.receiptledger.v1.category.CategoryNodeV1;
import com.receiptledger.v1.category.CategoryTaxonomyV1;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.persistence.ReceiptStore;
import com.receiptledger.v1.persistence.SqliteReceiptStore;
import com.receiptledger.v1.priceeval.PriceEvaluationServiceV1;
import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.priceintel.PriceCohortV2;
import com.receiptledger.v1.priceintel.PriceIntelligenceServiceV2;
import com.receiptledger.v1.priceintel.PriceIntelligenceV2;
import com.receiptledger.v1.priceintel.PriceObservationV2;
import com.receiptledger.v1.product.CatalogProduct;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.ItemLinkRef;
import com.receiptledger.v1.product.ProductCatalogStore;
import com.receiptledger.v1.product.ProductNameNormalizer;
import com.receiptledger.v1.product.ProductType;
import com.receiptledger.v1.product.SqliteProductCatalogStore;
import java.math.BigDecimal;
import java.math.MathContext;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

/**
 * Read-only CP29 discovery service. Search relevance is intentionally incapable of mutating identity.
 */
public final class SearchBrowseServiceV1 {
    private final ReceiptStore receipts;
    private final ProductCatalogStore catalog;
    private final CatalogV2PersistenceStore v2Store;
    private final PriceIntelligenceServiceV2 priceIntelligence;
    private final PriceEvaluationServiceV1 priceEvaluation;

    public SearchBrowseServiceV1(
            ReceiptStore receipts,
            ProductCatalogStore catalog,
            CatalogV2PersistenceStore v2Store,
            PriceIntelligenceServiceV2 priceIntelligence,
            PriceEvaluationServiceV1 priceEvaluation) {
        if (receipts == null || catalog == null || v2Store == null || priceIntelligence == null || priceEvaluation == null) {
            throw new IllegalArgumentException("stores/services");
        }
        this.receipts = receipts;
        this.catalog = catalog;
        this.v2Store = v2Store;
        this.priceIntelligence = priceIntelligence;
        this.priceEvaluation = priceEvaluation;
    }

    public SearchBrowseResultV1 search(SearchBrowseQueryV1 query) {
        SearchBrowseQueryV1 q = query == null ? SearchBrowseQueryV1.all(50) : query;
        if (q.hasCategory()) CategoryTaxonomyV1.require(q.categoryId);

        List<BuiltEntry> docs = buildEntries();
        List<SearchBrowseEntryV1> matches = new ArrayList<>();
        String normalizedQuery = key(q.text);
        String compactQuery = compactNormalized(normalizedQuery);
        List<String> queryTokens = tokens(normalizedQuery);

        for (BuiltEntry doc : docs) {
            if (q.productType != null && doc.entry.type != q.productType) continue;
            if (q.hasCategory() && !categoryIncludes(q.categoryId, doc.entry.categoryId)) continue;
            if (q.hasStore() && !containsExactNormalized(doc.entry.stores, q.storeName)) continue;

            if (!q.hasText()) {
                matches.add(doc.entry.withMatch(0, "BROWSE"));
                continue;
            }
            Match match = match(doc, normalizedQuery, compactQuery, queryTokens);
            if (match != null) matches.add(doc.entry.withMatch(match.score, match.reason));
        }

        final boolean hasText = q.hasText();
        Collections.sort(matches, new Comparator<SearchBrowseEntryV1>() {
            @Override public int compare(SearchBrowseEntryV1 a, SearchBrowseEntryV1 b) {
                if (hasText) {
                    int c = Integer.compare(b.relevanceScore, a.relevanceScore);
                    if (c != 0) return c;
                }
                int c = compareEntryRecency(a, b);
                if (c != 0) return c;
                c = Integer.compare(b.purchaseCount, a.purchaseCount);
                if (c != 0) return c;
                c = safe(a.canonicalName).compareToIgnoreCase(safe(b.canonicalName));
                if (c != 0) return c;
                return safe(a.productId).compareTo(safe(b.productId));
            }
        });

        int totalMatches = matches.size();
        List<SearchBrowseEntryV1> limited = limit(matches, q.limit);
        return new SearchBrowseResultV1(normalizedQuery, docs.size(), totalMatches, limited);
    }

    public List<SearchBrowseEntryV1> recent(int limit) {
        requireLimit(limit);
        List<SearchBrowseEntryV1> out = new ArrayList<>();
        for (BuiltEntry doc : buildEntries()) if (doc.entry.purchaseCount > 0) out.add(doc.entry.withMatch(0, "RECENT"));
        Collections.sort(out, new Comparator<SearchBrowseEntryV1>() {
            @Override public int compare(SearchBrowseEntryV1 a, SearchBrowseEntryV1 b) {
                int c = compareEntryRecency(a, b);
                if (c != 0) return c;
                c = Integer.compare(b.purchaseCount, a.purchaseCount);
                if (c != 0) return c;
                c = safe(a.canonicalName).compareToIgnoreCase(safe(b.canonicalName));
                return c != 0 ? c : safe(a.productId).compareTo(safe(b.productId));
            }
        });
        return immutableLimit(out, limit);
    }

    public List<SearchBrowseEntryV1> frequent(int limit) {
        requireLimit(limit);
        List<SearchBrowseEntryV1> out = new ArrayList<>();
        for (BuiltEntry doc : buildEntries()) if (doc.entry.purchaseCount > 0) out.add(doc.entry.withMatch(0, "FREQUENT"));
        Collections.sort(out, new Comparator<SearchBrowseEntryV1>() {
            @Override public int compare(SearchBrowseEntryV1 a, SearchBrowseEntryV1 b) {
                int c = Integer.compare(b.purchaseCount, a.purchaseCount);
                if (c != 0) return c;
                c = compareEntryRecency(a, b);
                if (c != 0) return c;
                c = safe(a.canonicalName).compareToIgnoreCase(safe(b.canonicalName));
                return c != 0 ? c : safe(a.productId).compareTo(safe(b.productId));
            }
        });
        return immutableLimit(out, limit);
    }

    public List<SearchBrowseEntryV1> byCategory(String categoryId, int limit) {
        requireLimit(limit);
        CategoryTaxonomyV1.require(categoryId);
        return search(new SearchBrowseQueryV1(null, categoryId, null, null, limit)).entries;
    }

    public List<PriceChangeBrowseRowV1> priceChanges(int limit) {
        requireLimit(limit);
        List<PriceChangeBrowseRowV1> out = new ArrayList<>();
        for (CatalogProduct product : catalog.listProducts()) {
            if (product == null || product.type == ProductType.UNCLASSIFIED) continue;
            PriceIntelligenceV2 intelligence = priceIntelligence.analyze(product.id);
            for (PriceCohortV2 cohort : intelligence.cohorts) {
                PriceEvaluationV1 evaluation = priceEvaluation.evaluate(cohort);
                if (evaluation.status != PriceEvaluationV1.Status.EVALUATED) continue;
                if (evaluation.judgment == PriceEvaluationV1.Judgment.NONE
                        || evaluation.judgment == PriceEvaluationV1.Judgment.TYPICAL) continue;
                if (cohort.observations.isEmpty()) continue;
                PriceObservationV2 latest = cohort.observations.get(0);
                out.add(new PriceChangeBrowseRowV1(
                        product.id,
                        product.type,
                        product.canonicalName,
                        cohort.basis.key(),
                        cohort.basis.displayUnit,
                        evaluation.judgment,
                        evaluation.latestPriceMinor,
                        evaluation.usualPriceMinor,
                        evaluation.deltaFromUsualMinor,
                        evaluation.deltaFromUsualPercent,
                        latest.purchaseDate,
                        latest.storeName,
                        cohort.count()));
            }
        }
        Collections.sort(out, PRICE_CHANGE_ORDER);
        return immutableLimit(out, limit);
    }

    private List<BuiltEntry> buildEntries() {
        if (receipts instanceof SqliteReceiptStore
                && catalog instanceof SqliteProductCatalogStore
                && v2Store == catalog) {
            SqliteSearchBrowseSnapshotV1.Snapshot snapshot = SqliteSearchBrowseSnapshotV1.load(
                    (SqliteReceiptStore) receipts,
                    (SqliteProductCatalogStore) catalog);
            List<BuiltEntry> out = new ArrayList<>();
            for (SqliteSearchBrowseSnapshotV1.ProductRow row : snapshot.products) {
                out.add(buildEntry(row));
            }
            return out;
        }

        List<BuiltEntry> out = new ArrayList<>();
        for (CatalogProduct product : catalog.listProducts()) {
            if (product == null || product.type == ProductType.UNCLASSIFIED) continue;
            out.add(buildEntry(product));
        }
        return out;
    }

    private BuiltEntry buildEntry(SqliteSearchBrowseSnapshotV1.ProductRow row) {
        String categoryPath = categoryPath(row.categoryId);
        LinkedHashSet<String> observed = new LinkedHashSet<>();
        LinkedHashSet<String> stores = new LinkedHashSet<>();
        Set<String> receiptIds = new HashSet<>();
        SqliteSearchBrowseSnapshotV1.PurchaseRow latest = null;

        for (SqliteSearchBrowseSnapshotV1.PurchaseRow purchase : row.purchases) {
            receiptIds.add(purchase.receiptId);
            if (!clean(purchase.itemName).isEmpty()) observed.add(purchase.itemName.trim());
            if (!clean(purchase.storeName).isEmpty()) stores.add(purchase.storeName.trim());
            if (latest == null || isPurchaseNewer(purchase, latest)) latest = purchase;
        }

        List<String> observedList = sortedText(observed);
        List<String> storeList = sortedText(stores);
        String specSummary = specificationSummary(row.specification);

        SearchBrowseEntryV1 entry = new SearchBrowseEntryV1(
                row.product.id,
                row.product.type,
                row.product.canonicalName,
                row.brand,
                row.productName,
                row.variant,
                specSummary,
                row.categoryId,
                categoryPath,
                observedList,
                storeList,
                receiptIds.size(),
                latest == null ? null : cleanToNull(latest.purchaseDate),
                latest == null ? null : cleanToNull(latest.storeName),
                latest == null ? 0L : latest.createdAtMillis,
                0,
                "BROWSE");

        List<FieldValue> fields = new ArrayList<>();
        add(fields, FieldKind.CANONICAL, row.product.canonicalName);
        add(fields, FieldKind.STRUCTURED, row.brand);
        add(fields, FieldKind.STRUCTURED, row.productName);
        add(fields, FieldKind.STRUCTURED, row.variant);
        for (String term : specificationTerms(row.specification)) add(fields, FieldKind.STRUCTURED, term);
        for (String term : observedList) add(fields, FieldKind.OBSERVED, term);
        if (row.categoryId != null) add(fields, FieldKind.CATEGORY, row.categoryId);
        if (categoryPath != null) add(fields, FieldKind.CATEGORY, categoryPath);
        for (String label : categoryLabels(row.categoryId)) add(fields, FieldKind.CATEGORY, label);
        for (String store : storeList) add(fields, FieldKind.STORE, store);
        return new BuiltEntry(entry, fields);
    }

    private BuiltEntry buildEntry(CatalogProduct product) {
        CatalogEntryV2 v2 = v2Store.catalogEntryV2(product.id);
        String brand = value(v2 == null ? null : v2.brand);
        String productName = value(v2 == null ? null : v2.productName);
        String variant = value(v2 == null ? null : v2.variant);
        ProductSpecification specification = valueSpec(v2 == null ? null : v2.specification);
        CategoryRef category = v2 == null ? null : v2.category;
        String categoryId = category == null ? null : category.id;
        String categoryPath = categoryPath(categoryId);

        LinkedHashSet<String> observed = new LinkedHashSet<>();
        LinkedHashSet<String> stores = new LinkedHashSet<>();
        Set<String> receiptIds = new HashSet<>();
        ReceiptRecord latestReceipt = null;

        for (ItemLinkRef link : catalog.linksForProduct(product.id)) {
            ReceiptRecord receipt = receipts.get(link.receiptId);
            if (receipt == null) continue;
            receiptIds.add(receipt.id);
            PersistedItem item = find(receipt.items, link.itemOrdinal);
            if (item != null && !clean(item.name).isEmpty()) observed.add(item.name.trim());
            if (!clean(receipt.storeName).isEmpty()) stores.add(receipt.storeName.trim());
            if (latestReceipt == null || isReceiptNewer(receipt, latestReceipt)) latestReceipt = receipt;
        }

        List<String> observedList = sortedText(observed);
        List<String> storeList = sortedText(stores);
        String specSummary = specificationSummary(specification);

        SearchBrowseEntryV1 entry = new SearchBrowseEntryV1(
                product.id,
                product.type,
                product.canonicalName,
                brand,
                productName,
                variant,
                specSummary,
                categoryId,
                categoryPath,
                observedList,
                storeList,
                receiptIds.size(),
                latestReceipt == null ? null : cleanToNull(latestReceipt.purchaseDate),
                latestReceipt == null ? null : cleanToNull(latestReceipt.storeName),
                latestReceipt == null ? 0L : latestReceipt.createdAtMillis,
                0,
                "BROWSE");

        List<FieldValue> fields = new ArrayList<>();
        add(fields, FieldKind.CANONICAL, product.canonicalName);
        add(fields, FieldKind.STRUCTURED, brand);
        add(fields, FieldKind.STRUCTURED, productName);
        add(fields, FieldKind.STRUCTURED, variant);
        for (String term : specificationTerms(specification)) add(fields, FieldKind.STRUCTURED, term);
        for (String term : observedList) add(fields, FieldKind.OBSERVED, term);
        if (categoryId != null) add(fields, FieldKind.CATEGORY, categoryId);
        if (categoryPath != null) add(fields, FieldKind.CATEGORY, categoryPath);
        for (String label : categoryLabels(categoryId)) add(fields, FieldKind.CATEGORY, label);
        for (String store : storeList) add(fields, FieldKind.STORE, store);
        return new BuiltEntry(entry, fields);
    }

    private Match match(BuiltEntry doc, String q, String qc, List<String> queryTokens) {
        if (q.isEmpty()) return new Match(0, "BROWSE");
        int bestScore = -1;
        String bestReason = null;

        for (FieldValue field : doc.fields) {
            String fk = key(field.text);
            String fc = compactNormalized(fk);
            if (fk.isEmpty()) continue;
            boolean exact = fk.equals(q) || (!qc.isEmpty() && fc.equals(qc));
            boolean prefix = !exact && (fk.startsWith(q) || (!qc.isEmpty() && fc.startsWith(qc)));
            boolean contains = !exact && !prefix && (fk.contains(q) || (!qc.isEmpty() && fc.contains(qc)));
            int score = exact ? exactScore(field.kind) : prefix ? prefixScore(field.kind) : contains ? containsScore(field.kind) : -1;
            if (score > bestScore) {
                bestScore = score;
                bestReason = reason(field.kind, exact ? "EXACT" : prefix ? "PREFIX" : "CONTAINS");
            }
        }

        if (queryTokens.size() > 1) {
            String productAggregate = aggregate(doc.fields, false);
            if (allContained(productAggregate, queryTokens) && 6500 > bestScore) {
                bestScore = 6500;
                bestReason = "PRODUCT_ALL_TERMS";
            }
            String allAggregate = aggregate(doc.fields, true);
            if (allContained(allAggregate, queryTokens) && 5000 > bestScore) {
                bestScore = 5000;
                bestReason = "ALL_TERMS";
            }
        }

        return bestScore < 0 ? null : new Match(bestScore, bestReason);
    }

    private static int exactScore(FieldKind kind) {
        switch (kind) {
            case CANONICAL: return 10000;
            case STRUCTURED: return 9500;
            case OBSERVED: return 9000;
            case CATEGORY: return 6200;
            case STORE: return 5600;
            default: return 0;
        }
    }

    private static int prefixScore(FieldKind kind) {
        switch (kind) {
            case CANONICAL: return 8500;
            case STRUCTURED: return 8200;
            case OBSERVED: return 7800;
            case CATEGORY: return 6000;
            case STORE: return 5400;
            default: return 0;
        }
    }

    private static int containsScore(FieldKind kind) {
        switch (kind) {
            case CANONICAL: return 7400;
            case STRUCTURED: return 7100;
            case OBSERVED: return 6800;
            case CATEGORY: return 5800;
            case STORE: return 5200;
            default: return 0;
        }
    }

    private static String reason(FieldKind kind, String mode) {
        return kind.name() + "_" + mode;
    }

    private static boolean categoryIncludes(String selectedId, String assignedId) {
        if (selectedId == null) return true;
        if (assignedId == null) return false;
        String current = assignedId;
        while (current != null) {
            if (selectedId.equals(current)) return true;
            CategoryNodeV1 node;
            try {
                node = CategoryTaxonomyV1.require(current);
            } catch (IllegalArgumentException e) {
                return false;
            }
            current = node.parentId;
        }
        return false;
    }

    private static String categoryPath(String categoryId) {
        if (categoryId == null) return null;
        List<String> labels = categoryLabels(categoryId);
        if (labels.isEmpty()) return categoryId;
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < labels.size(); i++) {
            if (i > 0) out.append(" > ");
            out.append(labels.get(i));
        }
        return out.toString();
    }

    private static List<String> categoryLabels(String categoryId) {
        if (categoryId == null) return Collections.emptyList();
        List<String> labels = new ArrayList<>();
        String current = categoryId;
        while (current != null) {
            CategoryNodeV1 node;
            try {
                node = CategoryTaxonomyV1.require(current);
            } catch (IllegalArgumentException e) {
                labels.clear();
                labels.add(categoryId);
                return labels;
            }
            labels.add(node.displayNameKo);
            current = node.parentId;
        }
        Collections.reverse(labels);
        return labels;
    }

    private static List<String> specificationTerms(ProductSpecification specification) {
        if (specification == null) return Collections.emptyList();
        LinkedHashSet<String> out = new LinkedHashSet<>();
        addMeasureTerms(out, specification.netContent);
        if (specification.packCount != null) {
            int n = specification.packCount;
            out.add(n + "입");
            out.add(n + "개입");
            out.add(n + "PACK");
        }
        if (specification.innerUnitContent != null) {
            List<String> inner = measureTerms(specification.innerUnitContent);
            out.addAll(inner);
            if (specification.packCount != null) {
                for (String term : inner) {
                    out.add(term + "X" + specification.packCount);
                    out.add(specification.packCount + "X" + term);
                }
            }
        }
        out.add(specification.candidateToken());
        return new ArrayList<>(out);
    }

    private static String specificationSummary(ProductSpecification specification) {
        if (specification == null) return null;
        StringBuilder out = new StringBuilder();
        if (specification.netContent != null) out.append(primaryMeasureTerm(specification.netContent));
        if (specification.packCount != null) {
            if (out.length() > 0) out.append(" · ");
            out.append(specification.packCount).append("입");
        }
        if (specification.innerUnitContent != null) {
            if (out.length() > 0) out.append(" · ");
            out.append(primaryMeasureTerm(specification.innerUnitContent));
            if (specification.packCount != null) out.append("×").append(specification.packCount);
        }
        return out.length() == 0 ? null : out.toString();
    }

    private static void addMeasureTerms(Set<String> out, PackageMeasure measure) {
        out.addAll(measureTerms(measure));
    }

    private static List<String> measureTerms(PackageMeasure measure) {
        if (measure == null) return Collections.emptyList();
        LinkedHashSet<String> out = new LinkedHashSet<>();
        String symbol = unitSymbol(measure.unit);
        out.add(measure.amount.toPlainString() + symbol);
        out.add(measure.amount.toPlainString() + " " + symbol);
        BigDecimal base = measure.baseAmount();
        if (measure.unit.dimension == SalesUnitCode.Dimension.WEIGHT) {
            out.add(base.toPlainString() + "G");
            if (isWholeThousand(base)) out.add(base.divide(new BigDecimal("1000"), MathContext.DECIMAL128).stripTrailingZeros().toPlainString() + "KG");
        } else if (measure.unit.dimension == SalesUnitCode.Dimension.VOLUME) {
            out.add(base.toPlainString() + "ML");
            if (isWholeThousand(base)) out.add(base.divide(new BigDecimal("1000"), MathContext.DECIMAL128).stripTrailingZeros().toPlainString() + "L");
        } else if (measure.unit.dimension == SalesUnitCode.Dimension.COUNT) {
            out.add(base.toPlainString() + "개");
            out.add(base.toPlainString() + "입");
        }
        return new ArrayList<>(out);
    }

    private static String primaryMeasureTerm(PackageMeasure measure) {
        return measure.amount.toPlainString() + unitSymbol(measure.unit);
    }

    private static String unitSymbol(SalesUnitCode unit) {
        if (unit == null) return "";
        switch (unit) {
            case EACH: return "개";
            case GRAM: return "g";
            case KILOGRAM: return "kg";
            case MILLILITER: return "ml";
            case LITER: return "L";
            default: return unit.name();
        }
    }

    private static boolean isWholeThousand(BigDecimal value) {
        return value != null && value.remainder(new BigDecimal("1000")).compareTo(BigDecimal.ZERO) == 0;
    }

    private static String aggregate(List<FieldValue> fields, boolean includeContext) {
        StringBuilder out = new StringBuilder();
        for (FieldValue field : fields) {
            if (!includeContext && (field.kind == FieldKind.CATEGORY || field.kind == FieldKind.STORE)) continue;
            String value = compact(field.text);
            if (!value.isEmpty()) out.append('|').append(value);
        }
        return out.toString();
    }

    private static boolean allContained(String aggregate, List<String> tokens) {
        if (aggregate == null || aggregate.isEmpty()) return false;
        for (String token : tokens) if (!aggregate.contains(compactNormalized(token))) return false;
        return true;
    }

    private static List<String> tokens(String normalized) {
        if (normalized == null || normalized.isEmpty()) return Collections.emptyList();
        List<String> out = new ArrayList<>();
        for (String token : normalized.split(" ")) {
            String clean = token.trim();
            if (!clean.isEmpty()) out.add(clean);
        }
        return out;
    }

    private static boolean containsExactNormalized(List<String> values, String target) {
        String wanted = key(target);
        for (String value : values) if (key(value).equals(wanted)) return true;
        return false;
    }

    private static int compareEntryRecency(SearchBrowseEntryV1 a, SearchBrowseEntryV1 b) {
        String ad = cleanToNull(a.latestPurchaseDate);
        String bd = cleanToNull(b.latestPurchaseDate);
        if (ad != null && bd != null) {
            int c = bd.compareTo(ad);
            if (c != 0) return c;
        }
        int c = Long.compare(b.latestCreatedAtMillis, a.latestCreatedAtMillis);
        if (c != 0) return c;
        if (ad != null && bd == null) return -1;
        if (ad == null && bd != null) return 1;
        return 0;
    }

    private static boolean isPurchaseNewer(
            SqliteSearchBrowseSnapshotV1.PurchaseRow a,
            SqliteSearchBrowseSnapshotV1.PurchaseRow b) {
        String ad = cleanToNull(a.purchaseDate);
        String bd = cleanToNull(b.purchaseDate);
        if (ad != null && bd != null) {
            int c = ad.compareTo(bd);
            if (c != 0) return c > 0;
        }
        int c = Long.compare(a.createdAtMillis, b.createdAtMillis);
        if (c != 0) return c > 0;
        if (ad != null && bd == null) return true;
        if (ad == null && bd != null) return false;
        return safe(a.receiptId).compareTo(safe(b.receiptId)) > 0;
    }

    private static boolean isReceiptNewer(ReceiptRecord a, ReceiptRecord b) {
        String ad = cleanToNull(a.purchaseDate);
        String bd = cleanToNull(b.purchaseDate);
        if (ad != null && bd != null) {
            int c = ad.compareTo(bd);
            if (c != 0) return c > 0;
        }
        int c = Long.compare(a.createdAtMillis, b.createdAtMillis);
        if (c != 0) return c > 0;
        if (ad != null && bd == null) return true;
        if (ad == null && bd != null) return false;
        return safe(a.id).compareTo(safe(b.id)) > 0;
    }

    private static PersistedItem find(List<PersistedItem> items, int ordinal) {
        if (items == null) return null;
        for (PersistedItem item : items) if (item != null && item.ordinal == ordinal) return item;
        return null;
    }

    private static String value(CatalogField<String> field) {
        return field != null && field.isPresent() ? field.value : null;
    }

    private static ProductSpecification valueSpec(CatalogField<ProductSpecification> field) {
        return field != null && field.isPresent() ? field.value : null;
    }

    private static List<String> sortedText(Set<String> values) {
        List<String> out = new ArrayList<>(values);
        Collections.sort(out, new Comparator<String>() {
            @Override public int compare(String a, String b) {
                int c = key(a).compareTo(key(b));
                return c != 0 ? c : safe(a).compareTo(safe(b));
            }
        });
        return out;
    }

    private static List<SearchBrowseEntryV1> limit(List<SearchBrowseEntryV1> values, int limit) {
        if (values.size() <= limit) return new ArrayList<>(values);
        return new ArrayList<>(values.subList(0, limit));
    }

    private static <T> List<T> immutableLimit(List<T> values, int limit) {
        List<T> out = values.size() <= limit ? new ArrayList<>(values) : new ArrayList<>(values.subList(0, limit));
        return Collections.unmodifiableList(out);
    }

    private static void requireLimit(int limit) {
        if (limit < 1 || limit > 100) throw new IllegalArgumentException("limit must be 1..100");
    }

    private static String key(String value) { return ProductNameNormalizer.key(value); }
    private static String compact(String value) { return compactNormalized(key(value)); }
    private static String compactNormalized(String normalized) { return normalized == null ? "" : normalized.replace(" ", ""); }
    private static String clean(String value) { return value == null ? "" : value.trim(); }
    private static String cleanToNull(String value) { String v = clean(value); return v.isEmpty() ? null : v; }
    private static String safe(String value) { return value == null ? "" : value; }

    private static void add(List<FieldValue> fields, FieldKind kind, String text) {
        if (!clean(text).isEmpty()) fields.add(new FieldValue(kind, text));
    }

    private static final Comparator<PriceChangeBrowseRowV1> PRICE_CHANGE_ORDER = new Comparator<PriceChangeBrowseRowV1>() {
        @Override public int compare(PriceChangeBrowseRowV1 a, PriceChangeBrowseRowV1 b) {
            BigDecimal ap = a.deltaFromUsualPercent == null ? BigDecimal.ZERO : a.deltaFromUsualPercent.abs();
            BigDecimal bp = b.deltaFromUsualPercent == null ? BigDecimal.ZERO : b.deltaFromUsualPercent.abs();
            int c = bp.compareTo(ap);
            if (c != 0) return c;
            String ad = cleanToNull(a.latestPurchaseDate);
            String bd = cleanToNull(b.latestPurchaseDate);
            if (ad != null && bd != null) {
                c = bd.compareTo(ad);
                if (c != 0) return c;
            } else if (ad != null) {
                return -1;
            } else if (bd != null) {
                return 1;
            }
            c = safe(a.canonicalName).compareToIgnoreCase(safe(b.canonicalName));
            if (c != 0) return c;
            c = safe(a.productId).compareTo(safe(b.productId));
            if (c != 0) return c;
            return safe(a.basisKey).compareTo(safe(b.basisKey));
        }
    };

    private enum FieldKind { CANONICAL, STRUCTURED, OBSERVED, CATEGORY, STORE }

    private static final class FieldValue {
        final FieldKind kind;
        final String text;
        FieldValue(FieldKind kind, String text) { this.kind = kind; this.text = text; }
    }

    private static final class BuiltEntry {
        final SearchBrowseEntryV1 entry;
        final List<FieldValue> fields;
        BuiltEntry(SearchBrowseEntryV1 entry, List<FieldValue> fields) { this.entry = entry; this.fields = fields; }
    }

    private static final class Match {
        final int score;
        final String reason;
        Match(int score, String reason) { this.score = score; this.reason = reason; }
    }
}
