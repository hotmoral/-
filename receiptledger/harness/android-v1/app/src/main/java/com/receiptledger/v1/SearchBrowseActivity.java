package com.receiptledger.v1;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Gravity;
import android.view.inputmethod.EditorInfo;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;
import com.receiptledger.v1.category.CategoryNodeV1;
import com.receiptledger.v1.category.CategoryTaxonomyV1;
import com.receiptledger.v1.design.DesignTokensV1;
import com.receiptledger.v1.design.ResponsiveLayoutPolicyV1;
import com.receiptledger.v1.design.UiKitV1;
import com.receiptledger.v1.persistence.SqliteReceiptStore;
import com.receiptledger.v1.priceeval.PriceEvaluationServiceV1;
import com.receiptledger.v1.priceintel.PriceIntelligenceServiceV2;
import com.receiptledger.v1.product.SqliteProductCatalogStore;
import com.receiptledger.v1.search.SearchBrowseEntryV1;
import com.receiptledger.v1.search.SearchBrowseQueryV1;
import com.receiptledger.v1.search.SearchBrowseServiceV1;
import com.receiptledger.v1.shell.CommercialDestinationV1;
import com.receiptledger.v1.shell.CommercialShellFormatterV1;
import com.receiptledger.v1.ui.SystemBarInsetHelper;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** CP34 normal-user discovery screen backed exclusively by the frozen CP29 read-only service. */
public final class SearchBrowseActivity extends Activity {
    public static final String EXTRA_MODE = "com.receiptledger.v1.extra.BROWSE_MODE";
    public static final String MODE_RECENT = "RECENT";
    public static final String MODE_FREQUENT = "FREQUENT";
    private static final int RESULT_LIMIT = 50;

    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private SqliteReceiptStore receipts;
    private SqliteProductCatalogStore catalog;
    private SearchBrowseServiceV1 discovery;
    private EditText queryField;
    private TextView status;
    private LinearLayout categoryHost;
    private LinearLayout resultHost;
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

        content.addView(UiKitV1.title(this, R.string.search_browse_title));
        content.addView(UiKitV1.body(this, getString(R.string.search_browse_intro)),
                blockParams(DesignTokensV1.SPACE_2_DP));

        queryField = UiKitV1.searchField(this, getString(R.string.search_browse_hint));
        queryField.setImeOptions(EditorInfo.IME_ACTION_SEARCH);
        queryField.setOnEditorActionListener((v, actionId, event) -> {
            if (actionId == EditorInfo.IME_ACTION_SEARCH) {
                searchText();
                return true;
            }
            return false;
        });
        content.addView(queryField, blockParams(DesignTokensV1.SPACE_4_DP));
        Button search = UiKitV1.button(this, R.string.search_browse_action,
                v -> searchText(), UiKitV1.ButtonTone.PRIMARY);
        content.addView(search, blockParams(DesignTokensV1.SPACE_2_DP));

        LinearLayout quick = new LinearLayout(this);
        quick.setOrientation(LinearLayout.HORIZONTAL);
        Button recent = UiKitV1.button(this, R.string.search_browse_recent,
                v -> showRecent(), UiKitV1.ButtonTone.SECONDARY);
        Button frequent = UiKitV1.button(this, R.string.search_browse_frequent,
                v -> showFrequent(), UiKitV1.ButtonTone.SECONDARY);
        quick.addView(recent, weightedButtonParams(false));
        quick.addView(frequent, weightedButtonParams(true));
        content.addView(quick, blockParams(DesignTokensV1.SPACE_2_DP));

        content.addView(UiKitV1.sectionTitle(this, getString(R.string.search_browse_category)),
                blockParams(DesignTokensV1.SPACE_6_DP));
        categoryHost = new LinearLayout(this);
        categoryHost.setOrientation(LinearLayout.VERTICAL);
        content.addView(categoryHost, blockParams(DesignTokensV1.SPACE_1_DP));

        status = UiKitV1.status(this);
        content.addView(status, blockParams(DesignTokensV1.SPACE_4_DP));
        resultHost = new LinearLayout(this);
        resultHost.setOrientation(LinearLayout.VERTICAL);
        content.addView(resultHost);

