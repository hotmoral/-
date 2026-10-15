package com.receiptledger.v1.catalog;

import java.math.BigDecimal;
import java.util.Objects;

/** Exact count/weight/volume fact usable in packaged-product specification. */
public final class PackageMeasure {
    public final BigDecimal amount;
    public final SalesUnitCode unit;

    public PackageMeasure(BigDecimal amount, SalesUnitCode unit) {
        this.amount = normalizedPositive(amount);
        this.unit = Objects.requireNonNull(unit, "unit");
        if (!unit.supportsExactBaseConversion()) {
            throw new IllegalArgumentException("package measure requires exact count/weight/volume unit");
        }
    }

    public PackageMeasure(String amount, SalesUnitCode unit) {
        this(new BigDecimal(amount), unit);
    }

    public BigDecimal baseAmount() {
        return normalize(unit.toBase(amount));
    }

    public String canonicalToken() {
        return unit.dimension.name() + ":" + baseAmount().toPlainString();
    }

    public boolean exactlyEquivalentTo(PackageMeasure other) {
        return other != null
                && unit.dimension == other.unit.dimension
                && baseAmount().compareTo(other.baseAmount()) == 0;
    }

    private static BigDecimal normalizedPositive(BigDecimal value) {
        Objects.requireNonNull(value, "amount");
        if (value.compareTo(BigDecimal.ZERO) <= 0) throw new IllegalArgumentException("amount must be positive");
        return normalize(value);
    }

    private static BigDecimal normalize(BigDecimal value) {
        BigDecimal stripped = value.stripTrailingZeros();
        return stripped.scale() < 0 ? stripped.setScale(0) : stripped;
    }

    @Override public String toString() {
        return amount.toPlainString() + " " + unit.name();
    }
}
