package com.receiptledger.v1.catalog;

import com.receiptledger.v1.product.ProductNameNormalizer;
import java.util.Objects;

/** Immutable V2 catalog entity. Entity equality is stable-ID equality only. */
public final class CatalogEntryV2 {
    public enum RecordOrigin { NATIVE_V2, LEGACY_V1 }

    public final String id;
    public final CatalogKind kind;
    public final String canonicalName;
    public final String canonicalKey;
    public final CatalogField<String> brand;
    public final CatalogField<String> productName;
    public final CatalogField<String> variant;
    public final CatalogField<ProductSpecification> specification;
    public final CategoryRef category;
    public final long createdAtMillis;
    public final RecordOrigin recordOrigin;

    private CatalogEntryV2(
            String id,
            CatalogKind kind,
            String canonicalName,
            CatalogField<String> brand,
            CatalogField<String> productName,
            CatalogField<String> variant,
            CatalogField<ProductSpecification> specification,
            CategoryRef category,
            long createdAtMillis,
            RecordOrigin recordOrigin) {
        String cleanId = id == null ? "" : id.trim();
        String cleanName = canonicalName == null ? "" : canonicalName.trim();
        if (cleanId.isEmpty()) throw new IllegalArgumentException("id");
        if (cleanName.isEmpty()) throw new IllegalArgumentException("canonicalName");
        this.id = cleanId;
        this.kind = Objects.requireNonNull(kind, "kind");
        this.canonicalName = cleanName;
        this.canonicalKey = ProductNameNormalizer.key(cleanName);
        this.brand = safe(brand);
        this.productName = safe(productName);
        this.variant = safe(variant);
        this.specification = safe(specification);
        this.category = category;
        this.createdAtMillis = createdAtMillis;
        this.recordOrigin = Objects.requireNonNull(recordOrigin, "recordOrigin");

        if (kind == CatalogKind.NON_STANDARD_COMMODITY) {
            if (this.brand.isPresent() || this.productName.isPresent() || this.variant.isPresent() || this.specification.isPresent()) {
                throw new IllegalArgumentException("commodity cannot carry STANDARD product fields");
            }
        } else if (recordOrigin == RecordOrigin.NATIVE_V2 && !this.productName.isPresent()) {
            throw new IllegalArgumentException("native STANDARD product requires productName");
        }
    }

    public static CatalogEntryV2 standard(
            String id,
            String canonicalName,
            CatalogField<String> brand,
            CatalogField<String> productName,
            CatalogField<String> variant,
            CatalogField<ProductSpecification> specification,
            CategoryRef category,
            long createdAtMillis) {
        return new CatalogEntryV2(id, CatalogKind.STANDARD_PRODUCT, canonicalName, brand, productName, variant,
                specification, category, createdAtMillis, RecordOrigin.NATIVE_V2);
    }

    public static CatalogEntryV2 commodity(String id, String canonicalName, CategoryRef category, long createdAtMillis) {
        return new CatalogEntryV2(id, CatalogKind.NON_STANDARD_COMMODITY, canonicalName,
                CatalogField.absent(), CatalogField.absent(), CatalogField.absent(), CatalogField.absent(),
                category, createdAtMillis, RecordOrigin.NATIVE_V2);
    }

    /** Rehydrates an already-persisted entity without changing CP21 validation semantics. */
    public static CatalogEntryV2 rehydrate(
            String id,
            CatalogKind kind,
            String canonicalName,
            CatalogField<String> brand,
            CatalogField<String> productName,
            CatalogField<String> variant,
            CatalogField<ProductSpecification> specification,
            CategoryRef category,
            long createdAtMillis,
            RecordOrigin recordOrigin) {
        return new CatalogEntryV2(id, kind, canonicalName, brand, productName, variant, specification,
                category, createdAtMillis, recordOrigin);
    }

    static CatalogEntryV2 legacy(String id, CatalogKind kind, String canonicalName, long createdAtMillis) {
        return new CatalogEntryV2(id, kind, canonicalName,
                CatalogField.absent(), CatalogField.absent(), CatalogField.absent(), CatalogField.absent(),
                null, createdAtMillis, RecordOrigin.LEGACY_V1);
    }

    private static <T> CatalogField<T> safe(CatalogField<T> value) {
        return value == null ? CatalogField.absent() : value;
    }

    @Override public boolean equals(Object other) {
        return other instanceof CatalogEntryV2 && id.equals(((CatalogEntryV2) other).id);
    }

    @Override public int hashCode() {
        return id.hashCode();
    }

    @Override public String toString() {
        return kind + ":" + id + ":" + canonicalName;
    }
}
