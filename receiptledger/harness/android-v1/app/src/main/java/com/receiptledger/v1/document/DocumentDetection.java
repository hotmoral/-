package com.receiptledger.v1.document;

public final class DocumentDetection {
    public final boolean found;
    public final Quad quad;
    public final double confidence;
    public final String reason;

    private DocumentDetection(boolean found, Quad quad, double confidence, String reason) {
        this.found = found;
        this.quad = quad;
        this.confidence = confidence;
        this.reason = reason;
    }

    public static DocumentDetection found(Quad quad, double confidence) {
        return new DocumentDetection(true, quad, confidence, "OK");
    }

    public static DocumentDetection none(String reason) {
        return new DocumentDetection(false, null, 0.0, reason);
    }
}
