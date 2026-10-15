package com.receiptledger.v1.document;

public final class PointD {
    public final double x;
    public final double y;

    public PointD(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public double distanceTo(PointD other) {
        double dx = x - other.x;
        double dy = y - other.y;
        return Math.hypot(dx, dy);
    }

    @Override
    public String toString() {
        return "(" + x + "," + y + ")";
    }
}
