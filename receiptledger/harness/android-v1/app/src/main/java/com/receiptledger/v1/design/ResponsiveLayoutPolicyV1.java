package com.receiptledger.v1.design;

/** View-toolkit-compatible adaptive policy mirroring Android width-class breakpoints. */
public final class ResponsiveLayoutPolicyV1 {
    public enum WidthClass { COMPACT, MEDIUM, EXPANDED }

    private ResponsiveLayoutPolicyV1() {}

    public static WidthClass widthClass(int widthDp) {
        if (widthDp < 1) throw new IllegalArgumentException("widthDp");
        if (widthDp < 600) return WidthClass.COMPACT;
        if (widthDp < 840) return WidthClass.MEDIUM;
        return WidthClass.EXPANDED;
    }

    public static int pageGutterDp(int widthDp) {
        return widthClass(widthDp) == WidthClass.COMPACT
                ? DesignTokensV1.SPACE_4_DP
                : DesignTokensV1.SPACE_6_DP;
    }

    public static int contentMaxWidthDp() {
        return DesignTokensV1.CONTENT_MAX_WIDTH_DP;
    }

    /** Avoid dual pane when height is compact even if width is expanded. */
    public static boolean twoPaneEligible(int widthDp, int heightDp) {
        if (heightDp < 1) throw new IllegalArgumentException("heightDp");
        return widthClass(widthDp) == WidthClass.EXPANDED && heightDp >= 480;
    }
}