        Button back = UiKitV1.button(this, R.string.search_browse_back,
                v -> finish(), UiKitV1.ButtonTone.SECONDARY);
        content.addView(back, blockParams(DesignTokensV1.SPACE_6_DP));

        setContentView(root);
        SystemBarInsetHelper.apply(this, root);
        renderCategoryNav(null);

        String mode = getIntent().getStringExtra(EXTRA_MODE);
        if (MODE_FREQUENT.equals(mode)) showFrequent();
        else showRecent();
    }

    private void searchText() {
        String text = queryField.getText().toString().trim();
        renderCategoryNav(null);
        if (text.isEmpty()) {
            showRecent();
            return;
        }
        load(getString(R.string.search_browse_searching), () ->
                discovery.search(SearchBrowseQueryV1.text(text, RESULT_LIMIT)).entries);
    }

    private void showRecent() {
        renderCategoryNav(null);
        load(getString(R.string.search_browse_loading_recent), () -> discovery.recent(RESULT_LIMIT));
    }

    private void showFrequent() {
        renderCategoryNav(null);
        load(getString(R.string.search_browse_loading_frequent), () -> discovery.frequent(RESULT_LIMIT));
    }

    private void selectCategory(String categoryId) {
        renderCategoryNav(categoryId);
        CategoryNodeV1 node = CategoryTaxonomyV1.require(categoryId);
        load(getString(R.string.search_browse_loading_category, node.displayNameKo),
                () -> discovery.byCategory(categoryId, RESULT_LIMIT));
    }

    private void renderCategoryNav(String categoryId) {
        categoryHost.removeAllViews();
        List<CategoryNodeV1> nodes;
        if (categoryId == null) {
            nodes = CategoryTaxonomyV1.roots();
        } else {
            CategoryNodeV1 selected = CategoryTaxonomyV1.require(categoryId);
            Button up = UiKitV1.listRow(this,
                    selected.parentId == null
                            ? getString(R.string.search_browse_all_categories)
                            : getString(R.string.search_browse_parent_category,
                                    CategoryTaxonomyV1.require(selected.parentId).displayNameKo),
                    v -> {
                        if (selected.parentId == null) {
                            renderCategoryNav(null);
                            showRecent();
                        } else {
                            selectCategory(selected.parentId);
                        }
                    });
            categoryHost.addView(up, blockParams(DesignTokensV1.SPACE_1_DP));
            nodes = CategoryTaxonomyV1.children(categoryId);
        }
        for (CategoryNodeV1 node : nodes) {
            Button row = UiKitV1.listRow(this, node.displayNameKo, v -> selectCategory(node.id));
            categoryHost.addView(row, blockParams(DesignTokensV1.SPACE_1_DP));
        }
    }

    private void load(String loadingText, EntryLoader loader) {
        final long ticket = ++generation;
        status.setText(loadingText);
        resultHost.removeAllViews();
        worker.execute(() -> {
            List<SearchBrowseEntryV1> rows;
            Exception error = null;
            try {
                rows = loader.load();
            } catch (Exception e) {
                rows = Collections.emptyList();
                error = e;
            }
            final List<SearchBrowseEntryV1> result = rows;
            final Exception failure = error;
            runOnUiThread(() -> {
                if (ticket != generation) return;
                resultHost.removeAllViews();
                if (failure != null) {
                    status.setText(R.string.search_browse_failed);
                    return;
                }
                status.setText(getString(R.string.search_browse_count, result.size()));
                if (result.isEmpty()) {
                    resultHost.addView(UiKitV1.body(this, getString(R.string.search_browse_empty)));
                    return;
                }
                for (SearchBrowseEntryV1 entry : result) {
                    resultHost.addView(UiKitV1.listRow(this,
                            CommercialShellFormatterV1.resultRow(entry),
                            v -> openEntry(entry)), blockParams(DesignTokensV1.SPACE_1_DP));
                }
            });
        });
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
            Toast.makeText(this, R.string.search_browse_unsupported, Toast.LENGTH_SHORT).show();
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

    private interface EntryLoader { List<SearchBrowseEntryV1> load(); }
}
