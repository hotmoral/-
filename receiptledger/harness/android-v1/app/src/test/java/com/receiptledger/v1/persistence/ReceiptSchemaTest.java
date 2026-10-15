package com.receiptledger.v1.persistence;

import org.junit.Test;import static org.junit.Assert.*;

public class ReceiptSchemaTest {
    @Test public void schemaV1HasAtomicChildContracts(){assertEquals(1,ReceiptSchema.VERSION);assertTrue(ReceiptSchema.CREATE_ITEMS.contains("ON DELETE CASCADE"));assertTrue(ReceiptSchema.CREATE_ISSUES.contains("ON DELETE CASCADE"));assertTrue(ReceiptSchema.CREATE_RECEIPTS.contains("validation_status TEXT NOT NULL"));assertTrue(ReceiptSchema.CREATE_RECEIPTS.contains("perspective_corrected"));}
}
