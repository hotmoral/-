package com.receiptledger.v1.priceintel;

import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/** Deterministic statistics for exactly one comparison basis. */
public final class PriceCohortV2 {
    public enum Strength { STRICT_NORMALIZED, CONTEXTUAL_LIKE_FORM }

    public final ComparisonBasisV2 basis;
    public final Strength strength;
    public final List<PriceObservationV2> observations;
    public final BigDecimal latest;
    public final BigDecimal previous;
    public final BigDecimal delta;
    public final BigDecimal deltaPercent;
    public final BigDecimal min;
    public final BigDecimal max;
    public final BigDecimal mean;
    public final BigDecimal median;

    private PriceCohortV2(
            ComparisonBasisV2 basis,
            List<PriceObservationV2> observations,
            BigDecimal latest,
            BigDecimal previous,
            BigDecimal delta,
            BigDecimal deltaPercent,
            BigDecimal min,
            BigDecimal max,
            BigDecimal mean,
            BigDecimal median) {
        this.basis = basis;
        this.strength = basis.isStrictNormalized() ? Strength.STRICT_NORMALIZED : Strength.CONTEXTUAL_LIKE_FORM;
        this.observations = Collections.unmodifiableList(observations);
        this.latest = latest;
        this.previous = previous;
        this.delta = delta;
        this.deltaPercent = deltaPercent;
        this.min = min;
        this.max = max;
        this.mean = mean;
        this.median = median;
    }

    public static PriceCohortV2 from(ComparisonBasisV2 basis, List<PriceObservationV2> source) {
        if (basis == null) throw new IllegalArgumentException("basis");
        List<PriceObservationV2> rows = new ArrayList<>();
        if (source != null) {
            for (PriceObservationV2 observation : source) {
                if (observation != null && observation.isEligible() && basis.equals(observation.basis)) rows.add(observation);
            }
        }
        Collections.sort(rows, NEWEST_FIRST);
        if (rows.isEmpty()) return new PriceCohortV2(basis, rows, null, null, null, null, null, null, null, null);

        BigDecimal latest = rows.get(0).comparisonPriceMinor;
        BigDecimal previous = rows.size() > 1 ? rows.get(1).comparisonPriceMinor : null;
        BigDecimal delta = previous == null ? null : latest.subtract(previous);
        BigDecimal deltaPercent = null;
        if (previous != null && previous.compareTo(BigDecimal.ZERO) != 0) {
            deltaPercent = delta.multiply(new BigDecimal("100"))
                    .divide(previous, 4, RoundingMode.HALF_UP).stripTrailingZeros();
        }

        List<BigDecimal> amounts = new ArrayList<>();
        BigDecimal sum = BigDecimal.ZERO;
        BigDecimal min = latest;
        BigDecimal max = latest;
        for (PriceObservationV2 row : rows) {
            BigDecimal amount = row.comparisonPriceMinor;
            amounts.add(amount);
            sum = sum.add(amount);
            if (amount.compareTo(min) < 0) min = amount;
            if (amount.compareTo(max) > 0) max = amount;
        }
        Collections.sort(amounts);
        BigDecimal mean = sum.divide(BigDecimal.valueOf(amounts.size()), MathContext.DECIMAL128).stripTrailingZeros();
        BigDecimal median;
        int middle = amounts.size() / 2;
        if ((amounts.size() & 1) == 1) {
            median = amounts.get(middle);
        } else {
            median = amounts.get(middle - 1).add(amounts.get(middle))
                    .divide(new BigDecimal("2"), MathContext.DECIMAL128).stripTrailingZeros();
        }
        return new PriceCohortV2(basis, rows, latest, previous, delta, deltaPercent,
                min.stripTrailingZeros(), max.stripTrailingZeros(), mean, median.stripTrailingZeros());
    }

    public int count() { return observations.size(); }

    static final Comparator<PriceObservationV2> NEWEST_FIRST = new Comparator<PriceObservationV2>() {
        @Override public int compare(PriceObservationV2 a, PriceObservationV2 b) {
            String ad = clean(a.purchaseDate);
            String bd = clean(b.purchaseDate);
            if (ad != null && bd != null) {
                int c = bd.compareTo(ad);
                if (c != 0) return c;
            } else if (ad != null) {
                return -1;
            } else if (bd != null) {
                return 1;
            }
            int c = Long.compare(b.createdAtMillis, a.createdAtMillis);
            if (c != 0) return c;
            c = safe(a.receiptId).compareTo(safe(b.receiptId));
            if (c != 0) return c;
            return Integer.compare(a.itemOrdinal, b.itemOrdinal);
        }
    };

    private static String clean(String value) {
        if (value == null) return null;
        String v = value.trim();
        return v.isEmpty() ? null : v;
    }

    private static String safe(String value) { return value == null ? "" : value; }
}
