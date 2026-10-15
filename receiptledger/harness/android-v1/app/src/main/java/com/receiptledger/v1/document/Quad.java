package com.receiptledger.v1.document;

public final class Quad {
    public final PointD topLeft;
    public final PointD topRight;
    public final PointD bottomRight;
    public final PointD bottomLeft;

    public Quad(PointD topLeft, PointD topRight, PointD bottomRight, PointD bottomLeft) {
        this.topLeft = topLeft;
        this.topRight = topRight;
        this.bottomRight = bottomRight;
        this.bottomLeft = bottomLeft;
    }

    public double area() {
        PointD[] p = {topLeft, topRight, bottomRight, bottomLeft};
        double sum = 0.0;
        for (int i = 0; i < p.length; i++) {
            PointD a = p[i];
            PointD b = p[(i + 1) % p.length];
            sum += a.x * b.y - b.x * a.y;
        }
        return Math.abs(sum) * 0.5;
    }

    public boolean isConvex() {
        PointD[] p = {topLeft, topRight, bottomRight, bottomLeft};
        double sign = 0.0;
        for (int i = 0; i < p.length; i++) {
            PointD a = p[i];
            PointD b = p[(i + 1) % p.length];
            PointD c = p[(i + 2) % p.length];
            double cross = (b.x - a.x) * (c.y - b.y) - (b.y - a.y) * (c.x - b.x);
            if (Math.abs(cross) < 1e-9) {
                return false;
            }
            if (sign == 0.0) {
                sign = Math.signum(cross);
            } else if (Math.signum(cross) != sign) {
                return false;
            }
        }
        return true;
    }

    public PointD[] points() {
        return new PointD[] {topLeft, topRight, bottomRight, bottomLeft};
    }
}
