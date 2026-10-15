package com.receiptledger.v1.catalog;

import java.util.Objects;

/** Immutable semantic value with independent source, confidence and confirmation state. */
public final class CatalogField<T> {
    public enum Source {
        UNKNOWN,
        RECEIPT_TEXT,
        PARSED_FROM_RECEIPT,
        USER_CONFIRMED,
        CONFIRMED_KNOWLEDGE,
        LEGACY_IMPORT
    }

    public enum Confirmation {
        UNCONFIRMED,
        CONFIRMED
    }

    public enum Confidence {
        UNKNOWN,
        LOW,
        MEDIUM,
        HIGH
    }

    public final T value;
    public final Source source;
    public final Confirmation confirmation;
    public final Confidence confidence;

    private CatalogField(T value, Source source, Confirmation confirmation, Confidence confidence) {
        this.value = value;
        this.source = Objects.requireNonNull(source, "source");
        this.confirmation = Objects.requireNonNull(confirmation, "confirmation");
        this.confidence = Objects.requireNonNull(confidence, "confidence");
        if (value == null) {
            if (source != Source.UNKNOWN || confirmation != Confirmation.UNCONFIRMED || confidence != Confidence.UNKNOWN) {
                throw new IllegalArgumentException("absent field must use UNKNOWN/UNCONFIRMED/UNKNOWN");
            }
        } else if (source == Source.UNKNOWN) {
            throw new IllegalArgumentException("present field requires a known source");
        }
    }

    public static <T> CatalogField<T> absent() {
        return new CatalogField<>(null, Source.UNKNOWN, Confirmation.UNCONFIRMED, Confidence.UNKNOWN);
    }

    public static <T> CatalogField<T> of(T value, Source source, Confirmation confirmation, Confidence confidence) {
        return new CatalogField<>(Objects.requireNonNull(value, "value"), source, confirmation, confidence);
    }

    public static <T> CatalogField<T> parsed(T value, Confidence confidence) {
        return of(value, Source.PARSED_FROM_RECEIPT, Confirmation.UNCONFIRMED, confidence);
    }

    public static <T> CatalogField<T> userConfirmed(T value) {
        return of(value, Source.USER_CONFIRMED, Confirmation.CONFIRMED, Confidence.HIGH);
    }

    public static <T> CatalogField<T> reusedConfirmed(T value) {
        return of(value, Source.CONFIRMED_KNOWLEDGE, Confirmation.CONFIRMED, Confidence.HIGH);
    }

    public static <T> CatalogField<T> legacyImport(T value) {
        return of(value, Source.LEGACY_IMPORT, Confirmation.UNCONFIRMED, Confidence.UNKNOWN);
    }

    public boolean isPresent() {
        return value != null;
    }

    public boolean isConfirmed() {
        return value != null && confirmation == Confirmation.CONFIRMED;
    }

    @Override public boolean equals(Object other) {
        if (this == other) return true;
        if (!(other instanceof CatalogField<?>)) return false;
        CatalogField<?> that = (CatalogField<?>) other;
        return Objects.equals(value, that.value) && source == that.source && confirmation == that.confirmation && confidence == that.confidence;
    }

    @Override public int hashCode() {
        return Objects.hash(value, source, confirmation, confidence);
    }
}
