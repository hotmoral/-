package com.receiptledger.v1.design;

import android.content.Context;
import android.content.res.ColorStateList;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

/** Small View-toolkit adapter for the CP30 foundation. No domain logic belongs here. */
public final class UiKitV1 {
    public enum ButtonTone { PRIMARY, SECONDARY, DESTRUCTIVE }

    private UiKitV1() {}

    public static void applyPage(Context context, LinearLayout root) {
        int widthDp = context.getResources().getConfiguration().screenWidthDp;
        if (widthDp < 1) {
            float density = context.getResources().getDisplayMetrics().density;
            widthDp = Math.max(1, Math.round(context.getResources().getDisplayMetrics().widthPixels / density));
        }
        int gutter = dp(context, ResponsiveLayoutPolicyV1.pageGutterDp(widthDp));
        root.setPadding(gutter, gutter, gutter, gutter);
        root.setBackgroundColor(DesignTokensV1.COLOR_BACKGROUND);
    }

    public static TextView title(Context context, int textRes) {
        TextView view = new TextView(context);
        view.setText(textRes);
        styleText(view, DesignTokensV1.TextRole.TITLE_LARGE, DesignTokensV1.COLOR_TEXT_PRIMARY);
        view.setPadding(0, 0, 0, dp(context, DesignTokensV1.SPACE_3_DP));
        return view;
    }

    public static TextView sectionTitle(Context context, CharSequence text) {
        TextView view = new TextView(context);
        view.setText(text);
        styleText(view, DesignTokensV1.TextRole.TITLE_MEDIUM, DesignTokensV1.COLOR_TEXT_PRIMARY);
        return view;
    }

    public static TextView body(Context context, CharSequence text) {
        TextView view = new TextView(context);
        view.setText(text);
        styleText(view, DesignTokensV1.TextRole.BODY_LARGE, DesignTokensV1.COLOR_TEXT_PRIMARY);
        return view;
    }

    public static TextView status(Context context) {
        TextView view = new TextView(context);
        styleText(view, DesignTokensV1.TextRole.BODY_MEDIUM, DesignTokensV1.COLOR_TEXT_SECONDARY);
        view.setPadding(0, dp(context, DesignTokensV1.SPACE_2_DP), 0, dp(context, DesignTokensV1.SPACE_2_DP));
        return view;
    }

    public static Button button(Context context, int textRes, View.OnClickListener listener, ButtonTone tone) {
        Button button = new Button(context);
        button.setText(textRes);
        configureButton(context, button, listener, tone);
        return button;
    }

    public static Button listRow(Context context, CharSequence text, View.OnClickListener listener) {
        Button button = new Button(context);
        button.setText(text);
        configureButton(context, button, listener, ButtonTone.SECONDARY);
        button.setGravity(Gravity.START | Gravity.CENTER_VERTICAL);
        button.setMinHeight(dp(context, DesignTokensV1.LIST_ROW_MIN_DP));
        return button;
    }

    public static EditText searchField(Context context, CharSequence hint) {
        EditText field = new EditText(context);
        field.setHint(hint);
        field.setSingleLine(true);
        field.setMinHeight(dp(context, DesignTokensV1.TOUCH_TARGET_MIN_DP));
        styleText(field, DesignTokensV1.TextRole.BODY_LARGE, DesignTokensV1.COLOR_TEXT_PRIMARY);
        field.setHintTextColor(DesignTokensV1.COLOR_TEXT_SECONDARY);
        field.setBackgroundTintList(ColorStateList.valueOf(DesignTokensV1.COLOR_PRIMARY));
        return field;
    }

    public static Button filterChip(Context context, CharSequence text, boolean selected, View.OnClickListener listener) {
        Button chip = new Button(context);
        chip.setText(text);
        configureButton(context, chip, listener, selected ? ButtonTone.PRIMARY : ButtonTone.SECONDARY);
        return chip;
    }

