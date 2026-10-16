package com.receiptledger.v1.design;

import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.priceintel.ComparisonBasisV2;
import com.receiptledger.v1.validation.ValidationStatus;
import java.util.Arrays;
import org.junit.Test;
import static org.junit.Assert.*;

public final class DesignSystemFoundationV1Test {
    @Test public void typographySpacingAndTouchTargetsAreFrozen() {
        assertEquals(6, DesignTokensV1.TextRole.values().length);
        assertEquals(30, DesignTokensV1.TextRole.PRICE_HERO.sizeSp);
        assertEquals(22, DesignTokensV1.TextRole.TITLE_LARGE.sizeSp);
        assertEquals(16, DesignTokensV1.TextRole.BODY_LARGE.sizeSp);
        assertEquals(48, DesignTokensV1.TOUCH_TARGET_MIN_DP);
        assertEquals(56, DesignTokensV1.LIST_ROW_MIN_DP);
        assertEquals(720, DesignTokensV1.CONTENT_MAX_WIDTH_DP);
        assertEquals(1, DesignTokensV1.ELEVATION_CARD_DP);
        assertEquals(3, DesignTokensV1.ELEVATION_FLOATING_DP);
        assertArrayEquals(new int[]{4,8,12,16,24,32}, new int[]{
                DesignTokensV1.SPACE_1_DP, DesignTokensV1.SPACE_2_DP, DesignTokensV1.SPACE_3_DP,
                DesignTokensV1.SPACE_4_DP, DesignTokensV1.SPACE_6_DP, DesignTokensV1.SPACE_8_DP});
    }

    @Test public void palettePassesSmallTextContrastContract() {
        for (SemanticToneV1 tone : SemanticToneV1.values()) {
            assertTrue(tone.name() + " contrast=" + DesignTokensV1.contrastRatio(tone.foregroundArgb, tone.backgroundArgb),
                    DesignTokensV1.passesSmallTextContrast(tone.foregroundArgb, tone.backgroundArgb));
        }
        assertTrue(DesignTokensV1.passesSmallTextContrast(
                DesignTokensV1.COLOR_TEXT_SECONDARY, DesignTokensV1.COLOR_BACKGROUND));
    }

    @Test public void everyPriceStateHasTextAndSemanticTone() {
        int count = 0;
        for (PriceEvaluationV1.Judgment judgment : new PriceEvaluationV1.Judgment[]{
                PriceEvaluationV1.Judgment.VERY_CHEAP,
                PriceEvaluationV1.Judgment.CHEAP,
                PriceEvaluationV1.Judgment.TYPICAL,
                PriceEvaluationV1.Judgment.EXPENSIVE,
                PriceEvaluationV1.Judgment.VERY_EXPENSIVE}) {
            SemanticPresentationV1.Presentation p = SemanticPresentationV1.price(PriceEvaluationV1.Status.EVALUATED, judgment);
            assertFalse(p.labelKo.isEmpty());
            assertFalse(p.explanationKo.isEmpty());
            assertTrue(p.judgment);
            count++;
        }
        for (PriceEvaluationV1.Status status : new PriceEvaluationV1.Status[]{
                PriceEvaluationV1.Status.INSUFFICIENT_HISTORY,
                PriceEvaluationV1.Status.CONTEXTUAL_ONLY,
                PriceEvaluationV1.Status.NON_POSITIVE_BASELINE}) {
            SemanticPresentationV1.Presentation p = SemanticPresentationV1.price(status, PriceEvaluationV1.Judgment.NONE);
            assertFalse(p.labelKo.isEmpty());
            assertFalse(p.explanationKo.isEmpty());
            assertFalse(p.judgment);
            assertNotEquals(SemanticToneV1.POSITIVE, p.tone);
            assertNotEquals(SemanticToneV1.NEGATIVE, p.tone);
            count++;
        }
        assertEquals(8, count);
    }

    @Test public void validationAndReusableUiStatesAreExplicit() {
        for (ValidationStatus status : ValidationStatus.values()) {
            SemanticPresentationV1.Presentation p = SemanticPresentationV1.validation(status);
            assertFalse(p.labelKo.isEmpty());
            assertFalse(p.explanationKo.isEmpty());
        }
        assertEquals(4, ValidationStatus.values().length);
        for (UiStatePresentationV1.Kind kind : UiStatePresentationV1.Kind.values()) {
            UiStatePresentationV1 state = UiStatePresentationV1.of(kind);
            assertFalse(state.titleKo.isEmpty());
            assertFalse(state.bodyKo.isEmpty());
            assertNotNull(state.tone);
        }
        assertEquals(8, UiStatePresentationV1.Kind.values().length);
    }

