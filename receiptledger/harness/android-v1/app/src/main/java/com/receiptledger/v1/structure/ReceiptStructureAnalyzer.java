package com.receiptledger.v1.structure;

import com.receiptledger.v1.layout.LayoutToken;
import com.receiptledger.v1.layout.ReceiptLayout;
import com.receiptledger.v1.layout.ReceiptRow;

import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public final class ReceiptStructureAnalyzer {
    private static final String[] TOTAL = {"합계","총계","총액","결제금액","받을금액","총구매","청구금액","TOTAL"};
    private static final String[] DISCOUNT = {"할인","쿠폰","CPN","DISCOUNT","에누리"};
    private static final String[] PAYMENT = {"신용카드","카드","현금","승인","결제","부가세","과세","면세","세액","공급가","잔돈"};

    public ReceiptStructure analyze(ReceiptLayout layout) {
        List<StructuredRow> rows = new ArrayList<>();
        if (layout == null) return new ReceiptStructure(rows, null, null);

        for (int i = 0; i < layout.rows.size(); i++) rows.add(classify(i, layout.rows.get(i)));

        int firstBody = rows.size();
        for (int i = 0; i < rows.size(); i++) {
            RowRole role = rows.get(i).role;
            if (role == RowRole.ITEM || role == RowRole.DISCOUNT || role == RowRole.TOTAL || role == RowRole.PAYMENT) {
                firstBody = i; break;
            }
        }
        for (int i = 0; i < firstBody; i++) {
            StructuredRow row = rows.get(i);
            if (row.role == RowRole.UNKNOWN && containsLetter(row.row.text)) rows.set(i, row.withRole(RowRole.HEADER, "PRE_BODY_TEXT"));
        }

        Long total = null;
        ReceiptDateCandidate date = null;
        for (StructuredRow row : rows) {
            if (date == null && row.dateCandidate != null) date = row.dateCandidate;
            if (row.role == RowRole.TOTAL) {
                MoneyCandidate money = row.rightmostMoney();
                if (money != null) total = money.amount;
            }
        }
        return new ReceiptStructure(rows, total, date);
    }

    private StructuredRow classify(int index, ReceiptRow row) {
        List<MoneyCandidate> money = new ArrayList<>();
        for (LayoutToken token : row.tokens) {
            MoneyCandidate candidate = MoneyCandidate.parse(token);
            if (candidate != null) money.add(candidate);
        }
        ReceiptDateCandidate date = ReceiptDateCandidate.find(row.text);
        String normalized = normalize(row.text);

        if (containsAny(normalized, TOTAL)) return new StructuredRow(index,row,RowRole.TOTAL,"TOTAL_KEYWORD",money,date);
        if (containsAny(normalized, DISCOUNT)) return new StructuredRow(index,row,RowRole.DISCOUNT,"DISCOUNT_KEYWORD",money,date);
        if (containsAny(normalized, PAYMENT)) return new StructuredRow(index,row,RowRole.PAYMENT,"PAYMENT_OR_TAX_KEYWORD",money,date);
        if (date != null) return new StructuredRow(index,row,RowRole.DATE,"VALID_DATE_PATTERN",money,date);
        if (looksLikeItem(row,money)) return new StructuredRow(index,row,RowRole.ITEM,"TEXT_LEFT_OF_RIGHTMOST_MONEY",money,date);
        return new StructuredRow(index,row,RowRole.UNKNOWN,"NO_CONSERVATIVE_MATCH",money,date);
    }

    private static boolean looksLikeItem(ReceiptRow row, List<MoneyCandidate> money) {
        MoneyCandidate rightmost = null;
        for (MoneyCandidate candidate : money) if (candidate.amount >= 0 && (rightmost == null || candidate.token.centerX > rightmost.token.centerX)) rightmost = candidate;
        if (rightmost == null) return false;
        double moneyLeft = rightmost.token.centerX - rightmost.token.width * 0.5;
        for (LayoutToken token : row.tokens) {
            if (token.centerX >= moneyLeft) continue;
            if (containsLetter(token.text)) return true;
        }
        return false;
    }

    private static boolean containsAny(String text, String[] needles) {
        for (String needle : needles) if (text.contains(needle)) return true;
        return false;
    }

    private static String normalize(String text) {
        return Normalizer.normalize(text == null ? "" : text, Normalizer.Form.NFKC).toUpperCase(Locale.ROOT).replace(" ", "");
    }

    private static boolean containsLetter(String text) {
        if (text == null) return false;
        for (int i = 0; i < text.length(); i++) if (Character.isLetter(text.charAt(i))) return true;
        return false;
    }
}