    public static LinearLayout semanticCard(Context context, SemanticPresentationV1.Presentation presentation) {
        if (presentation == null) throw new IllegalArgumentException("presentation");
        LinearLayout card = new LinearLayout(context);
        card.setOrientation(LinearLayout.VERTICAL);
        int pad = dp(context, DesignTokensV1.SPACE_4_DP);
        card.setPadding(pad, pad, pad, pad);
        card.setBackground(surfaceDrawable(context, presentation.tone.backgroundArgb, DesignTokensV1.RADIUS_MEDIUM_DP));
        card.setElevation(dp(context, 1));
        TextView label = sectionTitle(context, presentation.labelKo);
        label.setTextColor(presentation.tone.foregroundArgb);
        TextView body = body(context, presentation.explanationKo);
        body.setTextColor(presentation.tone.foregroundArgb);
        body.setPadding(0, dp(context, DesignTokensV1.SPACE_1_DP), 0, 0);
        card.addView(label, new LinearLayout.LayoutParams(-1, -2));
        card.addView(body, new LinearLayout.LayoutParams(-1, -2));
        return card;
    }

    public static LinearLayout stateCard(Context context, UiStatePresentationV1 state) {
        if (state == null) throw new IllegalArgumentException("state");
        return semanticCard(context, SemanticPresentationV1.display(state.titleKo, state.bodyKo, state.tone));
    }

    public static void styleText(TextView view, DesignTokensV1.TextRole role, int color) {
        if (view == null || role == null) throw new IllegalArgumentException("text style");
        view.setTextSize(TypedValue.COMPLEX_UNIT_SP, role.sizeSp);
        view.setTextColor(color);
        switch (role.weight) {
            case BOLD:
                view.setTypeface(Typeface.create("sans-serif", Typeface.BOLD));
                break;
            case MEDIUM:
                view.setTypeface(Typeface.create("sans-serif-medium", Typeface.NORMAL));
                break;
            case NORMAL:
            default:
                view.setTypeface(Typeface.create("sans-serif", Typeface.NORMAL));
                break;
        }
    }

    public static int dp(Context context, int valueDp) {
        return Math.round(valueDp * context.getResources().getDisplayMetrics().density);
    }

    private static void configureButton(Context context, Button button, View.OnClickListener listener, ButtonTone tone) {
        if (tone == null) throw new IllegalArgumentException("tone");
        button.setAllCaps(false);
        button.setOnClickListener(listener);
        button.setMinHeight(dp(context, DesignTokensV1.TOUCH_TARGET_MIN_DP));
        button.setGravity(Gravity.CENTER);
        styleText(button, DesignTokensV1.TextRole.LABEL, buttonText(tone));
        button.setBackgroundTintList(ColorStateList.valueOf(buttonBackground(tone)));
        int horizontal = dp(context, DesignTokensV1.SPACE_4_DP);
        int vertical = dp(context, DesignTokensV1.SPACE_2_DP);
        button.setPadding(horizontal, vertical, horizontal, vertical);
    }

    private static int buttonText(ButtonTone tone) {
        switch (tone) {
            case PRIMARY: return DesignTokensV1.COLOR_ON_PRIMARY;
            case DESTRUCTIVE: return DesignTokensV1.COLOR_NEGATIVE_TEXT;
            case SECONDARY:
            default: return DesignTokensV1.COLOR_TEXT_PRIMARY;
        }
    }

    private static int buttonBackground(ButtonTone tone) {
        switch (tone) {
            case PRIMARY: return DesignTokensV1.COLOR_PRIMARY;
            case DESTRUCTIVE: return DesignTokensV1.COLOR_NEGATIVE_BG;
            case SECONDARY:
            default: return DesignTokensV1.COLOR_SURFACE_SUBTLE;
        }
    }

    private static GradientDrawable surfaceDrawable(Context context, int color, int radiusDp) {
        GradientDrawable drawable = new GradientDrawable();
        drawable.setColor(color);
        drawable.setCornerRadius(dp(context, radiusDp));
        return drawable;
    }
}
