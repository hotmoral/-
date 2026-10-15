package com.receiptledger.v1.structure;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;

public final class ReceiptMerchantResolver {
    private static final Set<String> GENERIC = new HashSet<>(Arrays.asList(
            "영수증", "매출전표", "카드전표", "거래명세서", "receipt", "salesreceipt", "receiptcopy"));

    private ReceiptMerchantResolver() {}

    public static String resolve(ReceiptStructure structure) {
        if (structure == null) return null;
        for (StructuredRow row : structure.rows) {
            if (row.role != RowRole.HEADER || row.row == null) continue;
            String candidate = normalize(row.row.text);
            if (isMerchantLike(candidate)) return candidate;
        }
        return null;
    }

    static boolean isMerchantLike(String value) {
        if (value == null) return false;
        String s = normalize(value);
        if (s.length() < 2 || s.length() > 80) return false;
        String key = s.replaceAll("[\\s\\p{Punct}]+", "").toLowerCase(Locale.ROOT);
        if (GENERIC.contains(key)) return false;
        boolean hasLetter = false;
        for (int i = 0; i < s.length(); i++) {
            if (Character.isLetter(s.charAt(i))) { hasLetter = true; break; }
        }
        return hasLetter;
    }

    private static String normalize(String value) {
        return value == null ? null : value.trim().replaceAll("\\s+", " ");
    }
}
