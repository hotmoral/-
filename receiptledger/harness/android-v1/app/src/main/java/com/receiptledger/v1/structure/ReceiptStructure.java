package com.receiptledger.v1.structure;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class ReceiptStructure {
    public final List<StructuredRow> rows;
    public final List<StructuredRow> itemRows;
    public final Long totalAmount;
    public final ReceiptDateCandidate date;

    ReceiptStructure(List<StructuredRow> rows, Long totalAmount, ReceiptDateCandidate date) {
        this.rows = Collections.unmodifiableList(new ArrayList<>(rows));
        List<StructuredRow> items = new ArrayList<>();
        for (StructuredRow row : rows) if (row.role == RowRole.ITEM) items.add(row);
        this.itemRows = Collections.unmodifiableList(items);
        this.totalAmount = totalAmount;
        this.date = date;
    }
}
