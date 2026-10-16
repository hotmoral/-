package com.receiptledger.v1;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import com.receiptledger.v1.design.DesignTokensV1;
import com.receiptledger.v1.design.ResponsiveLayoutPolicyV1;
import com.receiptledger.v1.design.SemanticPresentationV1;
import com.receiptledger.v1.design.SemanticToneV1;
import com.receiptledger.v1.design.UiKitV1;
import com.receiptledger.v1.persistence.SqliteReceiptStore;
import com.receiptledger.v1.priceeval.PriceEvaluationServiceV1;
import com.receiptledger.v1.priceintel.PriceIntelligenceServiceV2;
import com.receiptledger.v1.product.SqliteProductCatalogStore;
import com.receiptledger.v1.search.SearchBrowseEntryV1;
import com.receiptledger.v1.search.SearchBrowseServiceV1;
import com.receiptledger.v1.shell.CommercialDestinationV1;
import com.receiptledger.v1.shell.CommercialShellFormatterV1;
import com.receiptledger.v1.ui.SystemBarInsetHelper;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** CP34 launcher: product-centric entry into the already-frozen ReceiptLedger capabilities. */
public final class HomeActivity extends Activity {
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private SqliteReceiptStore receipts;
    private SqliteProductCatalogStore catalog;
    private SearchBrowseServiceV1 discovery;
    private LinearLayout recentHost;
    private TextView recentStatus;
    private long generation;

    @Override protected void onCreate(Bundle state) {
        super.onCreate(state);
        receipts = new SqliteReceiptStore(getApplicationContext());
        catalog = new SqliteProductCatalogStore(getApplicationContext());
        PriceIntelligenceServiceV2 priceIntel = new PriceIntelligenceServiceV2(receipts, catalog, catalog);
        discovery = new SearchBrowseServiceV1(
                receipts, catalog, catalog, priceIntel, new PriceEvaluationServiceV1());

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL);
        UiKitV1.applyPage(this, root);

        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        root.addView(scroll, new LinearLayout.LayoutParams(-1, 0, 1f));

        LinearLayout content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        scroll.addView(content, new ScrollView.LayoutParams(
                contentWidthPx(), ScrollView.LayoutParams.WRAP_CONTENT,
                Gravity.TOP | Gravity.CENTER_HORIZONTAL));

        content.addView(UiKitV1.title(this, R.string.home_title));
        TextView intro = UiKitV1.body(this, getString(R.string.home_intro));
        content.addView(intro, blockParams(DesignTokensV1.SPACE_2_DP));

        content.addView(UiKitV1.semanticCard(this, SemanticPresentationV1.display(
                getString(R.string.home_memory_title),
                getString(R.string.home_memory_body),
                SemanticToneV1.INFO)), blockParams(DesignTokensV1.SPACE_4_DP));

        Button add = UiKitV1.button(this, R.string.home_add_receipt,
                v -> startActivity(new Intent(this, MainActivity.class)), UiKitV1.ButtonTone.PRIMARY);
        content.addView(add, blockParams(DesignTokensV1.SPACE_3_DP));

        TextView findTitle = UiKitV1.sectionTitle(this, getString(R.string.home_find_section));
        content.addView(findTitle, blockParams(DesignTokensV1.SPACE_6_DP));

        Button find = UiKitV1.button(this, R.string.home_find,
                v -> startActivity(new Intent(this, SearchBrowseActivity.class)), UiKitV1.ButtonTone.SECONDARY);
        content.addView(find, blockParams(DesignTokensV1.SPACE_2_DP));

        LinearLayout browseActions = new LinearLayout(this);
        browseActions.setOrientation(LinearLayout.HORIZONTAL);
        Button recent = UiKitV1.button(this, R.string.home_recent,
                v -> openBrowse(SearchBrowseActivity.MODE_RECENT), UiKitV1.ButtonTone.SECONDARY);
        Button frequent = UiKitV1.button(this, R.string.home_frequent,
                v -> openBrowse(SearchBrowseActivity.MODE_FREQUENT), UiKitV1.ButtonTone.SECONDARY);
        browseActions.addView(recent, weightedButtonParams(false));
        browseActions.addView(frequent, weightedButtonParams(true));
        content.addView(browseActions, blockParams(DesignTokensV1.SPACE_2_DP));

