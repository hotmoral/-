package com.receiptledger.v1.ui;

import com.receiptledger.v1.item.*;import com.receiptledger.v1.persistence.*;import com.receiptledger.v1.validation.*;import org.junit.Test;import java.util.*;import static org.junit.Assert.*;

public class ReceiptDisplayFormatterTest {
    @Test public void summaryAndDetailAreStable(){PersistedItem item=new PersistedItem(0,3,"신라면 5입",2,4500L,9000L,ValueOrigin.PRINTED,ValueOrigin.PRINTED,ValueOrigin.PRINTED,ItemResolution.EXACT,"exact");ReceiptRecord r=new ReceiptRecord("id",1,"2026-10-15",null,"",9000L,9000L,0L,9000L,0L,ValidationStatus.PASS,1800,2400,true,Collections.emptyList(),Collections.singletonList(item));String s=ReceiptDisplayFormatter.summary(r);assertTrue(s.contains("2026-10-15"));assertTrue(s.contains("9,000원"));assertTrue(s.contains("PASS"));String d=ReceiptDisplayFormatter.detail(r);assertTrue(d.contains("신라면 5입"));assertTrue(d.contains("보정 OCR"));}
}
