package com.receiptledger.v1.catalog;

import java.math.BigDecimal;
import java.util.Objects;

/** Raw purchase form for one observation; preserves display label without asserting comparability. */
public final class PurchaseForm {
    public final BigDecimal quantity;
    public final SalesUnitCode unit;
    public final String rawUnitLabel;

    public PurchaseForm(BigDecimal quantity, SalesUnitCode unit, String rawUnitLabel) {
        Objects.requireNonNull(quantity, "quantity");
        if (quantity.compareTo(BigDecimal.ZERO) <= 0) throw new IllegalArgumentException("quantity must be positive");
        this.quantity = normalize(quantity);
        this.unit = Objects.requireNonNull(unit, "unit");
        this.rawUnitLabel = rawUnitLabel == null ? "" : rawUnitLabel;
        if (unit == SalesUnitCode.OTHER && this.rawUnitLabel.trim().isEmpty()) {
            throw new IllegalArgumentException("OTHER requires raw unit label");
        }
    }

    public PurchaseForm(String quantity, SalesUnitCode unit, String rawUnitLabel) {
        this(new BigDecimal(quantity), unit, rawUnitLabel);
    }

    private static BigDecimal normalize(BigDecimal value) {
        BigDecimal stripped = value.stripTrailingZeros();
        return stripped.scale() < 0 ? stripped.setScale(0) : stripped;
    }

    @Override public String toString() {
        return quantity.toPlainString() + " " + unit.name() + " [" + rawUnitLabel + "]";
    }
}
