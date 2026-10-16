package com.receiptledger.v1;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import com.receiptledger.v1.design.UiKitV1;
import com.receiptledger.v1.persistence.SqliteReceiptStore;
import com.receiptledger.v1.price.PriceHistory;
import com.receiptledger.v1.price.PriceHistoryFormatter;
import com.receiptledger.v1.price.PriceHistoryService;
import com.receiptledger.v1.product.CatalogProduct;
import com.receiptledger.v1.product.ProductType;
import com.receiptledger.v1.product.SqliteProductCatalogStore;
import com.receiptledger.v1.ui.SystemBarInsetHelper;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class PriceHistoryActivity extends Activity {
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private SqliteReceiptStore receipts;
    private SqliteProductCatalogStore catalog;
    private PriceHistoryService service;
    private LinearLayout products;
    private TextView detail;
    private TextView status;
    private long generation;

    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        receipts = new SqliteReceiptStore(getApplicationContext());
        catalog = new SqliteProductCatalogStore(getApplicationContext());
        service = new PriceHistoryService(receipts, catalog);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        UiKitV1.applyPage(this, root);
        TextView title = UiKitV1.title(this, R.string.price_history_title);
        status = UiKitV1.status(this);
        ScrollView productScroll = new ScrollView(this);
        products = new LinearLayout(this);
        products.setOrientation(LinearLayout.VERTICAL);
        productScroll.addView(products);
        detail = UiKitV1.body(this, "");
        detail.setTextIsSelectable(true);
        ScrollView detailScroll = new ScrollView(this);
        detailScroll.addView(detail);
        Button close = UiKitV1.button(this, R.string.close_library, v -> finish(), UiKitV1.ButtonTone.SECONDARY);
        root.addView(title);
        root.addView(close);
        root.addView(status);
        root.addView(productScroll, new LinearLayout.LayoutParams(-1, 0, 0.38f));
        root.addView(detailScroll, new LinearLayout.LayoutParams(-1, 0, 0.62f));
        setContentView(root);
        SystemBarInsetHelper.apply(this, root);
        loadProducts();
    }

    private void loadProducts() {
        long ticket = ++generation;
        worker.execute(() -> {
            List<CatalogProduct> list = catalog.listProducts();
            runOnUiThread(() -> {
                if (ticket != generation) return;
                products.removeAllViews();
                status.setText(getString(R.string.price_product_count, list.size()));
                for (CatalogProduct product : list) {
                    Button row = UiKitV1.listRow(
                            this,
                            getString(R.string.price_product_button, product.type, product.canonicalName),
                            v -> openProduct(product));
                    products.addView(row);
                }
            });
        });
    }

    private void openProduct(CatalogProduct product) {
        if (product.type == ProductType.STANDARD) {
            Intent intent = new Intent(this, ProductDetailActivity.class);
            intent.putExtra(ProductDetailActivity.EXTRA_PRODUCT_ID, product.id);
            startActivity(intent);
            return;
        }
        if (product.type == ProductType.NON_STANDARD) {
            Intent intent = new Intent(this, CommodityDetailActivity.class);
            intent.putExtra(CommodityDetailActivity.EXTRA_PRODUCT_ID, product.id);
            startActivity(intent);
            return;
        }
        loadLegacyHistory(product.id);
    }

    private void loadLegacyHistory(String productId) {
        long ticket = ++generation;
        status.setText(R.string.price_loading);
        worker.execute(() -> {
            try {
                PriceHistory history = service.history(productId);
                runOnUiThread(() -> {
                    if (ticket == generation) {
                        detail.setText(PriceHistoryFormatter.format(history));
                        status.setText(getString(R.string.price_observation_count, history.observations.size()));
                    }
                });
            } catch (Exception e) {
                runOnUiThread(() -> { if (ticket == generation) status.setText(e.getMessage()); });
            }
        });
    }

    @Override protected void onDestroy() {
        generation++;
        worker.shutdownNow();
        catalog.close();
        receipts.close();
        super.onDestroy();
    }
}
