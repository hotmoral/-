package com.receiptledger.v1.structure;

import com.receiptledger.v1.layout.LayoutToken;
import java.text.Normalizer;

public final class MoneyCandidate {
    public final long amount;
    public final String rawText;
    public final LayoutToken token;

    private MoneyCandidate(long amount, String rawText, LayoutToken token) {
        this.amount = amount;
        this.rawText = rawText;
        this.token = token;
    }

    public static MoneyCandidate parse(LayoutToken token) {
        if (token == null || token.text == null) return null;
        String raw = Normalizer.normalize(token.text.trim(), Normalizer.Form.NFKC);
        if (raw.isEmpty()) return null;
        boolean currencyMarked = raw.contains("₩") || raw.contains("원");
        boolean grouped = raw.contains(",");
        boolean parenthesized = raw.startsWith("(") && raw.endsWith(")");
        String s = raw.replace("₩", "").replace("원", "").trim();
        if (parenthesized && s.length() >= 2) s = s.substring(1, s.length() - 1).trim();
        while (s.endsWith("T") || s.endsWith("t") || s.endsWith("*")) s = s.substring(0, s.length() - 1).trim();
        boolean negative = parenthesized;
        if (s.startsWith("-") || s.startsWith("−")) { negative = true; s = s.substring(1).trim(); }
        else if (s.startsWith("+")) s = s.substring(1).trim();
        String digits = s.replace(",", "");
        if (!digits.matches("[0-9]+")) return null;
        if (digits.length() < 3 && !currencyMarked && !grouped) return null;
        if (digits.length() > 10) return null;
        try {
            long value = Long.parseLong(digits);
            if (value > 9_999_999_999L) return null;
            return new MoneyCandidate(negative ? -value : value, raw, token);
        } catch (NumberFormatException e) {
            return null;
        }
    }
}
