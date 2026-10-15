package com.receiptledger.v1.catalog;

import java.math.BigDecimal;

public enum SalesUnitCode {
    EACH(Dimension.COUNT, BigDecimal.ONE),
    GRAM(Dimension.WEIGHT, BigDecimal.ONE),
    KILOGRAM(Dimension.WEIGHT, new BigDecimal("1000")),
    MILLILITER(Dimension.VOLUME, BigDecimal.ONE),
    LITER(Dimension.VOLUME, new BigDecimal("1000")),
    BAG(Dimension.PACKAGE_FORM, null),
    PACK(Dimension.PACKAGE_FORM, null),
    BOX(Dimension.PACKAGE_FORM, null),
    BUNDLE(Dimension.PACKAGE_FORM, null),
    OTHER(Dimension.OTHER, null),
    UNKNOWN(Dimension.UNKNOWN, null);

    public enum Dimension { COUNT, WEIGHT, VOLUME, PACKAGE_FORM, OTHER, UNKNOWN }

    public final Dimension dimension;
    private final BigDecimal factorToBase;

    SalesUnitCode(Dimension dimension, BigDecimal factorToBase) {
        this.dimension = dimension;
        this.factorToBase = factorToBase;
    }

    public boolean supportsExactBaseConversion() {
        return factorToBase != null;
    }

    public BigDecimal toBase(BigDecimal amount) {
        if (!supportsExactBaseConversion()) {
            throw new IllegalStateException("unit has no exact base conversion: " + name());
        }
        return amount.multiply(factorToBase);
    }
}
