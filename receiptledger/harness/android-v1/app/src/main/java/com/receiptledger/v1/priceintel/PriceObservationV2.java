package com.receiptledger.v1.priceintel;

import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.product.LinkSource;
import com.receiptledger.v1.validation.ValidationStatus;
import java.math.BigDecimal;
import java.math.MathContext;

/** One receipt-traceable CP27 price observation. Excluded rows stay visible with an explicit reason. */
public final class PriceObservationV2 {
    public enum Eligibility {
        ELIGIBLE,
        INVALID_RECEIPT,
        MISSING_ITEM_PRICE,
        NEGATIVE_EFFECTIVE_AMOUNT,
        UNALLOCATED_RECEIPT_DISCOUNT,
        ITEM_PRICE_CONFLICT,
        MISSING_PURCHASE_FORM,
        UNSUPPORTED_PURCHASE_FORM
    }

    public enum PriceSource {
        LINE_AMOUNT_PER_ITEM_QUANTITY,
        PRINTED_UNIT_PRICE,
        SOLE_ITEM_NET_LINE_PER_QUANTITY,
        LINE_AMOUNT_PER_PURCHASE_FORM,
        SOLE_ITEM_NET_LINE_PER_PURCHASE_FORM
    }

    public enum DiscountTreatment {
        NONE,
        SOLE_ITEM_EXACT,
        UNALLOCATED_MULTI_ITEM
    }

    public final String receiptId;
    public final int itemOrdinal;
    public final String purchaseDate;
    public final String storeName;
    public final long createdAtMillis;
    public final String rawItemName;
    public final Integer receiptItemQuantity;
    public final Long rawUnitPrice;
    public final Long rawLineAmount;
    public final Long receiptDiscountSum;
    public final ValidationStatus receiptValidation;
    public final LinkSource linkSource;
    public final PurchaseForm purchaseForm;
    public final CatalogField.Source purchaseFormSource;
    public final CatalogField.Confirmation purchaseFormConfirmation;
    public final CatalogField.Confidence purchaseFormConfidence;
    public final Eligibility eligibility;
    public final String exclusionReason;
    public final DiscountTreatment discountTreatment;
    public final ComparisonBasisV2 basis;
    public final PriceSource priceSource;
    public final BigDecimal sourceNumeratorMinor;
    public final BigDecimal sourceDenominator;
    public final BigDecimal comparisonPriceMinor;

    private PriceObservationV2(
            String receiptId,
            int itemOrdinal,
            String purchaseDate,
            String storeName,
            long createdAtMillis,
            String rawItemName,
            Integer receiptItemQuantity,
            Long rawUnitPrice,
            Long rawLineAmount,
            Long receiptDiscountSum,
            ValidationStatus receiptValidation,
            LinkSource linkSource,
            PurchaseForm purchaseForm,
            CatalogField.Source purchaseFormSource,
            CatalogField.Confirmation purchaseFormConfirmation,
            CatalogField.Confidence purchaseFormConfidence,
            Eligibility eligibility,
            String exclusionReason,
            DiscountTreatment discountTreatment,
            ComparisonBasisV2 basis,
            PriceSource priceSource,
            BigDecimal numeratorMinor,
            BigDecimal denominator) {
        this.receiptId = receiptId;
        this.itemOrdinal = itemOrdinal;
        this.purchaseDate = purchaseDate;
        this.storeName = storeName;
        this.createdAtMillis = createdAtMillis;
        this.rawItemName = rawItemName;
        this.receiptItemQuantity = receiptItemQuantity;
        this.rawUnitPrice = rawUnitPrice;
        this.rawLineAmount = rawLineAmount;
        this.receiptDiscountSum = receiptDiscountSum;
        this.receiptValidation = receiptValidation;
        this.linkSource = linkSource;
        this.purchaseForm = purchaseForm;
        this.purchaseFormSource = purchaseFormSource;
        this.purchaseFormConfirmation = purchaseFormConfirmation;
        this.purchaseFormConfidence = purchaseFormConfidence;
        this.eligibility = eligibility;
        this.exclusionReason = exclusionReason;
        this.discountTreatment = discountTreatment;
        this.basis = basis;
        this.priceSource = priceSource;
        this.sourceNumeratorMinor = numeratorMinor;
        this.sourceDenominator = denominator;
        this.comparisonPriceMinor = numeratorMinor == null || denominator == null
                ? null : numeratorMinor.divide(denominator, MathContext.DECIMAL128).stripTrailingZeros();
    }

    public static PriceObservationV2 eligible(
            String receiptId, int itemOrdinal, String purchaseDate, String storeName, long createdAtMillis,
            String rawItemName, Integer receiptItemQuantity, Long rawUnitPrice, Long rawLineAmount,
            Long receiptDiscountSum, ValidationStatus receiptValidation, LinkSource linkSource,
            PurchaseForm purchaseForm, CatalogField.Source purchaseFormSource,
            CatalogField.Confirmation purchaseFormConfirmation, CatalogField.Confidence purchaseFormConfidence,
            DiscountTreatment discountTreatment, ComparisonBasisV2 basis, PriceSource priceSource,
            BigDecimal numeratorMinor, BigDecimal denominator) {
        if (basis == null || priceSource == null || numeratorMinor == null || denominator == null
                || denominator.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("eligible observation requires positive traceable rate");
        }
        return new PriceObservationV2(receiptId, itemOrdinal, purchaseDate, storeName, createdAtMillis, rawItemName,
                receiptItemQuantity, rawUnitPrice, rawLineAmount, receiptDiscountSum, receiptValidation, linkSource,
                purchaseForm, purchaseFormSource, purchaseFormConfirmation, purchaseFormConfidence,
                Eligibility.ELIGIBLE, null, discountTreatment, basis, priceSource, numeratorMinor, denominator);
    }

    public static PriceObservationV2 excluded(
            String receiptId, int itemOrdinal, String purchaseDate, String storeName, long createdAtMillis,
            String rawItemName, Integer receiptItemQuantity, Long rawUnitPrice, Long rawLineAmount,
            Long receiptDiscountSum, ValidationStatus receiptValidation, LinkSource linkSource,
            PurchaseForm purchaseForm, CatalogField.Source purchaseFormSource,
            CatalogField.Confirmation purchaseFormConfirmation, CatalogField.Confidence purchaseFormConfidence,
            Eligibility eligibility, String reason, DiscountTreatment discountTreatment) {
        if (eligibility == null || eligibility == Eligibility.ELIGIBLE) throw new IllegalArgumentException("excluded eligibility");
        return new PriceObservationV2(receiptId, itemOrdinal, purchaseDate, storeName, createdAtMillis, rawItemName,
                receiptItemQuantity, rawUnitPrice, rawLineAmount, receiptDiscountSum, receiptValidation, linkSource,
                purchaseForm, purchaseFormSource, purchaseFormConfirmation, purchaseFormConfidence,
                eligibility, reason == null ? eligibility.name() : reason, discountTreatment, null, null, null, null);
    }

    public boolean isEligible() { return eligibility == Eligibility.ELIGIBLE; }
    public boolean isStrictComparable() { return isEligible() && basis.isStrictNormalized(); }
}
