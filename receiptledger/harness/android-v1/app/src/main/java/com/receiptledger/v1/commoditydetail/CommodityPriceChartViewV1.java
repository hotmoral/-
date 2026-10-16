package com.receiptledger.v1.commoditydetail;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Path;
import android.util.AttributeSet;
import android.util.TypedValue;
import android.view.View;
import com.receiptledger.v1.design.ChartGrammarV1;
import com.receiptledger.v1.design.DesignTokensV1;
import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.priceintel.ComparisonBasisV2;
import com.receiptledger.v1.priceintel.PriceObservationV2;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** CP32 strict-basis purchase-history chart. Contextual LIKE_FORM is intentionally not rendered here. */
public final class CommodityPriceChartViewV1 extends View {
    public static final int RECOMMENDED_HEIGHT_DP = 220;

    private final Paint grid = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint line = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint point = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint latestPoint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint usual = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint text = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Path linePath = new Path();
    private List<PriceObservationV2> points = Collections.emptyList();
    private PriceEvaluationV1 evaluation;
    private String axisLabel = "";
    private String usualLabel = "";
    private String firstDate = "";
    private String lastDate = "";

    public CommodityPriceChartViewV1(Context context) { super(context); init(); }
    public CommodityPriceChartViewV1(Context context, AttributeSet attrs) { super(context, attrs); init(); }

    private void init() {
        setImportantForAccessibility(IMPORTANT_FOR_ACCESSIBILITY_YES);
        grid.setColor(DesignTokensV1.COLOR_BORDER);
        grid.setStrokeWidth(dp(1));
        line.setColor(DesignTokensV1.COLOR_PRIMARY);
        line.setStyle(Paint.Style.STROKE);
        line.setStrokeWidth(dp(2));
        line.setStrokeCap(Paint.Cap.ROUND);
        line.setStrokeJoin(Paint.Join.ROUND);
        point.setColor(DesignTokensV1.COLOR_PRIMARY);
        point.setStyle(Paint.Style.FILL);
        latestPoint.setStyle(Paint.Style.FILL);
        usual.setColor(DesignTokensV1.COLOR_TEXT_SECONDARY);
        usual.setStyle(Paint.Style.STROKE);
        usual.setStrokeWidth(dp(1));
        text.setColor(DesignTokensV1.COLOR_TEXT_SECONDARY);
        text.setTextSize(sp(12));
    }

    public void setSection(CommodityDetailV1.BasisSection section) {
        if (section == null || !section.isStrict()) throw new IllegalArgumentException("strict section required");
        if (section.cohort.observations.isEmpty()) throw new IllegalArgumentException("chart observations");
        List<ComparisonBasisV2> bases = new ArrayList<>();
        List<PriceObservationV2> rows = new ArrayList<>();
        for (PriceObservationV2 row : section.cohort.observations) {
            if (!row.isEligible() || row.comparisonPriceMinor == null) continue;
            bases.add(row.basis);
            rows.add(row);
        }
        ChartGrammarV1.requireSingleBasis(bases);
        Collections.reverse(rows);
        points = Collections.unmodifiableList(rows);
        evaluation = section.evaluation;
        axisLabel = ChartGrammarV1.axisLabelKo(section.cohort.basis);
        usualLabel = evaluation.usualPriceMinor == null ? "" : "평소 "
                + CommodityDetailFormatterV1.formatRate(evaluation.usualPriceMinor, section.cohort.basis);
        firstDate = points.isEmpty() ? "" : shortDate(points.get(0).purchaseDate);
        lastDate = points.isEmpty() ? "" : shortDate(points.get(points.size() - 1).purchaseDate);
        latestPoint.setColor(latestColor(evaluation));
        setContentDescription(CommodityDetailFormatterV1.chartAccessibilitySummary(section));
        invalidate();
    }

