package com.receiptledger.v1.review;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.text.InputType;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;
import com.receiptledger.v1.R;
import com.receiptledger.v1.design.DesignTokensV1;
import com.receiptledger.v1.design.UiKitV1;
import com.receiptledger.v1.item.ItemResolution;
import com.receiptledger.v1.item.ValueOrigin;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** CP33 selective/full receipt review dialog backed by the frozen ReceiptReviewEngine. */
public final class ReceiptReviewDialog {
    public interface Callback { void onApplied(ReceiptRecord reviewed); }

    private ReceiptReviewDialog() {}

    /** Compatibility entry: full edit remains available. */
    public static void show(Activity activity, ReceiptRecord base, Callback callback) {
        showAll(activity, base, CaptureReviewAssessmentV2.assess(base), callback);
    }

    public static void showRequired(
            Activity activity,
            ReceiptRecord base,
            CaptureReviewAssessmentV2 assessment,
            Callback callback) {
        if (assessment == null) assessment = CaptureReviewAssessmentV2.assess(base);
        if (assessment.receiptFields.isEmpty() && assessment.itemOrdinals.isEmpty()) {
            showInternal(activity, base, assessment, true, callback);
            return;
        }
        showInternal(activity, base, assessment, false, callback);
    }

    public static void showAll(
            Activity activity,
            ReceiptRecord base,
            CaptureReviewAssessmentV2 assessment,
            Callback callback) {
        showInternal(activity, base,
                assessment == null ? CaptureReviewAssessmentV2.assess(base) : assessment,
                true,
                callback);
    }

