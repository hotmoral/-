package com.receiptledger.v1.commodity;

import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.catalog.SalesUnitCode;
import com.receiptledger.v1.product.ProductNameNormalizer;
import java.math.BigDecimal;

/** Form relation only. It never compares prices and never invents a unit conversion. */
public final class CommodityFormRelationV2 {
    public enum Relation {
        EXACT_NORMALIZABLE_QUANTITY,
        SAME_FORM_ONLY,
        INCOMPARABLE,
        MISSING
    }

    public final Relation relation;
    public final BigDecimal leftBaseQuantity;
    public final BigDecimal rightBaseQuantity;

    private CommodityFormRelationV2(Relation relation, BigDecimal leftBaseQuantity, BigDecimal rightBaseQuantity) {
        this.relation = relation;
        this.leftBaseQuantity = leftBaseQuantity;
        this.rightBaseQuantity = rightBaseQuantity;
    }

    public static CommodityFormRelationV2 classify(PurchaseForm left, PurchaseForm right) {
        if (left == null || right == null) return new CommodityFormRelationV2(Relation.MISSING, null, null);

        if (left.unit.supportsExactBaseConversion()
                && right.unit.supportsExactBaseConversion()
                && left.unit.dimension == right.unit.dimension) {
            return new CommodityFormRelationV2(
                    Relation.EXACT_NORMALIZABLE_QUANTITY,
                    left.unit.toBase(left.quantity),
                    right.unit.toBase(right.quantity));
        }

        if (left.unit.dimension == SalesUnitCode.Dimension.PACKAGE_FORM
                && left.unit == right.unit) {
            return new CommodityFormRelationV2(Relation.SAME_FORM_ONLY, null, null);
        }

        if (left.unit == SalesUnitCode.OTHER && right.unit == SalesUnitCode.OTHER
                && ProductNameNormalizer.key(left.rawUnitLabel)
                .equals(ProductNameNormalizer.key(right.rawUnitLabel))) {
            return new CommodityFormRelationV2(Relation.SAME_FORM_ONLY, null, null);
        }

        return new CommodityFormRelationV2(Relation.INCOMPARABLE, null, null);
    }
}
