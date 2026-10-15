package com.receiptledger.v1.layout;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class ReceiptLayout {
    public final List<ReceiptRow> rows;
    public final int tokenCount;
    public final double estimatedSkewSlope;
    public final double medianTokenHeight;

    ReceiptLayout(List<ReceiptRow> rows, int tokenCount, double estimatedSkewSlope, double medianTokenHeight) {
        this.rows = Collections.unmodifiableList(new ArrayList<>(rows));
        this.tokenCount = tokenCount;
        this.estimatedSkewSlope = estimatedSkewSlope;
        this.medianTokenHeight = medianTokenHeight;
    }

    public String reconstructedText() {
        StringBuilder out = new StringBuilder();
        for (ReceiptRow row : rows) {
            if (out.length() > 0) out.append('\n');
            out.append(row.text);
        }
        return out.toString();
    }
}
