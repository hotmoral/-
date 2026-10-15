package com.receiptledger.v1.document;

public final class PerspectivePlan {
    public final int outputWidth;
    public final int outputHeight;
    public final ProjectiveTransform sourceToOutput;
    public final ProjectiveTransform outputToSource;

    private PerspectivePlan(int outputWidth, int outputHeight, ProjectiveTransform sourceToOutput) {
        this.outputWidth = outputWidth;
        this.outputHeight = outputHeight;
        this.sourceToOutput = sourceToOutput;
        this.outputToSource = sourceToOutput.inverse();
    }

    public static PerspectivePlan create(Quad quad, int maxEdge, long maxPixels) {
        double width = (quad.topLeft.distanceTo(quad.topRight) + quad.bottomLeft.distanceTo(quad.bottomRight)) * 0.5;
        double height = (quad.topLeft.distanceTo(quad.bottomLeft) + quad.topRight.distanceTo(quad.bottomRight)) * 0.5;
        if (width < 2 || height < 2) throw new IllegalArgumentException("Document is too small");
        double scale = 1.0;
        if (Math.max(width, height) > maxEdge) scale = Math.min(scale, maxEdge / Math.max(width, height));
        if (width * height * scale * scale > maxPixels) {
            scale = Math.min(scale, Math.sqrt(maxPixels / (width * height)));
        }
        int outW = Math.max(2, (int) Math.round(width * scale));
        int outH = Math.max(2, (int) Math.round(height * scale));
        return new PerspectivePlan(outW, outH, ProjectiveTransform.fromQuadToRect(quad, outW, outH));
    }
}
