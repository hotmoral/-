package com.receiptledger.v1.priceintel;

import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.catalog.SalesUnitCode;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.persistence.ReceiptStore;
import com.receiptledger.v1.product.CatalogProduct;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.ItemLinkRef;
import com.receiptledger.v1.product.ProductCatalogStore;
import com.receiptledger.v1.product.ProductType;
import com.receiptledger.v1.validation.ValidationStatus;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Receipt-derived CP27 engine. It never mutates identity, purchase form or receipt truth. */
public final class PriceIntelligenceServiceV2 {
    private final ReceiptStore receipts;
    private final ProductCatalogStore catalog;
    private final CatalogV2PersistenceStore v2Store;

    public PriceIntelligenceServiceV2(ReceiptStore receipts, ProductCatalogStore catalog, CatalogV2PersistenceStore v2Store) {
        if (receipts == null || catalog == null || v2Store == null) throw new IllegalArgumentException("stores");
        this.receipts = receipts;
        this.catalog = catalog;
        this.v2Store = v2Store;
    }

    public PriceIntelligenceV2 analyze(String productId) { return analyze(productId, PriceScopeV2.all()); }

    public PriceIntelligenceV2 analyze(String productId, PriceScopeV2 scope) {
        CatalogProduct product = catalog.product(productId);
        if (product == null) throw new IllegalArgumentException("unknown product");
        if (product.type == ProductType.UNCLASSIFIED) throw new IllegalArgumentException("UNCLASSIFIED has no price intelligence");
        PriceScopeV2 effectiveScope = scope == null ? PriceScopeV2.all() : scope;

        List<PriceObservationV2> observations = new ArrayList<>();
        for (ItemLinkRef ref : catalog.linksForProduct(productId)) {
            ReceiptRecord receipt = receipts.get(ref.receiptId);
            if (receipt == null || !effectiveScope.matches(receipt.purchaseDate, receipt.storeName)) continue;
            PersistedItem item = find(receipt.items, ref.itemOrdinal);
            if (item == null) continue;
            observations.add(derive(product, ref, receipt, item));
        }
        Collections.sort(observations, PriceCohortV2.NEWEST_FIRST);

        Map<String,ComparisonBasisV2> bases = new HashMap<>();
        Map<String,List<PriceObservationV2>> byBasis = new HashMap<>();
        for (PriceObservationV2 observation : observations) {
            if (!observation.isEligible()) continue;
            String key = observation.basis.key();
            bases.put(key, observation.basis);
            List<PriceObservationV2> rows = byBasis.get(key);
            if (rows == null) {
                rows = new ArrayList<>();
                byBasis.put(key, rows);
            }
            rows.add(observation);
        }
        List<String> keys = new ArrayList<>(bases.keySet());
        Collections.sort(keys);
        List<PriceCohortV2> cohorts = new ArrayList<>();
        for (String key : keys) cohorts.add(PriceCohortV2.from(bases.get(key), byBasis.get(key)));
        return new PriceIntelligenceV2(product, effectiveScope, observations, cohorts);
    }

    private PriceObservationV2 derive(CatalogProduct product, ItemLinkRef ref, ReceiptRecord receipt, PersistedItem item) {
        CatalogField<PurchaseForm> formField = safeForm(v2Store.purchaseFormV2(receipt.id, item.ordinal));
        PurchaseForm form = formField.isPresent() ? formField.value : null;

        if (!valid(receipt.validationStatus)) {
            return excluded(ref, receipt, item, formField, PriceObservationV2.Eligibility.INVALID_RECEIPT,
                    "receipt validation is not PASS/PASS_WITH_WARNINGS", PriceObservationV2.DiscountTreatment.NONE);
        }

        EffectiveLine effective = effectiveLine(receipt, item);
        if (effective.exclusion != null) {
            return excluded(ref, receipt, item, formField, effective.exclusion, effective.reason, effective.discountTreatment);
        }

        if (product.type == ProductType.STANDARD) {
            return deriveStandard(ref, receipt, item, formField, effective);
        }
        if (product.type == ProductType.NON_STANDARD) {
            return deriveCommodity(ref, receipt, item, formField, effective);
        }
        return excluded(ref, receipt, item, formField, PriceObservationV2.Eligibility.MISSING_ITEM_PRICE,
                "unsupported product type", effective.discountTreatment);
    }

