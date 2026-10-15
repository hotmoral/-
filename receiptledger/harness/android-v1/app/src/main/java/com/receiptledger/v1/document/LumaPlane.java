package com.receiptledger.v1.document;

import java.util.Arrays;

public final class LumaPlane {
    private final int width;
    private final int height;
    private final byte[] luma;

    public LumaPlane(int width, int height, byte[] luma) {
        if (width <= 0 || height <= 0 || luma == null || luma.length != width * height) {
            throw new IllegalArgumentException("Invalid luma plane");
        }
        this.width = width;
        this.height = height;
        this.luma = Arrays.copyOf(luma, luma.length);
    }

    public int width() { return width; }
    public int height() { return height; }

    public int get(int x, int y) {
        return luma[y * width + x] & 0xff;
    }
}
