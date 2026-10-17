package com.receiptledger.v1.devicevalidation;

import com.receiptledger.v1.BuildConfig;
import com.receiptledger.v1.item.ItemTuple;
import com.receiptledger.v1.item.ItemTupleResult;
import com.receiptledger.v1.item.QuantityCandidate;
import com.receiptledger.v1.layout.LayoutToken;
import com.receiptledger.v1.structure.MoneyCandidate;
import com.receiptledger.v1.structure.ReceiptStructure;
import com.receiptledger.v1.structure.StructuredRow;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/** Debug evidence projection. Emits candidate counts/relative regions only, never receipt values/text. */
public final class CandidateStructureDiagnosticsV1 {
    public static final class Summary {
        public final boolean available;
        public final int moneyCandidates;
        public final int quantityCandidates;
        public final int quantityBeforeFirstMoney;
        public final int quantityBetweenMoney;
        public final int quantityAfterLine;
        public final int exactArithmeticPairs;
        public final int integerUnitPairs;
        public final String solverResolution;
        public final String solverReason;

        private Summary(boolean available, int moneyCandidates, int quantityCandidates,
                        int quantityBeforeFirstMoney, int quantityBetweenMoney, int quantityAfterLine,
                        int exactArithmeticPairs, int integerUnitPairs,
                        String solverResolution, String solverReason) {
            this.available = available;
            this.moneyCandidates = moneyCandidates;
            this.quantityCandidates = quantityCandidates;
            this.quantityBeforeFirstMoney = quantityBeforeFirstMoney;
            this.quantityBetweenMoney = quantityBetweenMoney;
            this.quantityAfterLine = quantityAfterLine;
            this.exactArithmeticPairs = exactArithmeticPairs;
            this.integerUnitPairs = integerUnitPairs;
            this.solverResolution = token(solverResolution);
            this.solverReason = token(solverReason);
        }

        public String reportLine() {
            return new StringBuilder(320)
                    .append("RL_CP37_DIAG version=1 target=FIRST_REVIEW_ITEM")
                    .append(" available=").append(available ? 1 : 0)
                    .append(" money_candidates=").append(moneyCandidates)
                    .append(" quantity_candidates=").append(quantityCandidates)
                    .append(" quantity_before_first_money=").append(quantityBeforeFirstMoney)
                    .append(" quantity_between_money=").append(quantityBetweenMoney)
                    .append(" quantity_after_line=").append(quantityAfterLine)
                    .append(" exact_arithmetic_pairs=").append(exactArithmeticPairs)
                    .append(" integer_unit_pairs=").append(integerUnitPairs)
                    .append(" solver_resolution=").append(solverResolution)
                    .append(" solver_reason=").append(solverReason)
                    .toString();
        }
    }

    private static final Map<String,List<Summary>> BY_RECEIPT = new ConcurrentHashMap<>();

    private CandidateStructureDiagnosticsV1() {}

    public static void publishForReceipt(String receiptId, ReceiptStructure structure, ItemTupleResult tupleResult) {
        if (!BuildConfig.DEBUG || receiptId == null || receiptId.isEmpty() || structure == null || tupleResult == null) return;
        List<Summary> summaries = new ArrayList<>();
        for (int i = 0; i < tupleResult.items.size(); i++) summaries.add(summarize(structure, tupleResult, i));
        BY_RECEIPT.put(receiptId, Collections.unmodifiableList(summaries));
    }

    public static Summary takeForReceipt(String receiptId, int targetOrdinal) {
        if (!BuildConfig.DEBUG || receiptId == null) return unavailable();
        List<Summary> summaries = BY_RECEIPT.remove(receiptId);
        if (summaries == null || targetOrdinal < 0 || targetOrdinal >= summaries.size()) return unavailable();
        return summaries.get(targetOrdinal);
    }

    public static Summary summarize(ReceiptStructure structure, ItemTupleResult tupleResult, int targetOrdinal) {
        if (structure == null || tupleResult == null || targetOrdinal < 0
                || targetOrdinal >= tupleResult.items.size()) return unavailable();
        ItemTuple item = tupleResult.items.get(targetOrdinal);
        StructuredRow row = null;
        for (StructuredRow candidate : structure.rows) {
            if (candidate.index == item.rowIndex) { row = candidate; break; }
        }
        if (row == null) return unavailable();

        List<MoneyCandidate> money = new ArrayList<>();
        for (MoneyCandidate candidate : row.moneyCandidates) if (candidate.amount >= 0) money.add(candidate);
        Collections.sort(money, (a,b) -> Double.compare(a.token.centerX, b.token.centerX));
        List<QuantityCandidate> quantities = new ArrayList<>();
        for (LayoutToken token : row.row.tokens) {
            QuantityCandidate q = QuantityCandidate.parse(token);
            if (q != null) quantities.add(q);
        }
        Collections.sort(quantities, (a,b) -> Double.compare(a.token.centerX, b.token.centerX));

        MoneyCandidate first = money.isEmpty() ? null : money.get(0);
        MoneyCandidate line = money.isEmpty() ? null : money.get(money.size() - 1);
        int before = 0, between = 0, after = 0;
        if (first != null && line != null) {
            for (QuantityCandidate q : quantities) {
                if (q.token.centerX < first.token.centerX) before++;
                else if (q.token.centerX > line.token.centerX) after++;
                else between++;
            }
        }

        int exactPairs = 0;
        int integerUnitPairs = 0;
        if (line != null && line.amount > 0) {
            for (MoneyCandidate unit : money) {
                if (unit == line || unit.amount <= 0 || unit.token.centerX >= line.token.centerX) continue;
                if (line.amount % unit.amount == 0) {
                    long inferred = line.amount / unit.amount;
                    if (inferred >= 1 && inferred <= 99) integerUnitPairs++;
                }
                for (QuantityCandidate q : quantities) {
                    Long product = safeMultiply(unit.amount, q.quantity);
                    if (product != null && product == line.amount) exactPairs++;
                }
            }
        }

        return new Summary(true, money.size(), quantities.size(), before, between, after,
                exactPairs, integerUnitPairs,
                item.resolution == null ? "UNKNOWN" : item.resolution.name(), item.reason);
    }

    public static Summary unavailable() {
        return new Summary(false, 0, 0, 0, 0, 0, 0, 0, "UNKNOWN", "UNKNOWN");
    }

    private static Long safeMultiply(long amount, int quantity) {
        if (amount < 0 || quantity < 0) return null;
        if (quantity != 0 && amount > Long.MAX_VALUE / quantity) return null;
        return amount * quantity;
    }

    private static String token(String value) {
        if (value == null || value.isEmpty()) return "UNKNOWN";
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            boolean ok = (c >= 'A' && c <= 'Z') || c == '_' || (c >= '0' && c <= '9');
            if (!ok) return "UNKNOWN";
        }
        return value;
    }
}
