package com.receiptledger.v1.catalog;

import com.receiptledger.v1.item.ValueOrigin;
import com.receiptledger.v1.product.LinkSource;
import com.receiptledger.v1.validation.ValidationStatus;
import java.util.Objects;

/** Logical immutable projection of one saved receipt item linked to one catalog entity. */
public final class PurchaseObservationV2 {
    public final String receiptId;
    public final int itemOrdinal;
    public final String catalogEntryId;
    public final LinkSource identityLinkSource;
    public final String rawItemName;
    public final String purchaseDate;
    public final String storeName;
    public final long createdAtMillis;
    public final CatalogField<PurchaseForm> purchaseForm;
    public final ValueOrigin quantityOrigin;
    public final Long unitPrice;
    public final ValueOrigin unitPriceOrigin;
    public final Long lineAmount;
    public final ValueOrigin lineAmountOrigin;
    public final ValidationStatus receiptValidation;

    public PurchaseObservationV2(
            String receiptId,
            int itemOrdinal,
            String catalogEntryId,
            LinkSource identityLinkSource,
            String rawItemName,
            String purchaseDate,
            String storeName,
            long createdAtMillis,
            CatalogField<PurchaseForm> purchaseForm,
            ValueOrigin quantityOrigin,
            Long unitPrice,
            ValueOrigin unitPriceOrigin,
            Long lineAmount,
            ValueOrigin lineAmountOrigin,
            ValidationStatus receiptValidation) {
        this.receiptId = required(receiptId, "receiptId");
        if (itemOrdinal < 0) throw new IllegalArgumentException("itemOrdinal");
        this.itemOrdinal = itemOrdinal;
        this.catalogEntryId = required(catalogEntryId, "catalogEntryId");
        this.identityLinkSource = Objects.requireNonNull(identityLinkSource, "identityLinkSource");
        this.rawItemName = rawItemName == null ? "" : rawItemName;
        this.purchaseDate = purchaseDate;
        this.storeName = storeName;
        this.createdAtMillis = createdAtMillis;
        this.purchaseForm = purchaseForm == null ? CatalogField.absent() : purchaseForm;
        this.quantityOrigin = quantityOrigin == null ? ValueOrigin.UNKNOWN : quantityOrigin;
        this.unitPrice = nonNegative(unitPrice, "unitPrice");
        this.unitPriceOrigin = unitPriceOrigin == null ? ValueOrigin.UNKNOWN : unitPriceOrigin;
        this.lineAmount = nonNegative(lineAmount, "lineAmount");
        this.lineAmountOrigin = lineAmountOrigin == null ? ValueOrigin.UNKNOWN : lineAmountOrigin;
        this.receiptValidation = Objects.requireNonNull(receiptValidation, "receiptValidation");
    }

    private static String required(String value, String name) {
        String clean = value == null ? "" : value.trim();
        if (clean.isEmpty()) throw new IllegalArgumentException(name);
        return clean;
    }

    private static Long nonNegative(Long value, String name) {
        if (value != null && value < 0) throw new IllegalArgumentException(name);
        return value;
    }
}
