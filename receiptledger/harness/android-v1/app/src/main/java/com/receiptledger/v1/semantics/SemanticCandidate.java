package com.receiptledger.v1.semantics;

import com.receiptledger.v1.catalog.CatalogField;
import java.util.Objects;

/** One unconfirmed semantic candidate extracted from receipt text. */
public final class SemanticCandidate<T> {
    public final T value;
    public final String evidence;
    public final CatalogField.Confidence confidence;
    public final String reason;

    private SemanticCandidate(T value, String evidence, CatalogField.Confidence confidence, String reason) {
        this.value = Objects.requireNonNull(value, "value");
        this.evidence = required(evidence, "evidence");
        this.confidence = Objects.requireNonNull(confidence, "confidence");
        this.reason = required(reason, "reason");
        if (confidence == CatalogField.Confidence.UNKNOWN) {
            throw new IllegalArgumentException("present semantic candidate cannot use UNKNOWN confidence");
        }
    }

    public static <T> SemanticCandidate<T> of(
            T value,
            String evidence,
            CatalogField.Confidence confidence,
            String reason) {
        return new SemanticCandidate<>(value, evidence, confidence, reason);
    }

    /** Parsed evidence is always unconfirmed; CP23 confidence never grants identity authority. */
    public CatalogField<T> asCatalogField() {
        return CatalogField.parsed(value, confidence);
    }

    private static String required(String value, String name) {
        String clean = value == null ? "" : value.trim();
        if (clean.isEmpty()) throw new IllegalArgumentException(name);
        return clean;
    }
}