    private static void showInternal(
            Activity activity,
            ReceiptRecord base,
            CaptureReviewAssessmentV2 assessment,
            boolean all,
            Callback callback) {
        if (activity == null || base == null || callback == null) throw new IllegalArgumentException("review dialog");
        ReceiptReviewEngine engine = new ReceiptReviewEngine();
        int pad = UiKitV1.dp(activity, DesignTokensV1.SPACE_4_DP);
        LinearLayout form = new LinearLayout(activity);
        form.setOrientation(LinearLayout.VERTICAL);
        form.setPadding(pad, pad, pad, pad);

        TextView help = UiKitV1.body(activity, activity.getString(
                all ? R.string.review_help_all : R.string.review_help_required));
        form.addView(help, new LinearLayout.LayoutParams(-1, -2));

        EditText store = null;
        EditText date = null;
        EditText total = null;
        EditText discount = null;
        if (all || assessment.flags(CaptureReviewAssessmentV2.ReceiptField.STORE)) {
            store = field(activity, R.string.review_store_hint, base.storeName, false);
            form.addView(store);
        }
        if (all || assessment.flags(CaptureReviewAssessmentV2.ReceiptField.PURCHASE_DATE)) {
            date = field(activity, R.string.review_date_hint, base.purchaseDate, false);
            form.addView(date);
        }
        if (all || assessment.flags(CaptureReviewAssessmentV2.ReceiptField.PRINTED_TOTAL)) {
            total = field(activity, R.string.review_total_hint, fmt(base.printedTotal), true);
            form.addView(total);
        }
        if (all || assessment.flags(CaptureReviewAssessmentV2.ReceiptField.DISCOUNT_SUM)) {
            discount = field(activity, R.string.review_discount_hint, fmt(base.discountSum), true);
            form.addView(discount);
        }

        Map<Integer, RowFields> rows = new LinkedHashMap<>();
        for (PersistedItem item : base.items) {
            if (!all && !assessment.flagsItem(item.ordinal)) continue;
            TextView label = UiKitV1.sectionTitle(activity,
                    activity.getString(R.string.review_item_label, item.ordinal + 1, itemStatus(activity, item)));
            label.setPadding(0, pad, 0, UiKitV1.dp(activity, DesignTokensV1.SPACE_2_DP));
            form.addView(label);
            EditText name = field(activity, R.string.review_item_name_hint, item.name, false);
            EditText quantity = field(activity, R.string.review_quantity_hint, fmt(item.quantity), true);
            EditText unit = field(activity, R.string.review_unit_price_hint, fmt(item.unitPrice), true);
            EditText amount = field(activity, R.string.review_line_amount_hint, fmt(item.lineAmount), true);
            form.addView(name);
            form.addView(quantity);
            form.addView(unit);
            form.addView(amount);
            rows.put(item.ordinal, new RowFields(name, quantity, unit, amount));
        }

        ScrollView scroll = new ScrollView(activity);
        scroll.addView(form);
        AlertDialog dialog = new AlertDialog.Builder(activity)
                .setTitle(all ? R.string.review_title_all : R.string.review_title_required)
                .setView(scroll)
                .setNegativeButton(android.R.string.cancel, null)
                .setPositiveButton(R.string.apply_review, null)
                .create();

        final EditText storeField = store;
        final EditText dateField = date;
        final EditText totalField = total;
        final EditText discountField = discount;
        dialog.setOnShowListener(ignored -> dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener(v -> {
            try {
                String storeValue = storeField == null ? base.storeName : storeField.getText().toString();
                String dateValue = dateField == null
                        ? base.purchaseDate
                        : ReviewInputParser.nullableDate(dateField.getText().toString());
                Long totalValue = totalField == null
                        ? base.printedTotal
                        : ReviewInputParser.nullableMoney(totalField.getText().toString());
                Long discountValue = discountField == null
                        ? base.discountSum
                        : ReviewInputParser.nullableMoney(discountField.getText().toString());
                List<ReviewItemInput> edits = new ArrayList<>();
                for (PersistedItem item : base.items) {
                    RowFields row = rows.get(item.ordinal);
                    if (row == null) {
                        edits.add(new ReviewItemInput(item.name, item.quantity, item.unitPrice, item.lineAmount));
                    } else {
                        edits.add(new ReviewItemInput(
                                row.name.getText().toString(),
                                ReviewInputParser.nullableQuantity(row.quantity.getText().toString()),
                                ReviewInputParser.nullableMoney(row.unit.getText().toString()),
                                ReviewInputParser.nullableMoney(row.amount.getText().toString())));
                    }
                }
                ReceiptRecord reviewed = engine.apply(
                        base, storeValue, dateValue, totalValue, discountValue, edits);
                reviewed = CaptureReviewConfirmationV2.apply(reviewed, assessment);
                callback.onApplied(reviewed);
                dialog.dismiss();
            } catch (IllegalArgumentException e) {
                Toast.makeText(activity, e.getMessage(), Toast.LENGTH_LONG).show();
            }
        }));
        dialog.show();
    }

    private static EditText field(Context context, int hintRes, Object value, boolean number) {
        EditText field = new EditText(context);
        field.setHint(hintRes);
        field.setSingleLine(true);
        field.setMinHeight(UiKitV1.dp(context, DesignTokensV1.TOUCH_TARGET_MIN_DP));
        UiKitV1.styleText(field, DesignTokensV1.TextRole.BODY_LARGE, DesignTokensV1.COLOR_TEXT_PRIMARY);
        if (value != null) field.setText(String.valueOf(value));
        if (number) field.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_FLAG_SIGNED);
        return field;
    }

    private static String itemStatus(Context context, PersistedItem item) {
        if (item.resolution == ItemResolution.PARTIAL) return context.getString(R.string.review_item_required);
        if (item.quantityOrigin == ValueOrigin.DEFAULT_ONE) return context.getString(R.string.review_item_quantity_assumed);
        if (item.resolution == ItemResolution.INFERRED) return context.getString(R.string.review_item_calculated);
        return context.getString(R.string.review_item_auto);
    }

    private static String fmt(Object value) {
        return value == null ? "" : String.valueOf(value);
    }

    private static final class RowFields {
        final EditText name;
        final EditText quantity;
        final EditText unit;
        final EditText amount;
        RowFields(EditText name, EditText quantity, EditText unit, EditText amount) {
            this.name = name;
            this.quantity = quantity;
            this.unit = unit;
            this.amount = amount;
        }
    }
}