    private PriceObservationV2 deriveStandard(ItemLinkRef ref, ReceiptRecord receipt, PersistedItem item,
            CatalogField<PurchaseForm> formField, EffectiveLine effective) {
        Integer quantity = item.quantity;
        if (effective.amount != null && quantity != null && quantity > 0) {
            if (effective.discountTreatment == PriceObservationV2.DiscountTreatment.NONE
                    && item.unitPrice != null && item.unitPrice >= 0 && item.lineAmount != null) {
                Long expected = multiply(item.unitPrice, quantity);
                if (expected == null || expected.longValue() != item.lineAmount.longValue()) {
                    return excluded(ref, receipt, item, formField, PriceObservationV2.Eligibility.ITEM_PRICE_CONFLICT,
                            "unitPrice * quantity does not equal lineAmount", effective.discountTreatment);
                }
            }
            PriceObservationV2.PriceSource source = effective.discountTreatment == PriceObservationV2.DiscountTreatment.SOLE_ITEM_EXACT
                    ? PriceObservationV2.PriceSource.SOLE_ITEM_NET_LINE_PER_QUANTITY
                    : PriceObservationV2.PriceSource.LINE_AMOUNT_PER_ITEM_QUANTITY;
            return eligible(ref, receipt, item, formField, effective.discountTreatment,
                    ComparisonBasisV2.standardPackage(), source,
                    BigDecimal.valueOf(effective.amount), BigDecimal.valueOf(quantity));
        }
        if (effective.discountTreatment == PriceObservationV2.DiscountTreatment.NONE
                && item.unitPrice != null && item.unitPrice >= 0) {
            return eligible(ref, receipt, item, formField, effective.discountTreatment,
                    ComparisonBasisV2.standardPackage(), PriceObservationV2.PriceSource.PRINTED_UNIT_PRICE,
                    BigDecimal.valueOf(item.unitPrice), BigDecimal.ONE);
        }
        return excluded(ref, receipt, item, formField, PriceObservationV2.Eligibility.MISSING_ITEM_PRICE,
                "STANDARD comparison needs traceable unit price or line amount + quantity", effective.discountTreatment);
    }

    private PriceObservationV2 deriveCommodity(ItemLinkRef ref, ReceiptRecord receipt, PersistedItem item,
            CatalogField<PurchaseForm> formField, EffectiveLine effective) {
        if (effective.amount == null) {
            return excluded(ref, receipt, item, formField, PriceObservationV2.Eligibility.MISSING_ITEM_PRICE,
                    "commodity comparison needs line amount", effective.discountTreatment);
        }
        if (!formField.isPresent()) {
            return excluded(ref, receipt, item, formField, PriceObservationV2.Eligibility.MISSING_PURCHASE_FORM,
                    "commodity comparison needs observed PurchaseForm", effective.discountTreatment);
        }
        PurchaseForm form = formField.value;
        ComparisonBasisV2 basis;
        BigDecimal denominator;
        SalesUnitCode.Dimension dimension = form.unit.dimension;
        if (dimension == SalesUnitCode.Dimension.WEIGHT && form.unit.supportsExactBaseConversion()) {
            basis = ComparisonBasisV2.weightKg();
            denominator = form.unit.toBase(form.quantity).divide(new BigDecimal("1000"));
        } else if (dimension == SalesUnitCode.Dimension.VOLUME && form.unit.supportsExactBaseConversion()) {
            basis = ComparisonBasisV2.volumeLiter();
            denominator = form.unit.toBase(form.quantity).divide(new BigDecimal("1000"));
        } else if (dimension == SalesUnitCode.Dimension.COUNT && form.unit.supportsExactBaseConversion()) {
            basis = ComparisonBasisV2.each();
            denominator = form.unit.toBase(form.quantity);
        } else if (dimension == SalesUnitCode.Dimension.PACKAGE_FORM || dimension == SalesUnitCode.Dimension.OTHER) {
            basis = ComparisonBasisV2.likeForm(form.unit.name(), form.rawUnitLabel);
            denominator = form.quantity;
        } else {
            return excluded(ref, receipt, item, formField, PriceObservationV2.Eligibility.UNSUPPORTED_PURCHASE_FORM,
                    "purchase form has no safe comparison basis", effective.discountTreatment);
        }
        if (denominator.compareTo(BigDecimal.ZERO) <= 0) {
            return excluded(ref, receipt, item, formField, PriceObservationV2.Eligibility.UNSUPPORTED_PURCHASE_FORM,
                    "purchase form denominator is not positive", effective.discountTreatment);
        }
        PriceObservationV2.PriceSource source = effective.discountTreatment == PriceObservationV2.DiscountTreatment.SOLE_ITEM_EXACT
                ? PriceObservationV2.PriceSource.SOLE_ITEM_NET_LINE_PER_PURCHASE_FORM
                : PriceObservationV2.PriceSource.LINE_AMOUNT_PER_PURCHASE_FORM;
        return eligible(ref, receipt, item, formField, effective.discountTreatment, basis, source,
                BigDecimal.valueOf(effective.amount), denominator);
    }

