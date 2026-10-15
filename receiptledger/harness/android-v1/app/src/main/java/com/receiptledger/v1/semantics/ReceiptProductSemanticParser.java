package com.receiptledger.v1.semantics;

import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.PackageMeasure;
import com.receiptledger.v1.catalog.ProductSpecification;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.catalog.SalesUnitCode;
import java.math.BigDecimal;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Conservative parser for semantic candidates in one receipt item name. */
public final class ReceiptProductSemanticParser {
    private static final Pattern BRACKET_BRAND = Pattern.compile("^\\s*\\[([^\\]]{1,40})\\]\\s*");
    private static final Pattern PAREN = Pattern.compile("\\(([^()]{1,30})\\)");
    private static final Pattern MULTI_FWD = Pattern.compile("(?i)(\\d+(?:\\.\\d+)?)\\s*(ML|KG|L|G)\\s*[X×*]\\s*(\\d+)\\s*(?:개입|입)?");
    private static final Pattern MULTI_REV = Pattern.compile("(?i)(\\d+)\\s*[X×*]\\s*(\\d+(?:\\.\\d+)?)\\s*(ML|KG|L|G)\\s*(?:개입|입)?");
    private static final Pattern PACK_COUNT = Pattern.compile("(\\d+)\\s*(개입|입)");
    private static final Pattern PURCHASE_FORM = Pattern.compile("(\\d+(?:\\.\\d+)?)\\s*(상자|봉|단|팩|개)");
    private static final Pattern PHYSICAL = Pattern.compile("(?i)(\\d+(?:\\.\\d+)?)\\s*(ML|KG|L|G)");

    private final List<String> knownBrands = new ArrayList<>();

    public ReceiptProductSemanticParser(Collection<String> brands) {
        if (brands != null) for (String brand : brands) {
            String b = norm(brand);
            if (!b.isEmpty() && !knownBrands.contains(b)) knownBrands.add(b);
        }
        knownBrands.sort(Comparator.comparingInt(String::length).reversed().thenComparing(String::compareTo));
    }

    public static ReceiptProductSemanticParser withoutBrandKnowledge() {
        return new ReceiptProductSemanticParser(null);
    }

    public ReceiptProductSemantics parse(String rawName) {
        String raw = rawName == null ? "" : rawName;
        String work = norm(raw);
        List<String> reasons = new ArrayList<>();
        SemanticCandidate<String> brand = null;
        SemanticCandidate<String> variant = null;
        SemanticCandidate<ProductSpecification> spec = null;
        SemanticCandidate<PurchaseForm> purchase = null;
        boolean ambiguous = false;

        Matcher m = BRACKET_BRAND.matcher(work);
        if (m.find()) {
            String value = norm(m.group(1));
            if (!value.isEmpty()) {
                brand = SemanticCandidate.of(value, m.group(0).trim(), CatalogField.Confidence.HIGH,
                        "explicit leading bracketed brand evidence");
                work = remove(work, m.start(), m.end());
            }
        } else {
            String known = knownBrandPrefix(work);
            if (known != null) {
                brand = SemanticCandidate.of(known, known, CatalogField.Confidence.HIGH,
                        "caller-supplied known brand prefix");
                work = norm(work.substring(known.length()));
            }
        }

        m = PAREN.matcher(work);
        if (m.find() && nonNumericDescriptor(norm(m.group(1)))) {
            String value = norm(m.group(1));
            variant = SemanticCandidate.of(value, m.group(0), CatalogField.Confidence.HIGH,
                    "explicit non-numeric parenthetical descriptor");
            work = remove(work, m.start(), m.end());
        }

        m = MULTI_FWD.matcher(work);
        if (m.find()) {
            spec = multipack(m.group(1), m.group(2), m.group(3), m.group(0), true);
            work = remove(work, m.start(), m.end());
        } else {
            m = MULTI_REV.matcher(work);
            if (m.find()) {
                spec = multipack(m.group(2), m.group(3), m.group(1), m.group(0), false);
                work = remove(work, m.start(), m.end());
            }
        }

        Integer packCount = null;
        String packEvidence = null;
        if (spec == null) {
            m = PACK_COUNT.matcher(work);
            if (m.find()) {
                packCount = positiveInt(m.group(1));
                packEvidence = m.group(0);
                work = remove(work, m.start(), m.end());
            }
        }

        m = PURCHASE_FORM.matcher(work);
        if (m.find()) {
            BigDecimal quantity = positiveDecimal(m.group(1));
            String label = m.group(2);
            CatalogField.Confidence confidence = strongForm(label)
                    ? CatalogField.Confidence.HIGH : CatalogField.Confidence.MEDIUM;
            purchase = SemanticCandidate.of(new PurchaseForm(quantity, purchaseUnit(label), label), m.group(0), confidence,
                    confidence == CatalogField.Confidence.HIGH
                            ? "explicit raw purchase-form label"
                            : "context-sensitive count/package-form label");
            if (confidence == CatalogField.Confidence.MEDIUM) {
                ambiguous = true;
                reasons.add("context-sensitive purchase form: " + label);
            }
            work = remove(work, m.start(), m.end());
        }

        if (spec == null) {
            m = PHYSICAL.matcher(work);
            if (m.find()) {
                BigDecimal amount = positiveDecimal(m.group(1));
                SalesUnitCode unit = physicalUnit(m.group(2));
                PackageMeasure physical = new PackageMeasure(amount, unit);
                if (packCount != null) {
                    PackageMeasure total = new PackageMeasure(amount.multiply(BigDecimal.valueOf(packCount)), unit);
                    spec = SemanticCandidate.of(new ProductSpecification(total, packCount, physical),
                            m.group(0) + " " + packEvidence, CatalogField.Confidence.MEDIUM,
                            "explicit physical measure plus pack count without multiplication delimiter");
                } else {
                    spec = SemanticCandidate.of(new ProductSpecification(physical, null, null), m.group(0),
                            CatalogField.Confidence.MEDIUM,
                            "standalone physical measure can be packaged net content");
                    if (purchase == null) purchase = SemanticCandidate.of(
                            new PurchaseForm(amount, unit, m.group(2)), m.group(0), CatalogField.Confidence.MEDIUM,
                            "standalone physical measure can be commodity purchase amount");
                    ambiguous = true;
                    reasons.add("physical measure is ambiguous between package specification and purchase form");
                }
                work = remove(work, m.start(), m.end());
            } else if (packCount != null) {
                spec = SemanticCandidate.of(new ProductSpecification(null, packCount, null), packEvidence,
                        CatalogField.Confidence.HIGH, "explicit 입/개입 package count");
            }
        }

        String lexical = cleanLexical(work);
        SemanticCandidate<String> product = lexical.isEmpty() ? null : SemanticCandidate.of(
                lexical, lexical, CatalogField.Confidence.HIGH,
                "remaining lexical receipt text after explicit semantic tokens");
        boolean structured = brand != null || variant != null || spec != null || purchase != null;
        if (product == null) reasons.add("no lexical product name remains");
        if (!structured) reasons.add("no structured semantic evidence beyond lexical name");
        boolean review = product == null || ambiguous || !structured;
        return new ReceiptProductSemantics(raw, brand, product, variant, spec, purchase, ambiguous, review, reasons);
    }