    @Test public void responsiveBreakpointsUseWindowWidthNotDeviceType() {
        assertEquals(ResponsiveLayoutPolicyV1.WidthClass.COMPACT, ResponsiveLayoutPolicyV1.widthClass(360));
        assertEquals(ResponsiveLayoutPolicyV1.WidthClass.COMPACT, ResponsiveLayoutPolicyV1.widthClass(599));
        assertEquals(ResponsiveLayoutPolicyV1.WidthClass.MEDIUM, ResponsiveLayoutPolicyV1.widthClass(600));
        assertEquals(ResponsiveLayoutPolicyV1.WidthClass.MEDIUM, ResponsiveLayoutPolicyV1.widthClass(839));
        assertEquals(ResponsiveLayoutPolicyV1.WidthClass.EXPANDED, ResponsiveLayoutPolicyV1.widthClass(840));
        assertEquals(16, ResponsiveLayoutPolicyV1.pageGutterDp(412));
        assertEquals(24, ResponsiveLayoutPolicyV1.pageGutterDp(600));
        assertFalse(ResponsiveLayoutPolicyV1.twoPaneEligible(840, 479));
        assertTrue(ResponsiveLayoutPolicyV1.twoPaneEligible(840, 480));
    }

    @Test public void chartGrammarNeverConnectsDifferentComparisonBases() {
        ChartGrammarV1.requireSingleBasis(Arrays.asList(ComparisonBasisV2.weightKg(), ComparisonBasisV2.weightKg()));
        try {
            ChartGrammarV1.requireSingleBasis(Arrays.asList(ComparisonBasisV2.weightKg(), ComparisonBasisV2.each()));
            fail("cross-basis series must fail");
        } catch (IllegalArgumentException expected) {
            assertTrue(expected.getMessage().contains("cross-basis"));
        }
        assertEquals("원/kg", ChartGrammarV1.axisLabelKo(ComparisonBasisV2.weightKg()));
        assertTrue(ChartGrammarV1.axisLabelKo(ComparisonBasisV2.likeForm("BAG", "봉")).startsWith("참고"));
    }

    @Test public void iconGrammarCentralizesGlyphHitAreaAndSpokenLabels() {
        assertEquals(10, IconGrammarV1.values().length);
        assertEquals(24, DesignTokensV1.ICON_GLYPH_DP);
        for (IconGrammarV1 icon : IconGrammarV1.values()) {
            assertTrue(icon.validForIconOnlyControl());
            assertEquals(24, icon.glyphSizeDp());
            assertEquals(48, icon.minimumHitTargetDp());
            assertFalse(icon.contentDescriptionKo.isEmpty());
        }
    }

    @Test public void cheapExpensiveColorNeverExistsWithoutTextMeaning() {
        SemanticPresentationV1.Presentation cheap = SemanticPresentationV1.price(
                PriceEvaluationV1.Status.EVALUATED, PriceEvaluationV1.Judgment.CHEAP);
        SemanticPresentationV1.Presentation expensive = SemanticPresentationV1.price(
                PriceEvaluationV1.Status.EVALUATED, PriceEvaluationV1.Judgment.EXPENSIVE);
        assertEquals(SemanticToneV1.POSITIVE, cheap.tone);
        assertEquals(SemanticToneV1.NEGATIVE, expensive.tone);
        assertTrue(cheap.labelKo.contains("저렴"));
        assertTrue(expensive.labelKo.contains("비쌈"));
    }

    @Test public void canonicalMetrics() {
        int pricePresentations = 5 + 3;
        int contrastPairs = SemanticToneV1.values().length + 1;
        System.out.println("CP30_METRICS typography_roles=" + DesignTokensV1.TextRole.values().length
                + " semantic_tones=" + SemanticToneV1.values().length
                + " price_presentations=" + pricePresentations
                + " validation_presentations=" + ValidationStatus.values().length
                + " ui_states=" + UiStatePresentationV1.Kind.values().length
                + " contrast_pairs=" + contrastPairs
                + " responsive_cases=5 chart_cross_basis_rejections=1 min_touch_dp="
                + DesignTokensV1.TOUCH_TARGET_MIN_DP
                + " icon_roles=" + IconGrammarV1.values().length
                + " elevation_tokens=2 representative_activities=2");
    }
}
