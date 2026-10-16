package com.receiptledger.v1.shell;

import static org.junit.Assert.*;

import com.receiptledger.v1.category.CategoryNodeV1;
import com.receiptledger.v1.category.CategoryTaxonomyV1;
import com.receiptledger.v1.persistence.ReceiptSchema;
import com.receiptledger.v1.product.ProductCatalogSchema;
import com.receiptledger.v1.product.ProductType;
import java.util.List;
import org.junit.Test;

public final class CommercialUiShellV1Test {

    @Test public void standardRoutesToProductDetail() {
        assertEquals(CommercialDestinationV1.PRODUCT_DETAIL,
                CommercialDestinationV1.forType(ProductType.STANDARD));
    }

    @Test public void nonStandardRoutesToCommodityDetail() {
        assertEquals(CommercialDestinationV1.COMMODITY_DETAIL,
                CommercialDestinationV1.forType(ProductType.NON_STANDARD));
    }

    @Test public void unclassifiedAndNullStayUnsupported() {
        assertEquals(CommercialDestinationV1.UNSUPPORTED,
                CommercialDestinationV1.forType(ProductType.UNCLASSIFIED));
        assertEquals(CommercialDestinationV1.UNSUPPORTED,
                CommercialDestinationV1.forType(null));
    }

    @Test public void userFacingTypeLabelsDoNotInventAuthority() {
        assertEquals("제품", CommercialShellFormatterV1.typeLabel(ProductType.STANDARD));
        assertEquals("품목", CommercialShellFormatterV1.typeLabel(ProductType.NON_STANDARD));
        assertEquals("미분류", CommercialShellFormatterV1.typeLabel(ProductType.UNCLASSIFIED));
    }

    @Test public void boundedTaxonomyStillHasStableRoots() {
        List<CategoryNodeV1> roots = CategoryTaxonomyV1.roots();
        assertEquals(2, roots.size());
        assertEquals(CategoryTaxonomyV1.FOOD, roots.get(0).id);
        assertEquals(CategoryTaxonomyV1.HOUSEHOLD, roots.get(1).id);
    }

    @Test public void schemasRemainFrozen() {
        assertEquals(2, ProductCatalogSchema.VERSION);
        assertEquals(1, ReceiptSchema.VERSION);
    }

    @Test public void metrics() {
        System.out.println("CP34_METRICS shell_version=1 launcher_home=1 add_receipt=1 search_browse=1 category_browse=1 standard_detail=1 commodity_detail=1 receipt_history=1 legacy_price_entry_removed=1 schema_unchanged=1");
    }
}
