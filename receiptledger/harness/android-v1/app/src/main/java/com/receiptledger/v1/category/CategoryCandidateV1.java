package com.receiptledger.v1.category;

import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.CategoryRef;
import java.util.Objects;

/** One deterministic taxonomy candidate. It never carries identity authority. */
public final class CategoryCandidateV1 {
    public final CategoryRef category;
    public final CatalogField.Confidence confidence;
    public final int score;
    public final String reason;

    public CategoryCandidateV1(CategoryRef category, CatalogField.Confidence confidence, int score, String reason) {
        this.category = Objects.requireNonNull(category, "category");
        this.confidence = Objects.requireNonNull(confidence, "confidence");
        if (confidence == CatalogField.Confidence.UNKNOWN) throw new IllegalArgumentException("confidence");
        if (score <= 0) throw new IllegalArgumentException("score");
        this.score = score;
        String clean = reason == null ? "" : reason.trim();
        if (clean.isEmpty()) throw new IllegalArgumentException("reason");
        this.reason = clean;
    }
}