    private SemanticCandidate<ProductSpecification> multipack(
            String amountRaw, String unitRaw, String countRaw, String evidence, boolean forward) {
        BigDecimal amount = positiveDecimal(amountRaw);
        SalesUnitCode unit = physicalUnit(unitRaw);
        int count = positiveInt(countRaw);
        PackageMeasure inner = new PackageMeasure(amount, unit);
        PackageMeasure total = new PackageMeasure(amount.multiply(BigDecimal.valueOf(count)), unit);
        return SemanticCandidate.of(new ProductSpecification(total, count, inner), evidence,
                CatalogField.Confidence.HIGH,
                forward ? "explicit inner-content multiplication and pack count"
                        : "explicit pack count and inner-content multiplication");
    }

    private String knownBrandPrefix(String work) {
        String upper = work.toUpperCase(Locale.ROOT);
        for (String brand : knownBrands) {
            if (upper.startsWith(brand.toUpperCase(Locale.ROOT))) return work.substring(0, brand.length());
        }
        return null;
    }

    private static boolean nonNumericDescriptor(String value) {
        if (value.isEmpty()) return false;
        for (int i = 0; i < value.length(); i++) if (Character.isDigit(value.charAt(i))) return false;
        for (int i = 0; i < value.length(); i++) if (Character.isLetter(value.charAt(i))) return true;
        return false;
    }

    private static boolean strongForm(String label) {
        return "봉".equals(label) || "상자".equals(label) || "단".equals(label);
    }

    private static SalesUnitCode purchaseUnit(String label) {
        switch (label) {
            case "봉": return SalesUnitCode.BAG;
            case "상자": return SalesUnitCode.BOX;
            case "단": return SalesUnitCode.BUNDLE;
            case "팩": return SalesUnitCode.PACK;
            case "개": return SalesUnitCode.EACH;
            default: throw new IllegalArgumentException("unsupported purchase unit: " + label);
        }
    }

    private static SalesUnitCode physicalUnit(String raw) {
        switch (raw.toUpperCase(Locale.ROOT)) {
            case "G": return SalesUnitCode.GRAM;
            case "KG": return SalesUnitCode.KILOGRAM;
            case "ML": return SalesUnitCode.MILLILITER;
            case "L": return SalesUnitCode.LITER;
            default: throw new IllegalArgumentException("unsupported physical unit: " + raw);
        }
    }

    private static BigDecimal positiveDecimal(String raw) {
        BigDecimal value = new BigDecimal(raw);
        if (value.compareTo(BigDecimal.ZERO) <= 0) throw new IllegalArgumentException("quantity must be positive");
        return value;
    }

    private static int positiveInt(String raw) {
        int value = Integer.parseInt(raw);
        if (value < 1) throw new IllegalArgumentException("count must be positive");
        return value;
    }

    private static String remove(String value, int start, int end) {
        return norm(value.substring(0, start) + " " + value.substring(end));
    }

    private static String cleanLexical(String value) {
        return norm(norm(value).replaceAll("\\s*[-_/|]+\\s*", " "));
    }

    private static String norm(String raw) {
        if (raw == null) return "";
        return Normalizer.normalize(raw, Normalizer.Form.NFKC).trim().replaceAll("\\s+", " ");
    }
}
