package com.receiptledger.v1.layout;

import com.receiptledger.v1.ocr.OcrBlock;
import com.receiptledger.v1.ocr.OcrDocument;
import com.receiptledger.v1.ocr.OcrElement;
import com.receiptledger.v1.ocr.OcrLine;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class ReceiptLayoutAnalyzer {
    private static final double MAX_ABS_SKEW = 0.35;

    public ReceiptLayout analyze(OcrDocument document) {
        List<LayoutToken> tokens = flatten(document);
        if (tokens.isEmpty()) return new ReceiptLayout(new ArrayList<>(), 0, 0.0, 0.0);

        double medianHeight = medianHeights(tokens);
        double slope = estimateSkew(tokens);
        List<Positioned> positioned = new ArrayList<>(tokens.size());
        for (LayoutToken token : tokens) {
            positioned.add(new Positioned(token, token.centerY - slope * token.centerX));
        }
        Collections.sort(positioned, (a,b) -> {
            int c = Double.compare(a.correctedY, b.correctedY);
            return c != 0 ? c : Double.compare(a.token.centerX, b.token.centerX);
        });

        double tolerance = Math.max(3.0, medianHeight * 0.62);
        List<RowBuilder> builders = new ArrayList<>();
        for (Positioned p : positioned) {
            RowBuilder best = null;
            double bestDistance = Double.POSITIVE_INFINITY;
            for (RowBuilder row : builders) {
                double distance = Math.abs(p.correctedY - row.meanY());
                if (distance <= tolerance && distance < bestDistance) {
                    best = row; bestDistance = distance;
                }
            }
            if (best == null) {
                best = new RowBuilder();
                builders.add(best);
            }
            best.add(p);
        }
        Collections.sort(builders, (a,b) -> Double.compare(a.meanY(), b.meanY()));

        List<ReceiptRow> rows = new ArrayList<>(builders.size());
        for (RowBuilder builder : builders) {
            rows.add(new ReceiptRow(builder.tokens(), builder.meanY()));
        }
        return new ReceiptLayout(rows, tokens.size(), slope, medianHeight);
    }

    private static List<LayoutToken> flatten(OcrDocument document) {
        List<LayoutToken> out = new ArrayList<>();
        if (document == null) return out;
        for (OcrBlock block : document.blocks) {
            for (OcrLine line : block.lines) {
                for (OcrElement element : line.elements) {
                    LayoutToken token = LayoutToken.from(element);
                    if (token != null) out.add(token);
                }
            }
        }
        return out;
    }

    private static double estimateSkew(List<LayoutToken> tokens) {
        List<Double> slopes = new ArrayList<>();
        for (LayoutToken token : tokens) {
            double slope = token.edgeSlope();
            if (Double.isFinite(slope) && Math.abs(slope) <= MAX_ABS_SKEW) slopes.add(slope);
        }
        return slopes.isEmpty() ? 0.0 : median(slopes);
    }

    private static double medianHeights(List<LayoutToken> tokens) {
        List<Double> heights = new ArrayList<>(tokens.size());
        for (LayoutToken token : tokens) heights.add(token.height);
        return median(heights);
    }

    private static double median(List<Double> values) {
        Collections.sort(values);
        int n = values.size();
        return (n & 1) == 1 ? values.get(n / 2) : (values.get(n / 2 - 1) + values.get(n / 2)) * 0.5;
    }

    private static final class Positioned {
        final LayoutToken token; final double correctedY;
        Positioned(LayoutToken token, double correctedY) { this.token = token; this.correctedY = correctedY; }
    }

    private static final class RowBuilder {
        final List<Positioned> items = new ArrayList<>();
        double ySum;
        void add(Positioned p) { items.add(p); ySum += p.correctedY; }
        double meanY() { return ySum / items.size(); }
        List<LayoutToken> tokens() { List<LayoutToken> out = new ArrayList<>(); for (Positioned p : items) out.add(p.token); return out; }
    }
}
