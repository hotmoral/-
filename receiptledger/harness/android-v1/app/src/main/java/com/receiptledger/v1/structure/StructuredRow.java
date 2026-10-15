package com.receiptledger.v1.structure;

import com.receiptledger.v1.layout.ReceiptRow;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class StructuredRow {
    public final int index;
    public final ReceiptRow row;
    public final RowRole role;
    public final String reason;
    public final List<MoneyCandidate> moneyCandidates;
    public final ReceiptDateCandidate dateCandidate;

    StructuredRow(int index, ReceiptRow row, RowRole role, String reason,
                  List<MoneyCandidate> moneyCandidates, ReceiptDateCandidate dateCandidate) {
        this.index = index;
        this.row = row;
        this.role = role;
        this.reason = reason;
        this.moneyCandidates = Collections.unmodifiableList(new ArrayList<>(moneyCandidates));
        this.dateCandidate = dateCandidate;
    }

    StructuredRow withRole(RowRole newRole, String newReason) {
        return new StructuredRow(index, row, newRole, newReason, moneyCandidates, dateCandidate);
    }

    public MoneyCandidate rightmostMoney() {
        MoneyCandidate best = null;
        for (MoneyCandidate candidate : moneyCandidates) {
            if (best == null || candidate.token.centerX > best.token.centerX) best = candidate;
        }
        return best;
    }
}