    private EffectiveLine effectiveLine(ReceiptRecord receipt, PersistedItem item) {
        long discount = receipt.discountSum == null ? 0L : receipt.discountSum;
        if (discount != 0L) {
            if (receipt.items.size() != 1 || item.lineAmount == null) {
                return EffectiveLine.excluded(PriceObservationV2.Eligibility.UNALLOCATED_RECEIPT_DISCOUNT,
                        "discount exists but cannot be attributed to this item without guessing",
                        PriceObservationV2.DiscountTreatment.UNALLOCATED_MULTI_ITEM);
            }
            Long net = add(item.lineAmount, discount);
            if (net == null || net < 0) {
                return EffectiveLine.excluded(PriceObservationV2.Eligibility.NEGATIVE_EFFECTIVE_AMOUNT,
                        "sole-item lineAmount + discount is invalid", PriceObservationV2.DiscountTreatment.SOLE_ITEM_EXACT);
            }
            return EffectiveLine.value(net, PriceObservationV2.DiscountTreatment.SOLE_ITEM_EXACT);
        }
        if (item.lineAmount != null) {
            if (item.lineAmount < 0) {
                return EffectiveLine.excluded(PriceObservationV2.Eligibility.NEGATIVE_EFFECTIVE_AMOUNT,
                        "negative line amount", PriceObservationV2.DiscountTreatment.NONE);
            }
            return EffectiveLine.value(item.lineAmount, PriceObservationV2.DiscountTreatment.NONE);
        }
        return EffectiveLine.value(null, PriceObservationV2.DiscountTreatment.NONE);
    }

    private PriceObservationV2 eligible(ItemLinkRef ref, ReceiptRecord receipt, PersistedItem item,
            CatalogField<PurchaseForm> formField, PriceObservationV2.DiscountTreatment discountTreatment,
            ComparisonBasisV2 basis, PriceObservationV2.PriceSource source,
            BigDecimal numerator, BigDecimal denominator) {
        PurchaseForm form = formField.isPresent() ? formField.value : null;
        return PriceObservationV2.eligible(receipt.id, item.ordinal, receipt.purchaseDate, receipt.storeName,
                receipt.createdAtMillis, item.name, item.quantity, item.unitPrice, item.lineAmount, receipt.discountSum,
                receipt.validationStatus, ref.source, form, formField.source, formField.confirmation, formField.confidence,
                discountTreatment, basis, source, numerator, denominator);
    }

    private PriceObservationV2 excluded(ItemLinkRef ref, ReceiptRecord receipt, PersistedItem item,
            CatalogField<PurchaseForm> formField, PriceObservationV2.Eligibility eligibility, String reason,
            PriceObservationV2.DiscountTreatment discountTreatment) {
        PurchaseForm form = formField.isPresent() ? formField.value : null;
        return PriceObservationV2.excluded(receipt.id, item.ordinal, receipt.purchaseDate, receipt.storeName,
                receipt.createdAtMillis, item.name, item.quantity, item.unitPrice, item.lineAmount, receipt.discountSum,
                receipt.validationStatus, ref.source, form, formField.source, formField.confirmation, formField.confidence,
                eligibility, reason, discountTreatment);
    }

    private static CatalogField<PurchaseForm> safeForm(CatalogField<PurchaseForm> field) {
        return field == null ? CatalogField.<PurchaseForm>absent() : field;
    }

    private static PersistedItem find(List<PersistedItem> items, int ordinal) {
        for (PersistedItem item : items) if (item.ordinal == ordinal) return item;
        return null;
    }

    private static boolean valid(ValidationStatus status) {
        return status == ValidationStatus.PASS || status == ValidationStatus.PASS_WITH_WARNINGS;
    }

    private static Long add(long a, long b) {
        try { return Math.addExact(a, b); } catch (ArithmeticException e) { return null; }
    }

    private static Long multiply(long a, int b) {
        try { return Math.multiplyExact(a, (long)b); } catch (ArithmeticException e) { return null; }
    }

    private static final class EffectiveLine {
        final Long amount;
        final PriceObservationV2.DiscountTreatment discountTreatment;
        final PriceObservationV2.Eligibility exclusion;
        final String reason;
        private EffectiveLine(Long amount, PriceObservationV2.DiscountTreatment treatment,
                PriceObservationV2.Eligibility exclusion, String reason) {
            this.amount = amount;
            this.discountTreatment = treatment;
            this.exclusion = exclusion;
            this.reason = reason;
        }
        static EffectiveLine value(Long amount, PriceObservationV2.DiscountTreatment treatment) {
            return new EffectiveLine(amount, treatment, null, null);
        }
        static EffectiveLine excluded(PriceObservationV2.Eligibility exclusion, String reason,
                PriceObservationV2.DiscountTreatment treatment) {
            return new EffectiveLine(null, treatment, exclusion, reason);
        }
    }
}
