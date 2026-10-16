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
import com.receiptledger.v1.commoditydetail.CommodityDetailFormatterV1;
import com.receiptledger.v1.commoditydetail.CommodityDetailServiceV1;
import com.receiptledger.v1.commoditydetail.CommodityDetailV1;
import com.receiptledger.v1.commoditydetail.CommodityPriceChartViewV1;
import com.receiptledger.v1.design.DesignTokensV1;
import com.receiptledger.v1.design.ResponsiveLayoutPolicyV1;
import com.receiptledger.v1.design.SemanticPresentationV1;
import com.receiptledger.v1.design.SemanticToneV1;
import com.receiptledger.v1.design.UiKitV1;
import com.receiptledger.v1.persistence.SqliteReceiptStore;
import com.receiptledger.v1.priceintel.PriceIntelligenceServiceV2;
import com.receiptledger.v1.product.SqliteProductCatalogStore;
import com.receiptledger.v1.ui.SystemBarInsetHelper;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** CP32 commercial NON_STANDARD commodity detail surface. */
public final class CommodityDetailActivity extends Activity {
    public static final String EXTRA_PRODUCT_ID = "product_id";

    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private SqliteReceiptStore receipts;
    private SqliteProductCatalogStore catalog;
    private CommodityDetailServiceV1 service;
    private LinearLayout page;
    private long generation;

