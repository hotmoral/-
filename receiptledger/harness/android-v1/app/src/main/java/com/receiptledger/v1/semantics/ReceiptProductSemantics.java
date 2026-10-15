package com.receiptledger.v1.semantics;

import com.receiptledger.v1.catalog.ProductSpecification;
import com.receiptledger.v1.catalog.PurchaseForm;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Immutable CP23 parse result. It contains evidence only and never a catalog identity. */
public final class ReceiptProductSemantics {
    public final String rawName;
    public final SemanticCandidate<String> brand;
    public final SemanticCandidate<String> productName;
    public final SemanticCandidate<String> variant;
    public final SemanticCandidate<ProductSpecification> specification;
    public final SemanticCandidate<PurchaseForm> purchaseForm;
    public final boolean measureAmbiguous;
    public final boolean reviewRequired;
    public final List<String> reviewReasons;

    ReceiptProductSemantics(
            String rawName,
            SemanticCandidate<String> brand,
            SemanticCandidate<String> productName,
            SemanticCandidate<String> variant,
            SemanticCandidate<ProductSpecification> specification,
            SemanticCandidate<PurchaseForm> purchaseForm,
            boolean measureAmbiguous,
            boolean reviewRequired,
            List<String> reviewReasons) {
        this.rawName = rawName == null ? "" : rawName;
        this.brand = brand;
        this.productName = productName;
        this.variant = variant;
        this.specification = specification;
        this.purchaseForm = purchaseForm;
        this.measureAmbiguous = measureAmbiguous;
        this.reviewRequired = reviewRequired;
        this.reviewReasons = Collections.unmodifiableList(new ArrayList<>(reviewReasons));
    }

    public boolean hasStructuredEvidence() {
        return brand != null || variant != null || specification != null || purchaseForm != null;
    }

    /** Means only that CP23 parsing is sufficiently explicit; never means auto-link authority. */
    public boolean semanticReadyForResolver() {
        return productName != null && !reviewRequired;
    }
}
