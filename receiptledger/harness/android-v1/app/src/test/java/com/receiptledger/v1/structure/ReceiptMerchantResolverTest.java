package com.receiptledger.v1.structure;

import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.layout.ReceiptLayout;
import com.receiptledger.v1.layout.ReceiptLayoutAnalyzer;
import com.receiptledger.v1.ocr.OcrBlock;
import com.receiptledger.v1.ocr.OcrDocument;
import com.receiptledger.v1.ocr.OcrElement;
import com.receiptledger.v1.ocr.OcrLine;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import static org.junit.Assert.*;

public class ReceiptMerchantResolverTest {
    @Test public void skipsGenericReceiptHeaderAndKeepsMerchant() {
        ReceiptStructure s = structure("영수증", "가상마트", "2026-10-15");
        assertEquals("가상마트", ReceiptMerchantResolver.resolve(s));
    }

    @Test public void refusesGenericOnlyHeader() {
        ReceiptStructure s = structure("매출전표", "2026-10-15");
        assertNull(ReceiptMerchantResolver.resolve(s));
    }

    @Test public void requiresLetters() {
        assertFalse(ReceiptMerchantResolver.isMerchantLike("123456"));
        assertTrue(ReceiptMerchantResolver.isMerchantLike("GS25 강서점"));
    }

    private static ReceiptStructure structure(String... rows) {
        List<OcrElement> elements = new ArrayList<>();
        double y = 10;
        for (String row : rows) {
            elements.add(token(row, 10, y, Math.max(25, row.length() * 8)));
            y += 20;
        }
        OcrLine wrong = new OcrLine("all", null, null, elements);
        OcrDocument doc = new OcrDocument("raw", 180, 120,
                Collections.singletonList(new OcrBlock("all", null, null, Collections.singletonList(wrong))));
        ReceiptLayout layout = new ReceiptLayoutAnalyzer().analyze(doc);
        return new ReceiptStructureAnalyzer().analyze(layout);
    }

    private static OcrElement token(String text, double x, double y, double w) {
        Quad q = new Quad(new PointD(x,y), new PointD(x+w,y), new PointD(x+w,y+10), new PointD(x,y+10));
        return new OcrElement(text,q,q);
    }
}