    @Override protected void onCreate(Bundle state) {
        super.onCreate(state);
        receipts = new SqliteReceiptStore(getApplicationContext());
        catalog = new SqliteProductCatalogStore(getApplicationContext());
        service = new CommodityDetailServiceV1(
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
        outer.addView(scroll, new LinearLayout.LayoutParams(-1, 0, 1f));
        setContentView(outer);
        SystemBarInsetHelper.apply(this, outer);

        showLoading();
        load();
    }

    private void load() {
        String id = getIntent().getStringExtra(EXTRA_PRODUCT_ID);
        if (id == null || id.trim().isEmpty()) {
            showError(getString(R.string.commodity_detail_missing));
            return;
        }
        long ticket = ++generation;
        worker.execute(() -> {
            try {
                CommodityDetailV1 detail = service.load(id);
                runOnUiThread(() -> { if (ticket == generation) render(detail); });
            } catch (Exception ignored) {
                runOnUiThread(() -> { if (ticket == generation) showError(getString(R.string.commodity_detail_load_failed)); });
            }
        });
    }

    private void showLoading() {
        page.removeAllViews();
        addTopBar();
        LinearLayout card = surface();
        card.addView(UiKitV1.sectionTitle(this, getString(R.string.commodity_detail_loading)));
        TextView body = smallBody(getString(R.string.commodity_detail_loading_body));
        body.setPadding(0, dp(DesignTokensV1.SPACE_2_DP), 0, 0);
        card.addView(body);
        addBlock(page, card, DesignTokensV1.SPACE_4_DP);
    }

    private void showError(String message) {
        page.removeAllViews();
        addTopBar();
        addBlock(page, UiKitV1.semanticCard(this, SemanticPresentationV1.display(
                getString(R.string.commodity_detail_unavailable), message, SemanticToneV1.ERROR)),
                DesignTokensV1.SPACE_4_DP);
    }

    private void render(CommodityDetailV1 detail) {
        page.removeAllViews();
        addTopBar();
        if (ResponsiveLayoutPolicyV1.twoPaneEligible(widthDp(), heightDp())) {
            LinearLayout panes = new LinearLayout(this);
            panes.setOrientation(LinearLayout.HORIZONTAL);
            panes.setGravity(Gravity.TOP);
            LinearLayout left = column();
            LinearLayout right = column();
            renderOverview(detail, left);
            renderComparisons(detail, right);
            renderHistory(detail, right);
            LinearLayout.LayoutParams leftLp = new LinearLayout.LayoutParams(0, -2, 0.42f);
            leftLp.setMarginEnd(dp(DesignTokensV1.SPACE_6_DP));
            panes.addView(left, leftLp);
            panes.addView(right, new LinearLayout.LayoutParams(0, -2, 0.58f));
            page.addView(panes, new LinearLayout.LayoutParams(-1, -2));
        } else {
            renderOverview(detail, page);
            renderComparisons(detail, page);
            renderHistory(detail, page);
        }
    }

    private void renderOverview(CommodityDetailV1 detail, LinearLayout host) {
        LinearLayout identity = column();
        identity.setPadding(0, dp(DesignTokensV1.SPACE_3_DP), 0, 0);
        TextView context = label(getString(R.string.commodity_detail_identity_label));
        context.setTextColor(DesignTokensV1.COLOR_PRIMARY);
        identity.addView(context);
        TextView name = new TextView(this);
        name.setText(CommodityDetailFormatterV1.primaryName(detail));
        UiKitV1.styleText(name, DesignTokensV1.TextRole.TITLE_LARGE, DesignTokensV1.COLOR_TEXT_PRIMARY);
        identity.addView(name);
        TextView rule = smallBody(getString(R.string.commodity_detail_comparison_rule));
        rule.setPadding(0, dp(DesignTokensV1.SPACE_2_DP), 0, 0);
        identity.addView(rule);
        addBlock(host, identity, DesignTokensV1.SPACE_4_DP);

        addBlock(host, UiKitV1.sectionTitle(this, getString(R.string.commodity_detail_latest_purchase)),
                DesignTokensV1.SPACE_2_DP);
        if (detail.latestPurchase == null) {
            addBlock(host, UiKitV1.semanticCard(this, CommodityDetailFormatterV1.latestPresentation(null)),
                    DesignTokensV1.SPACE_4_DP);
            return;
        }

        CommodityDetailV1.PurchaseRow latest = detail.latestPurchase;
        LinearLayout latestCard = surface();
        latestCard.addView(label(CommodityDetailFormatterV1.purchaseAmountLabel(latest)));
        TextView amount = new TextView(this);
        amount.setText(CommodityDetailFormatterV1.purchaseAmount(latest));
        UiKitV1.styleText(amount, DesignTokensV1.TextRole.PRICE_HERO, DesignTokensV1.COLOR_TEXT_PRIMARY);
        amount.setPadding(0, dp(DesignTokensV1.SPACE_1_DP), 0, 0);
        latestCard.addView(amount);
        TextView form = smallBody(CommodityDetailFormatterV1.latestContext(latest));
        form.setPadding(0, dp(DesignTokensV1.SPACE_2_DP), 0, 0);
        latestCard.addView(form);
        SemanticPresentationV1.Presentation p = CommodityDetailFormatterV1.latestPresentation(latest);
        TextView status = new TextView(this);
        status.setText(p.labelKo + " · " + p.explanationKo);
        UiKitV1.styleText(status, DesignTokensV1.TextRole.BODY_MEDIUM, p.tone.foregroundArgb);
        status.setPadding(0, dp(DesignTokensV1.SPACE_3_DP), 0, 0);
        latestCard.addView(status);
        addBlock(host, latestCard, DesignTokensV1.SPACE_4_DP);
    }

    private void renderComparisons(CommodityDetailV1 detail, LinearLayout host) {
        addBlock(host, UiKitV1.sectionTitle(this, getString(R.string.commodity_detail_strict_title)),
                DesignTokensV1.SPACE_2_DP);
        if (detail.strictSections.isEmpty()) {
            addBlock(host, UiKitV1.semanticCard(this, SemanticPresentationV1.display(
                    getString(R.string.commodity_detail_strict_empty_title),
                    getString(R.string.commodity_detail_strict_empty_body),
                    SemanticToneV1.INFO)), DesignTokensV1.SPACE_4_DP);
        } else {
            for (CommodityDetailV1.BasisSection section : detail.strictSections) {
                renderStrictSection(section, host);
            }
        }

        if (!detail.contextualSections.isEmpty()) {
            addBlock(host, UiKitV1.sectionTitle(this, getString(R.string.commodity_detail_contextual_title)),
                    DesignTokensV1.SPACE_2_DP);
            LinearLayout intro = UiKitV1.semanticCard(this, SemanticPresentationV1.display(
                    getString(R.string.commodity_detail_contextual_label),
                    getString(R.string.commodity_detail_contextual_body),
                    SemanticToneV1.INFO));
            addBlock(host, intro, DesignTokensV1.SPACE_3_DP);
            for (CommodityDetailV1.BasisSection section : detail.contextualSections) {
                renderContextualSection(section, host);
            }
        }
    }

    private void renderStrictSection(CommodityDetailV1.BasisSection section, LinearLayout host) {
        TextView sectionTitle = UiKitV1.sectionTitle(this,
                CommodityDetailFormatterV1.basisTitleKo(section.cohort.basis));
        addBlock(host, sectionTitle, DesignTokensV1.SPACE_2_DP);

        LinearLayout hero = surface();
        hero.addView(label(CommodityDetailFormatterV1.basisMeta(section)));
        TextView latest = new TextView(this);
        latest.setText(CommodityDetailFormatterV1.formatRate(section.evaluation.latestPriceMinor, section.cohort.basis));
        UiKitV1.styleText(latest, DesignTokensV1.TextRole.PRICE_HERO, DesignTokensV1.COLOR_TEXT_PRIMARY);
        latest.setPadding(0, dp(DesignTokensV1.SPACE_1_DP), 0, 0);
        hero.addView(latest);
        TextView description = smallBody(CommodityDetailFormatterV1.basisDescriptionKo(section.cohort.basis));
        description.setPadding(0, dp(DesignTokensV1.SPACE_2_DP), 0, 0);
        hero.addView(description);
        TextView context = smallBody(CommodityDetailFormatterV1.sectionLatestContext(section));
        context.setPadding(0, dp(DesignTokensV1.SPACE_2_DP), 0, 0);
        hero.addView(context);
        addBlock(host, hero, DesignTokensV1.SPACE_3_DP);

        SemanticPresentationV1.Presentation state = SemanticPresentationV1.price(section.evaluation);
        LinearLayout evaluation = UiKitV1.semanticCard(this, state);
        TextView evidence = new TextView(this);
        evidence.setText(CommodityDetailFormatterV1.evaluationEvidence(section.evaluation));
        UiKitV1.styleText(evidence, DesignTokensV1.TextRole.BODY_MEDIUM, state.tone.foregroundArgb);
        evidence.setPadding(0, dp(DesignTokensV1.SPACE_2_DP), 0, 0);
        evaluation.addView(evidence);
        addBlock(host, evaluation, DesignTokensV1.SPACE_3_DP);

        LinearLayout metrics = surface();
        metrics.setOrientation(LinearLayout.HORIZONTAL);
        metrics.addView(metric(
                getString(R.string.commodity_detail_previous_price),
                section.evaluation.previousPriceMinor == null
                        ? getString(R.string.commodity_detail_not_enough)
                        : CommodityDetailFormatterV1.formatRate(section.evaluation.previousPriceMinor, section.cohort.basis)),
                new LinearLayout.LayoutParams(0, -2, 1f));
        View separator = divider();
        LinearLayout.LayoutParams separatorLp = new LinearLayout.LayoutParams(dp(1), dp(52));
        separatorLp.setMargins(dp(DesignTokensV1.SPACE_4_DP), 0, dp(DesignTokensV1.SPACE_4_DP), 0);
        metrics.addView(separator, separatorLp);
        metrics.addView(metric(
                getString(R.string.commodity_detail_usual_price),
                section.evaluation.usualPriceMinor == null
                        ? getString(R.string.commodity_detail_not_enough)
                        : CommodityDetailFormatterV1.formatRate(section.evaluation.usualPriceMinor, section.cohort.basis)),
                new LinearLayout.LayoutParams(0, -2, 1f));
        addBlock(host, metrics, DesignTokensV1.SPACE_3_DP);

        LinearLayout chartCard = surface();
        CommodityPriceChartViewV1 chart = new CommodityPriceChartViewV1(this);
        chart.setSection(section);
        chartCard.addView(chart, new LinearLayout.LayoutParams(-1, dp(CommodityPriceChartViewV1.RECOMMENDED_HEIGHT_DP)));
        addBlock(host, chartCard, DesignTokensV1.SPACE_5_DP);
    }

    private void renderContextualSection(CommodityDetailV1.BasisSection section, LinearLayout host) {
        LinearLayout card = surface();
        card.addView(label(CommodityDetailFormatterV1.basisTitleKo(section.cohort.basis)));
        TextView latest = new TextView(this);
        latest.setText(CommodityDetailFormatterV1.formatRate(section.cohort.latest, section.cohort.basis));
        UiKitV1.styleText(latest, DesignTokensV1.TextRole.TITLE_MEDIUM, DesignTokensV1.COLOR_TEXT_PRIMARY);
        latest.setPadding(0, dp(DesignTokensV1.SPACE_1_DP), 0, 0);
        card.addView(latest);
        TextView summary = smallBody(CommodityDetailFormatterV1.contextualSummary(section));
        summary.setPadding(0, dp(DesignTokensV1.SPACE_2_DP), 0, 0);
        card.addView(summary);
        SemanticPresentationV1.Presentation p = SemanticPresentationV1.price(section.evaluation);
        TextView context = new TextView(this);
        context.setText(p.labelKo + " · " + p.explanationKo);
        UiKitV1.styleText(context, DesignTokensV1.TextRole.BODY_MEDIUM, p.tone.foregroundArgb);
        context.setPadding(0, dp(DesignTokensV1.SPACE_3_DP), 0, 0);
        card.addView(context);
        addBlock(host, card, DesignTokensV1.SPACE_3_DP);
    }

    private void renderHistory(CommodityDetailV1 detail, LinearLayout host) {
        addBlock(host, UiKitV1.sectionTitle(this, getString(R.string.commodity_detail_purchase_history)),
                DesignTokensV1.SPACE_2_DP);
        LinearLayout history = surface();
        if (detail.purchases.isEmpty()) {
            history.addView(smallBody(getString(R.string.commodity_detail_history_empty)));
        } else {
            for (int i = 0; i < detail.purchases.size(); i++) {
                CommodityDetailV1.PurchaseRow row = detail.purchases.get(i);
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
        Button back = UiKitV1.button(this, R.string.commodity_detail_back, v -> finish(), UiKitV1.ButtonTone.SECONDARY);
        TextView title = UiKitV1.title(this, R.string.commodity_detail_title);
        title.setPadding(dp(DesignTokensV1.SPACE_3_DP), 0, 0, 0);
        top.addView(back, new LinearLayout.LayoutParams(-2, -2));
        top.addView(title, new LinearLayout.LayoutParams(0, -2, 1f));
        page.addView(top, new LinearLayout.LayoutParams(-1, -2));
    }

    private LinearLayout historyRow(CommodityDetailV1.PurchaseRow row) {
        LinearLayout item = column();
        item.setGravity(Gravity.CENTER_VERTICAL);
        item.setMinimumHeight(dp(64));
        int vertical = dp(DesignTokensV1.SPACE_3_DP);
        item.setPadding(0, vertical, 0, vertical);
        item.setClickable(true);
        item.setFocusable(true);
        int selectable = selectableBackground();
        if (selectable != 0) item.setBackgroundResource(selectable);
        item.addView(UiKitV1.body(this, CommodityDetailFormatterV1.purchaseTitle(row)));
        TextView subtitle = new TextView(this);
        subtitle.setText(CommodityDetailFormatterV1.purchaseSubtitle(row));
        UiKitV1.styleText(subtitle, DesignTokensV1.TextRole.BODY_MEDIUM,
                row.isEligible() ? DesignTokensV1.COLOR_TEXT_SECONDARY : DesignTokensV1.COLOR_REVIEW_TEXT);
        subtitle.setPadding(0, dp(DesignTokensV1.SPACE_1_DP), 0, 0);
        item.addView(subtitle);
        item.setContentDescription(CommodityDetailFormatterV1.purchaseTitle(row) + ", "
                + CommodityDetailFormatterV1.purchaseSubtitle(row) + ", 영수증 보기");
        item.setOnClickListener(v -> {
            Intent intent = new Intent(this, ReceiptDetailActivity.class);
            intent.putExtra(ReceiptDetailActivity.EXTRA_ID, row.observation.receiptId);
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

    @Override protected void onDestroy() {
        generation++;
        worker.shutdownNow();
        catalog.close();
        receipts.close();
        super.onDestroy();
    }
}
