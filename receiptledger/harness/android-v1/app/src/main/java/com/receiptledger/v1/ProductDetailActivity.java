package com.receiptledger.v1;

import android.app.Activity;
import android.content.Intent;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import com.receiptledger.v1.design.DesignTokensV1;
import com.receiptledger.v1.design.ResponsiveLayoutPolicyV1;
import com.receiptledger.v1.design.SemanticPresentationV1;
import com.receiptledger.v1.design.SemanticToneV1;
import com.receiptledger.v1.design.UiKitV1;
import com.receiptledger.v1.detail.ProductDetailFormatterV1;
import com.receiptledger.v1.detail.ProductDetailServiceV1;
import com.receiptledger.v1.detail.ProductDetailV1;
import com.receiptledger.v1.detail.ProductPriceChartViewV1;
import com.receiptledger.v1.persistence.SqliteReceiptStore;
import com.receiptledger.v1.priceintel.PriceIntelligenceServiceV2;
import com.receiptledger.v1.product.SqliteProductCatalogStore;
import com.receiptledger.v1.ui.SystemBarInsetHelper;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** CP31 commercial STANDARD-product detail surface. */
public final class ProductDetailActivity extends Activity {
    public static final String EXTRA_PRODUCT_ID = "product_id";

    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private SqliteReceiptStore receipts;
    private SqliteProductCatalogStore catalog;
    private ProductDetailServiceV1 service;
    private LinearLayout page;
    private long generation;

