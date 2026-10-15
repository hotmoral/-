package com.receiptledger.v1.layout;

import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.ocr.OcrElement;

public final class LayoutToken {
    public final String text;
    public final Quad inputQuad;
    public final Quad sourceQuad;
    public final double centerX;
    public final double centerY;
    public final double width;
    public final double height;

    private LayoutToken(String text, Quad inputQuad, Quad sourceQuad,
                        double centerX, double centerY, double width, double height) {
        this.text = text;
        this.inputQuad = inputQuad;
        this.sourceQuad = sourceQuad;
        this.centerX = centerX;
        this.centerY = centerY;
        this.width = width;
        this.height = height;
    }

    public static LayoutToken from(OcrElement element) {
        if (element == null || element.inputQuad == null || element.text == null || element.text.trim().isEmpty()) {
            return null;
        }
        Quad q = element.inputQuad;
        PointD[] p = q.points();
        double cx = 0, cy = 0;
        for (PointD point : p) { cx += point.x; cy += point.y; }
        cx /= 4.0; cy /= 4.0;
        double width = (q.topLeft.distanceTo(q.topRight) + q.bottomLeft.distanceTo(q.bottomRight)) * 0.5;
        double height = (q.topLeft.distanceTo(q.bottomLeft) + q.topRight.distanceTo(q.bottomRight)) * 0.5;
        if (!Double.isFinite(cx) || !Double.isFinite(cy) || width < 0.5 || height < 0.5) return null;
        return new LayoutToken(element.text.trim(), q, element.sourceQuad, cx, cy, width, height);
    }

    public double edgeSlope() {
        double dx1 = inputQuad.topRight.x - inputQuad.topLeft.x;
        double dx2 = inputQuad.bottomRight.x - inputQuad.bottomLeft.x;
        double s = 0.0; int n = 0;
        if (Math.abs(dx1) >= 2.0) { s += (inputQuad.topRight.y - inputQuad.topLeft.y) / dx1; n++; }
        if (Math.abs(dx2) >= 2.0) { s += (inputQuad.bottomRight.y - inputQuad.bottomLeft.y) / dx2; n++; }
        return n == 0 ? Double.NaN : s / n;
    }
}
