package com.receiptledger.v1.persistence;

public final class ReceiptSchema {
    private ReceiptSchema(){}
    public static final String DB_NAME="receiptledger-v1.db";public static final int VERSION=1;
    public static final String CREATE_RECEIPTS="CREATE TABLE receipts (id TEXT PRIMARY KEY NOT NULL,created_at_ms INTEGER NOT NULL,purchase_date TEXT,store_name TEXT,raw_ocr_text TEXT NOT NULL,printed_total INTEGER,item_line_sum INTEGER,discount_sum INTEGER,computed_net INTEGER,difference INTEGER,validation_status TEXT NOT NULL,source_width INTEGER NOT NULL,source_height INTEGER NOT NULL,perspective_corrected INTEGER NOT NULL CHECK(perspective_corrected IN (0,1)))";
    public static final String CREATE_ITEMS="CREATE TABLE receipt_items (receipt_id TEXT NOT NULL,ordinal INTEGER NOT NULL,row_index INTEGER NOT NULL,name TEXT NOT NULL,quantity INTEGER,unit_price INTEGER,line_amount INTEGER,quantity_origin TEXT NOT NULL,unit_price_origin TEXT NOT NULL,line_amount_origin TEXT NOT NULL,resolution TEXT NOT NULL,reason TEXT,PRIMARY KEY(receipt_id,ordinal),FOREIGN KEY(receipt_id) REFERENCES receipts(id) ON DELETE CASCADE)";
    public static final String CREATE_ISSUES="CREATE TABLE receipt_issues (receipt_id TEXT NOT NULL,ordinal INTEGER NOT NULL,issue TEXT NOT NULL,PRIMARY KEY(receipt_id,ordinal),FOREIGN KEY(receipt_id) REFERENCES receipts(id) ON DELETE CASCADE)";
    public static final String CREATE_RECEIPT_DATE_INDEX="CREATE INDEX idx_receipts_date ON receipts(purchase_date,created_at_ms)";
}
