package com.receiptledger.v1.priceintel;

import java.text.Normalizer;
import java.util.Locale;
import java.util.Objects;

/** Stable comparison cohort identity. LIKE_FORM is contextual, not mathematically normalized. */
public final class ComparisonBasisV2 {
    public enum Kind { STANDARD_PACKAGE, WEIGHT_KG, VOLUME_L, EACH, LIKE_FORM }

    public final Kind kind;
    public final String formKey;
    public final String displayUnit;

    private ComparisonBasisV2(Kind kind, String formKey, String displayUnit) {
        this.kind = Objects.requireNonNull(kind, "kind");
        this.formKey = formKey;
        this.displayUnit = Objects.requireNonNull(displayUnit, "displayUnit");
        if (kind == Kind.LIKE_FORM && (formKey == null || formKey.isEmpty())) {
            throw new IllegalArgumentException("LIKE_FORM requires formKey");
        }
        if (kind != Kind.LIKE_FORM && formKey != null) {
            throw new IllegalArgumentException("only LIKE_FORM uses formKey");
        }
    }

    public static ComparisonBasisV2 standardPackage() { return new ComparisonBasisV2(Kind.STANDARD_PACKAGE, null, "package"); }
    public static ComparisonBasisV2 weightKg() { return new ComparisonBasisV2(Kind.WEIGHT_KG, null, "kg"); }
    public static ComparisonBasisV2 volumeLiter() { return new ComparisonBasisV2(Kind.VOLUME_L, null, "L"); }
    public static ComparisonBasisV2 each() { return new ComparisonBasisV2(Kind.EACH, null, "each"); }

    public static ComparisonBasisV2 likeForm(String unitName, String rawLabel) {
        String unit = normalize(unitName);
        String raw = normalize(rawLabel);
        if (unit.isEmpty()) throw new IllegalArgumentException("unitName");
        if (raw.isEmpty()) raw = unit;
        return new ComparisonBasisV2(Kind.LIKE_FORM, unit + ":" + raw, rawLabel == null || rawLabel.trim().isEmpty() ? unitName : rawLabel.trim());
    }

    public boolean isStrictNormalized() { return kind != Kind.LIKE_FORM; }

    public String key() { return kind == Kind.LIKE_FORM ? "LIKE_FORM:" + formKey : kind.name(); }

    private static String normalize(String value) {
        return Normalizer.normalize(value == null ? "" : value, Normalizer.Form.NFKC)
                .trim().replaceAll("\\s+", " ").toUpperCase(Locale.ROOT);
    }

    @Override public boolean equals(Object other) {
        if (this == other) return true;
        if (!(other instanceof ComparisonBasisV2)) return false;
        ComparisonBasisV2 that = (ComparisonBasisV2) other;
        return kind == that.kind && Objects.equals(formKey, that.formKey);
    }

    @Override public int hashCode() { return Objects.hash(kind, formKey); }
    @Override public String toString() { return key(); }
}