    @Override protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        int desired = dp(RECOMMENDED_HEIGHT_DP);
        setMeasuredDimension(resolveSize(getSuggestedMinimumWidth(), widthMeasureSpec), resolveSize(desired, heightMeasureSpec));
    }

    @Override protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        int w = getWidth();
        int h = getHeight();
        if (w <= 0 || h <= 0) return;

        float left = dp(8), right = Math.max(left + 1, w - dp(8));
        float top = dp(22), bottom = Math.max(top + 1, h - dp(28));
        text.setTextAlign(Paint.Align.LEFT);
        canvas.drawText(axisLabel, left, text.getTextSize(), text);
        canvas.drawLine(left, bottom, right, bottom, grid);
        if (points.isEmpty()) {
            text.setTextAlign(Paint.Align.CENTER);
            canvas.drawText("비교 가능한 구매 기록이 없습니다", w / 2f, h / 2f, text);
            return;
        }

        BigDecimal min = points.get(0).comparisonPriceMinor;
        BigDecimal max = min;
        for (PriceObservationV2 row : points) {
            if (row.comparisonPriceMinor.compareTo(min) < 0) min = row.comparisonPriceMinor;
            if (row.comparisonPriceMinor.compareTo(max) > 0) max = row.comparisonPriceMinor;
        }
        if (evaluation != null && ChartGrammarV1.showUsualPriceReference(evaluation.status)
                && evaluation.usualPriceMinor != null) {
            if (evaluation.usualPriceMinor.compareTo(min) < 0) min = evaluation.usualPriceMinor;
            if (evaluation.usualPriceMinor.compareTo(max) > 0) max = evaluation.usualPriceMinor;
        }

        double lo = min.doubleValue(), hi = max.doubleValue();
        double spread = hi - lo;
        if (spread <= 0d) spread = Math.max(100d, Math.abs(hi) * 0.08d);
        double padding = spread * 0.14d;
        lo -= padding;
        hi += padding;

        for (int i = 1; i <= 2; i++) {
            float y = top + (bottom - top) * i / 3f;
            canvas.drawLine(left, y, right, y, grid);
        }

        if (evaluation != null && ChartGrammarV1.showUsualPriceReference(evaluation.status)
                && evaluation.usualPriceMinor != null) {
            float y = y(evaluation.usualPriceMinor.doubleValue(), lo, hi, top, bottom);
            canvas.drawLine(left, y, right, y, usual);
            text.setTextAlign(Paint.Align.RIGHT);
            canvas.drawText(usualLabel, right, Math.max(top + text.getTextSize(), y - dp(4)), text);
        }

        linePath.reset();
        for (int i = 0; i < points.size(); i++) {
            float x = x(i, points.size(), left, right);
            float y = y(points.get(i).comparisonPriceMinor.doubleValue(), lo, hi, top, bottom);
            if (i == 0) linePath.moveTo(x, y); else linePath.lineTo(x, y);
        }
        if (points.size() > 1) canvas.drawPath(linePath, line);

        for (int i = 0; i < points.size(); i++) {
            float x = x(i, points.size(), left, right);
            float y = y(points.get(i).comparisonPriceMinor.doubleValue(), lo, hi, top, bottom);
            boolean latest = i == points.size() - 1;
            canvas.drawCircle(x, y, dp(latest ? 5 : 3), latest ? latestPoint : point);
        }

        text.setTextAlign(Paint.Align.LEFT);
        canvas.drawText(firstDate, left, h - dp(6), text);
        if (points.size() > 1) {
            text.setTextAlign(Paint.Align.RIGHT);
            canvas.drawText(lastDate, right, h - dp(6), text);
        }
    }

    private int latestColor(PriceEvaluationV1 e) {
        if (e == null || !ChartGrammarV1.allowJudgmentColor(e.status)) return DesignTokensV1.COLOR_PRIMARY;
        switch (e.judgment) {
            case VERY_CHEAP:
            case CHEAP: return DesignTokensV1.COLOR_POSITIVE_TEXT;
            case EXPENSIVE:
            case VERY_EXPENSIVE: return DesignTokensV1.COLOR_NEGATIVE_TEXT;
            default: return DesignTokensV1.COLOR_PRIMARY;
        }
    }

    private static float x(int index, int count, float left, float right) {
        return count <= 1 ? (left + right) / 2f : left + (right - left) * index / (count - 1f);
    }

    private static float y(double value, double lo, double hi, float top, float bottom) {
        return (float) (bottom - ((value - lo) / (hi - lo)) * (bottom - top));
    }

    private static String shortDate(String date) {
        String value = date == null ? "" : date.trim();
        if (value.length() >= 10) return value.substring(5, 10).replace('-', '.');
        return value.isEmpty() ? "날짜 미상" : value;
    }

    private int dp(float value) {
        return Math.round(TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, value, getResources().getDisplayMetrics()));
    }

    private float sp(float value) {
        return TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_SP, value, getResources().getDisplayMetrics());
    }
}
