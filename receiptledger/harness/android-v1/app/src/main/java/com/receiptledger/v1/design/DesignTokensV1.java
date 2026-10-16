package com.receiptledger.v1.design;

/** Pure-Java visual tokens. Android rendering adapters must consume these rather than inventing screen-local values. */
public final class DesignTokensV1 {
    private DesignTokensV1() {}

    public static final int COLOR_BACKGROUND = 0xFFF7F8FA;
    public static final int COLOR_SURFACE = 0xFFFFFFFF;
    public static final int COLOR_SURFACE_SUBTLE = 0xFFF1F3F5;
    public static final int COLOR_BORDER = 0xFFD8DDE4;
    public static final int COLOR_TEXT_PRIMARY = 0xFF171A1F;
    public static final int COLOR_TEXT_SECONDARY = 0xFF4F5661;
    public static final int COLOR_TEXT_DISABLED = 0xFF626A75;

    public static final int COLOR_PRIMARY = 0xFF1558A6;
    public static final int COLOR_ON_PRIMARY = 0xFFFFFFFF;

    public static final int COLOR_POSITIVE_TEXT = 0xFF135C34;
    public static final int COLOR_POSITIVE_BG = 0xFFEAF5EE;
    public static final int COLOR_NEGATIVE_TEXT = 0xFF8C2630;
    public static final int COLOR_NEGATIVE_BG = 0xFFFAECEC;
    public static final int COLOR_REVIEW_TEXT = 0xFF6B4500;
    public static final int COLOR_REVIEW_BG = 0xFFFFF4D6;
    public static final int COLOR_ERROR_TEXT = 0xFFA32020;
    public static final int COLOR_ERROR_BG = 0xFFFBECEC;
    public static final int COLOR_INFO_TEXT = 0xFF184F91;
    public static final int COLOR_INFO_BG = 0xFFEAF1FB;

    public static final int SPACE_1_DP = 4;
    public static final int SPACE_2_DP = 8;
    public static final int SPACE_3_DP = 12;
    public static final int SPACE_4_DP = 16;
    public static final int SPACE_6_DP = 24;
    public static final int SPACE_8_DP = 32;

    public static final int RADIUS_SMALL_DP = 8;
    public static final int RADIUS_MEDIUM_DP = 12;
    public static final int RADIUS_LARGE_DP = 16;

    public static final int TOUCH_TARGET_MIN_DP = 48;
    public static final int LIST_ROW_MIN_DP = 56;
    public static final int CONTENT_MAX_WIDTH_DP = 720;

    public enum Weight { NORMAL, MEDIUM, BOLD }

    public enum TextRole {
        PRICE_HERO(30, 36, Weight.BOLD),
        TITLE_LARGE(22, 28, Weight.BOLD),
        TITLE_MEDIUM(18, 24, Weight.MEDIUM),
        BODY_LARGE(16, 24, Weight.NORMAL),
        BODY_MEDIUM(14, 20, Weight.NORMAL),
        LABEL(12, 16, Weight.MEDIUM);

        public final int sizeSp;
        public final int lineHeightSp;
        public final Weight weight;

        TextRole(int sizeSp, int lineHeightSp, Weight weight) {
            this.sizeSp = sizeSp;
            this.lineHeightSp = lineHeightSp;
            this.weight = weight;
        }
    }

    public static double contrastRatio(int foregroundArgb, int backgroundArgb) {
        double a = relativeLuminance(foregroundArgb);
        double b = relativeLuminance(backgroundArgb);
        double lighter = Math.max(a, b);
        double darker = Math.min(a, b);
        return (lighter + 0.05d) / (darker + 0.05d);
    }

    public static boolean passesSmallTextContrast(int foregroundArgb, int backgroundArgb) {
        return contrastRatio(foregroundArgb, backgroundArgb) >= 4.5d;
    }

    public static boolean passesLargeTextOrGraphicContrast(int foregroundArgb, int backgroundArgb) {
        return contrastRatio(foregroundArgb, backgroundArgb) >= 3.0d;
    }

    private static double relativeLuminance(int argb) {
        double r = linear((argb >> 16) & 0xff);
        double g = linear((argb >> 8) & 0xff);
        double b = linear(argb & 0xff);
        return 0.2126d * r + 0.7152d * g + 0.0722d * b;
    }

    private static double linear(int channel) {
        double s = channel / 255.0d;
        return s <= 0.04045d ? s / 12.92d : Math.pow((s + 0.055d) / 1.055d, 2.4d);
    }
}