        TextView recentTitle = UiKitV1.sectionTitle(this, getString(R.string.home_recent_title));
        content.addView(recentTitle, blockParams(DesignTokensV1.SPACE_6_DP));
        recentStatus = UiKitV1.status(this);
        content.addView(recentStatus);
        recentHost = new LinearLayout(this);
        recentHost.setOrientation(LinearLayout.VERTICAL);
        content.addView(recentHost);

        TextView receiptTitle = UiKitV1.sectionTitle(this, getString(R.string.home_receipt_section));
        content.addView(receiptTitle, blockParams(DesignTokensV1.SPACE_6_DP));
        Button history = UiKitV1.button(this, R.string.home_receipts,
                v -> startActivity(new Intent(this, LibraryActivity.class)), UiKitV1.ButtonTone.SECONDARY);
        content.addView(history, blockParams(DesignTokensV1.SPACE_2_DP));

        setContentView(root);
        SystemBarInsetHelper.apply(this, root);
    }

    @Override protected void onResume() {
        super.onResume();
        loadRecent();
    }

    private void loadRecent() {
        final long ticket = ++generation;
        recentStatus.setText(R.string.home_recent_loading);
        worker.execute(() -> {
            List<SearchBrowseEntryV1> rows;
            Exception error = null;
            try {
                rows = discovery.recent(3);
            } catch (Exception e) {
                rows = Collections.emptyList();
                error = e;
            }
            final List<SearchBrowseEntryV1> result = rows;
            final Exception failure = error;
            runOnUiThread(() -> {
                if (ticket != generation) return;
                recentHost.removeAllViews();
                if (failure != null) {
                    recentStatus.setText(R.string.home_recent_failed);
                    return;
                }
                if (result.isEmpty()) {
                    recentStatus.setText(R.string.home_recent_empty);
                    return;
                }
                recentStatus.setText(getString(R.string.home_recent_count, result.size()));
                for (SearchBrowseEntryV1 entry : result) {
                    recentHost.addView(UiKitV1.listRow(this,
                            CommercialShellFormatterV1.resultRow(entry),
                            v -> openEntry(entry)), blockParams(DesignTokensV1.SPACE_1_DP));
                }
            });
        });
    }

    private void openBrowse(String mode) {
        Intent intent = new Intent(this, SearchBrowseActivity.class);
        intent.putExtra(SearchBrowseActivity.EXTRA_MODE, mode);
        startActivity(intent);
    }

    private void openEntry(SearchBrowseEntryV1 entry) {
        CommercialDestinationV1 destination = CommercialDestinationV1.forType(entry.type);
        Intent intent;
        if (destination == CommercialDestinationV1.PRODUCT_DETAIL) {
            intent = new Intent(this, ProductDetailActivity.class);
            intent.putExtra(ProductDetailActivity.EXTRA_PRODUCT_ID, entry.productId);
        } else if (destination == CommercialDestinationV1.COMMODITY_DETAIL) {
            intent = new Intent(this, CommodityDetailActivity.class);
            intent.putExtra(CommodityDetailActivity.EXTRA_PRODUCT_ID, entry.productId);
        } else {
            return;
        }
        startActivity(intent);
    }

    private LinearLayout.LayoutParams blockParams(int topDp) {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(-1, -2);
        if (topDp > 0) params.topMargin = dp(topDp);
        return params;
    }

    private LinearLayout.LayoutParams weightedButtonParams(boolean marginStart) {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(0, -2, 1f);
        if (marginStart) params.setMarginStart(dp(DesignTokensV1.SPACE_2_DP));
        return params;
    }

    private int contentWidthPx() {
        int widthDp = getResources().getConfiguration().screenWidthDp;
        if (widthDp < 1) {
            widthDp = Math.max(1, Math.round(
                    getResources().getDisplayMetrics().widthPixels
                            / getResources().getDisplayMetrics().density));
        }
        int gutter = ResponsiveLayoutPolicyV1.pageGutterDp(widthDp);
        int available = Math.max(dp(240),
                getResources().getDisplayMetrics().widthPixels - dp(gutter * 2));
        return Math.min(available, dp(ResponsiveLayoutPolicyV1.contentMaxWidthDp()));
    }

    private int dp(int value) { return UiKitV1.dp(this, value); }

    @Override protected void onDestroy() {
        generation++;
        worker.shutdownNow();
        if (catalog != null) catalog.close();
        if (receipts != null) receipts.close();
        super.onDestroy();
    }
}