    @Override protected void onCreate(Bundle state) {
        super.onCreate(state);
        receipts = new SqliteReceiptStore(getApplicationContext());
        catalog = new SqliteProductCatalogStore(getApplicationContext());
        service = new ProductDetailServiceV1(
                catalog, catalog, new PriceIntelligenceServiceV2(receipts, catalog, catalog));

        LinearLayout outer = new LinearLayout(this);
        outer.setOrientation(LinearLayout.VERTICAL);
        outer.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL);
        UiKitV1.applyPage(this, outer);

        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        page = new LinearLayout(this);
        page.setOrientation(LinearLayout.VERTICAL);
        page.setPadding(0, 0, 0, dp(DesignTokensV1.SPACE_8_DP));
        scroll.addView(page, new ScrollView.LayoutParams(
                contentWidthPx(), ScrollView.LayoutParams.WRAP_CONTENT, Gravity.TOP | Gravity.CENTER_HORIZONTAL));
        outer.addView(scroll, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f));
        setContentView(outer);
        SystemBarInsetHelper.apply(this, outer);

        showLoading();
        load();
    }

    private void load() {
        String id = getIntent().getStringExtra(EXTRA_PRODUCT_ID);
        if (id == null || id.trim().isEmpty()) {
            showError(getString(R.string.product_detail_missing));
            return;
        }
        long ticket = ++generation;
        worker.execute(() -> {
            try {
                ProductDetailV1 detail = service.load(id);
                runOnUiThread(() -> { if (ticket == generation) render(detail); });
            } catch (Exception ignored) {
                runOnUiThread(() -> { if (ticket == generation) showError(getString(R.string.product_detail_load_failed)); });
            }
        });
    }

    private void showLoading() {
        page.removeAllViews();
        addTopBar();
        LinearLayout card = surface();
        card.addView(UiKitV1.sectionTitle(this, getString(R.string.product_detail_loading)));
        TextView body = smallBody(getString(R.string.product_detail_loading_body));
        body.setPadding(0, dp(DesignTokensV1.SPACE_2_DP), 0, 0);
        card.addView(body);
        addBlock(page, card, DesignTokensV1.SPACE_4_DP);
    }

    private void showError(String message) {
        page.removeAllViews();
        addTopBar();
        addBlock(page, UiKitV1.semanticCard(this, SemanticPresentationV1.display(
                getString(R.string.product_detail_unavailable), message, SemanticToneV1.ERROR)),
                DesignTokensV1.SPACE_4_DP);
    }

    private void render(ProductDetailV1 detail) {
        page.removeAllViews();
        addTopBar();
        if (ResponsiveLayoutPolicyV1.twoPaneEligible(widthDp(), heightDp())) {
            LinearLayout panes = new LinearLayout(this);
            panes.setOrientation(LinearLayout.HORIZONTAL);
            panes.setGravity(Gravity.TOP);
            LinearLayout left = column();
            LinearLayout right = column();
            renderSummary(detail, left);
            renderHistory(detail, right);
            LinearLayout.LayoutParams leftLp = new LinearLayout.LayoutParams(0, -2, 0.46f);
            leftLp.setMarginEnd(dp(DesignTokensV1.SPACE_6_DP));
            panes.addView(left, leftLp);
            panes.addView(right, new LinearLayout.LayoutParams(0, -2, 0.54f));
            page.addView(panes, new LinearLayout.LayoutParams(-1, -2));
        } else {
            renderSummary(detail, page);
            renderHistory(detail, page);
        }
    }

    private void renderSummary(ProductDetailV1 detail, LinearLayout host) {
        LinearLayout identity = column();
        identity.setPadding(0, dp(DesignTokensV1.SPACE_3_DP), 0, 0);
        String brand = ProductDetailFormatterV1.brand(detail);
        if (!brand.isEmpty()) {
            TextView brandView = label(brand);
            brandView.setTextColor(DesignTokensV1.COLOR_PRIMARY);
            identity.addView(brandView);
        }
        TextView name = new TextView(this);
        name.setText(ProductDetailFormatterV1.primaryName(detail));
        UiKitV1.styleText(name, DesignTokensV1.TextRole.TITLE_LARGE, DesignTokensV1.COLOR_TEXT_PRIMARY);
        identity.addView(name);
        String support = joinSupport(
                ProductDetailFormatterV1.variant(detail), ProductDetailFormatterV1.specification(detail));
        if (!support.isEmpty()) {
            TextView supportView = smallBody(support);
            supportView.setPadding(0, dp(DesignTokensV1.SPACE_1_DP), 0, 0);
            identity.addView(supportView);
        }
        addBlock(host, identity, DesignTokensV1.SPACE_3_DP);

        LinearLayout hero = surface();
        hero.addView(label(getString(R.string.product_detail_latest_price)));
        TextView price = new TextView(this);
        price.setText(ProductDetailFormatterV1.formatWon(detail.evaluation.latestPriceMinor));
        UiKitV1.styleText(price, DesignTokensV1.TextRole.PRICE_HERO, DesignTokensV1.COLOR_TEXT_PRIMARY);
        price.setPadding(0, dp(DesignTokensV1.SPACE_1_DP), 0, 0);
        hero.addView(price);
        hero.addView(smallBody(getString(R.string.product_detail_standard_basis)));
        TextView context = smallBody(ProductDetailFormatterV1.latestContext(detail));
        context.setPadding(0, dp(DesignTokensV1.SPACE_3_DP), 0, 0);
        hero.addView(context);
        addBlock(host, hero, DesignTokensV1.SPACE_3_DP);

        SemanticPresentationV1.Presentation state = SemanticPresentationV1.price(detail.evaluation);
        LinearLayout evaluation = UiKitV1.semanticCard(this, state);
        TextView evidence = new TextView(this);
        evidence.setText(ProductDetailFormatterV1.evaluationEvidence(detail.evaluation));
        UiKitV1.styleText(evidence, DesignTokensV1.TextRole.BODY_MEDIUM, state.tone.foregroundArgb);
        evidence.setPadding(0, dp(DesignTokensV1.SPACE_2_DP), 0, 0);
        evaluation.addView(evidence);
        addBlock(host, evaluation, DesignTokensV1.SPACE_3_DP);

        LinearLayout metrics = surface();
        metrics.setOrientation(LinearLayout.HORIZONTAL);
        metrics.addView(metric(
                getString(R.string.product_detail_previous_price),
                detail.evaluation.previousPriceMinor == null
                        ? getString(R.string.product_detail_not_enough)
                        : ProductDetailFormatterV1.formatWon(detail.evaluation.previousPriceMinor)),
                new LinearLayout.LayoutParams(0, -2, 1f));
        View separator = divider();
        LinearLayout.LayoutParams separatorLp = new LinearLayout.LayoutParams(dp(1), dp(52));
        separatorLp.setMargins(dp(DesignTokensV1.SPACE_4_DP), 0, dp(DesignTokensV1.SPACE_4_DP), 0);
        metrics.addView(separator, separatorLp);
        metrics.addView(metric(
                getString(R.string.product_detail_usual_price),
                detail.evaluation.usualPriceMinor == null
                        ? getString(R.string.product_detail_not_enough)
                        : ProductDetailFormatterV1.formatWon(detail.evaluation.usualPriceMinor)),
                new LinearLayout.LayoutParams(0, -2, 1f));
        addBlock(host, metrics, DesignTokensV1.SPACE_4_DP);
    }

    private void renderHistory(ProductDetailV1 detail, LinearLayout host) {
        addBlock(host, UiKitV1.sectionTitle(this, getString(R.string.product_detail_price_trend)),
                DesignTokensV1.SPACE_2_DP);
        LinearLayout chartCard = surface();
        chartCard.addView(smallBody(getString(
                R.string.product_detail_price_trend_meta, detail.comparablePurchases().size())));
        ProductPriceChartViewV1 chart = new ProductPriceChartViewV1(this);
        chart.setDetail(detail);
        chartCard.addView(chart, new LinearLayout.LayoutParams(-1, dp(ProductPriceChartViewV1.RECOMMENDED_HEIGHT_DP)));
        addBlock(host, chartCard, DesignTokensV1.SPACE_4_DP);

        addBlock(host, UiKitV1.sectionTitle(this, getString(R.string.product_detail_purchase_history)),
                DesignTokensV1.SPACE_2_DP);
        LinearLayout history = surface();
        if (detail.purchases.isEmpty()) {
            history.addView(smallBody(getString(R.string.product_detail_history_empty)));
        } else {
            for (int i = 0; i < detail.purchases.size(); i++) {
                ProductDetailV1.PurchaseRow row = detail.purchases.get(i);
                history.addView(historyRow(row), new LinearLayout.LayoutParams(-1, -2));
                if (i + 1 < detail.purchases.size()) {
                    history.addView(divider(), new LinearLayout.LayoutParams(-1, dp(1)));
                }
            }
        }
        addBlock(host, history, DesignTokensV1.SPACE_4_DP);
    }

    private void addTopBar() {
        LinearLayout top = new LinearLayout(this);
        top.setOrientation(LinearLayout.HORIZONTAL);
        top.setGravity(Gravity.CENTER_VERTICAL);
        Button back = UiKitV1.button(this, R.string.product_detail_back, v -> finish(), UiKitV1.ButtonTone.SECONDARY);
        TextView title = UiKitV1.title(this, R.string.product_detail_title);
        title.setPadding(dp(DesignTokensV1.SPACE_3_DP), 0, 0, 0);
        top.addView(back, new LinearLayout.LayoutParams(-2, -2));
        top.addView(title, new LinearLayout.LayoutParams(0, -2, 1f));
        page.addView(top, new LinearLayout.LayoutParams(-1, -2));
    }

    private LinearLayout historyRow(ProductDetailV1.PurchaseRow row) {
        LinearLayout item = column();
        item.setGravity(Gravity.CENTER_VERTICAL);
        item.setMinimumHeight(dp(64));
        int vertical = dp(DesignTokensV1.SPACE_3_DP);
        item.setPadding(0, vertical, 0, vertical);
        item.setClickable(true);
        item.setFocusable(true);
        int selectable = selectableBackground();
        if (selectable != 0) item.setBackgroundResource(selectable);
        item.addView(UiKitV1.body(this, ProductDetailFormatterV1.purchaseTitle(row)));
        TextView subtitle = new TextView(this);
        subtitle.setText(ProductDetailFormatterV1.purchaseSubtitle(row));
        UiKitV1.styleText(subtitle, DesignTokensV1.TextRole.BODY_MEDIUM,
                row.comparable ? DesignTokensV1.COLOR_TEXT_SECONDARY : DesignTokensV1.COLOR_REVIEW_TEXT);
        subtitle.setPadding(0, dp(DesignTokensV1.SPACE_1_DP), 0, 0);
        item.addView(subtitle);
        item.setContentDescription(ProductDetailFormatterV1.purchaseTitle(row) + ", "
                + ProductDetailFormatterV1.purchaseSubtitle(row) + ", 영수증 보기");
        item.setOnClickListener(v -> {
            Intent intent = new Intent(this, ReceiptDetailActivity.class);
            intent.putExtra(ReceiptDetailActivity.EXTRA_ID, row.receiptId);
            startActivity(intent);
        });
        return item;
    }

    private LinearLayout metric(String title, String value) {
        LinearLayout box = column();
        box.addView(label(title));
        TextView amount = new TextView(this);
        amount.setText(value);
        UiKitV1.styleText(amount, DesignTokensV1.TextRole.TITLE_MEDIUM, DesignTokensV1.COLOR_TEXT_PRIMARY);
        amount.setPadding(0, dp(DesignTokensV1.SPACE_1_DP), 0, 0);
        box.addView(amount);
        return box;
    }

    private LinearLayout surface() {
        LinearLayout card = column();
        int pad = dp(DesignTokensV1.SPACE_4_DP);
        card.setPadding(pad, pad, pad, pad);
        GradientDrawable bg = new GradientDrawable();
        bg.setColor(DesignTokensV1.COLOR_SURFACE);
        bg.setCornerRadius(dp(DesignTokensV1.RADIUS_LARGE_DP));
        bg.setStroke(dp(1), DesignTokensV1.COLOR_BORDER);
        card.setBackground(bg);
        card.setElevation(dp(DesignTokensV1.ELEVATION_CARD_DP));
        return card;
    }

    private LinearLayout column() {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        return layout;
    }

    private TextView label(String text) {
        TextView view = new TextView(this);
        view.setText(text);
        UiKitV1.styleText(view, DesignTokensV1.TextRole.LABEL, DesignTokensV1.COLOR_TEXT_SECONDARY);
        return view;
    }

    private TextView smallBody(String text) {
        TextView view = new TextView(this);
        view.setText(text);
        UiKitV1.styleText(view, DesignTokensV1.TextRole.BODY_MEDIUM, DesignTokensV1.COLOR_TEXT_SECONDARY);
        return view;
    }

    private View divider() {
        View view = new View(this);
        view.setBackgroundColor(DesignTokensV1.COLOR_BORDER);
        return view;
    }

    private void addBlock(LinearLayout host, View child, int bottomDp) {
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(-1, -2);
        lp.bottomMargin = dp(bottomDp);
        host.addView(child, lp);
    }

    private int contentWidthPx() {
        int gutter = ResponsiveLayoutPolicyV1.pageGutterDp(widthDp());
        int available = Math.max(1, widthDp() - gutter * 2);
        return dp(Math.min(available, ResponsiveLayoutPolicyV1.contentMaxWidthDp()));
    }

    private int widthDp() {
        int value = getResources().getConfiguration().screenWidthDp;
        return value > 0 ? value : Math.max(1, Math.round(
                getResources().getDisplayMetrics().widthPixels / getResources().getDisplayMetrics().density));
    }

    private int heightDp() {
        int value = getResources().getConfiguration().screenHeightDp;
        return value > 0 ? value : Math.max(1, Math.round(
                getResources().getDisplayMetrics().heightPixels / getResources().getDisplayMetrics().density));
    }

    private int selectableBackground() {
        TypedValue out = new TypedValue();
        return getTheme().resolveAttribute(android.R.attr.selectableItemBackground, out, true) ? out.resourceId : 0;
    }

    private int dp(int value) { return UiKitV1.dp(this, value); }

    private static String joinSupport(String a, String b) {
        String left = a == null ? "" : a.trim();
        String right = b == null ? "" : b.trim();
        if (left.isEmpty()) return right;
        if (right.isEmpty()) return left;
        return left + " · " + right;
    }

    @Override protected void onDestroy() {
        generation++;
        worker.shutdownNow();
        catalog.close();
        receipts.close();
        super.onDestroy();
    }
}
