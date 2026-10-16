package com.receiptledger.v1.shell;

import com.receiptledger.v1.product.ProductType;

/** Pure CP34 mapping from frozen product type to commercial detail destination. */
public enum CommercialDestinationV1 {
    PRODUCT_DETAIL,
    COMMODITY_DETAIL,
    UNSUPPORTED;

    public static CommercialDestinationV1 forType(ProductType type) {
        if (type == ProductType.STANDARD) return PRODUCT_DETAIL;
        if (type == ProductType.NON_STANDARD) return COMMODITY_DETAIL;
        return UNSUPPORTED;
    }
}
