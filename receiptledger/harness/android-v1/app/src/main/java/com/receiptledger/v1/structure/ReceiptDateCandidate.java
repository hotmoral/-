package com.receiptledger.v1.structure;

import java.text.Normalizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class ReceiptDateCandidate {
    private static final Pattern DELIMITED = Pattern.compile("(?<![0-9])([0-9]{2,4})[./-]([0-9]{1,2})[./-]([0-9]{1,2})(?![0-9])");
    private static final Pattern KOREAN = Pattern.compile("(?<![0-9])([0-9]{2,4})\\s*년\\s*([0-9]{1,2})\\s*월\\s*([0-9]{1,2})\\s*일");

    public final int year;
    public final int month;
    public final int day;
    public final String rawText;

    private ReceiptDateCandidate(int year, int month, int day, String rawText) {
        this.year = year; this.month = month; this.day = day; this.rawText = rawText;
    }

    public static ReceiptDateCandidate find(String text) {
        if (text == null) return null;
        String normalized = Normalizer.normalize(text, Normalizer.Form.NFKC);
        ReceiptDateCandidate result = match(normalized, DELIMITED);
        return result != null ? result : match(normalized, KOREAN);
    }

    private static ReceiptDateCandidate match(String text, Pattern pattern) {
        Matcher m = pattern.matcher(text);
        if (!m.find()) return null;
        int year = Integer.parseInt(m.group(1));
        if (year < 100) year += 2000;
        int month = Integer.parseInt(m.group(2));
        int day = Integer.parseInt(m.group(3));
        if (!valid(year, month, day)) return null;
        return new ReceiptDateCandidate(year, month, day, m.group(0));
    }

    private static boolean valid(int year, int month, int day) {
        if (year < 2000 || year > 2199 || month < 1 || month > 12 || day < 1) return false;
        int[] days = {31,28,31,30,31,30,31,31,30,31,30,31};
        boolean leap = (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;
        if (leap) days[1] = 29;
        return day <= days[month - 1];
    }
}
