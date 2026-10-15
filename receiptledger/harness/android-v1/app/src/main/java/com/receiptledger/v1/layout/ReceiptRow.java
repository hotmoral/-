package com.receiptledger.v1.layout;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public final class ReceiptRow {
    public final List<LayoutToken> tokens;
    public final String text;
    public final double correctedCenterY;

    ReceiptRow(List<LayoutToken> source, double correctedCenterY) {
        List<LayoutToken> copy = new ArrayList<>(source);
        copy.sort(Comparator.comparingDouble(t -> t.centerX));
        this.tokens = Collections.unmodifiableList(copy);
        this.correctedCenterY = correctedCenterY;
        this.text = join(copy);
    }

    private static String join(List<LayoutToken> tokens) {
        StringBuilder out = new StringBuilder();
        LayoutToken previous = null;
        for (LayoutToken token : tokens) {
            if (out.length() > 0) {
                double gap = token.centerX - token.width * 0.5 - (previous.centerX + previous.width * 0.5);
                if (gap > Math.max(2.0, Math.min(previous.height, token.height) * 0.20)) out.append(' ');
            }
            out.append(token.text);
            previous = token;
        }
        return out.toString();
    }
}
