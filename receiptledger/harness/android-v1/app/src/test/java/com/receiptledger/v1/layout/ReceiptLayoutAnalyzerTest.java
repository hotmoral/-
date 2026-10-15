package com.receiptledger.v1.layout;

import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.ocr.*;
import org.junit.Test;

import java.util.Arrays;
import java.util.Collections;

import static org.junit.Assert.*;

public class ReceiptLayoutAnalyzerTest {
    @Test public void rebuildsRowsFromShuffledElementsWithSkew() {
        double s = 0.08;
        OcrElement price2 = element("4,500", 78, 54, 30, 10, s);
        OcrElement name1 = element("서울우유", 12, 20, 38, 10, s);
        OcrElement name3 = element("왕교자", 12, 88, 35, 10, s);
        OcrElement price1 = element("3,200", 80, 20, 28, 10, s);
        OcrElement name2 = element("신라면", 12, 54, 32, 10, s);
        OcrElement price3 = element("8,990", 80, 88, 28, 10, s);
        OcrDocument doc = document(price2, name1, name3, price1, name2, price3);

        ReceiptLayout layout = new ReceiptLayoutAnalyzer().analyze(doc);
        assertEquals(3, layout.rows.size());
        assertEquals(6, layout.tokenCount);
        assertEquals(s, layout.estimatedSkewSlope, 1e-6);
        assertEquals("서울우유 3,200", layout.rows.get(0).text);
        assertEquals("신라면 4,500", layout.rows.get(1).text);
        assertEquals("왕교자 8,990", layout.rows.get(2).text);
    }

    @Test public void ignoresBlankAndGeometrylessElements() {
        OcrElement valid = element("합계", 10, 30, 20, 10, 0);
        OcrElement blank = new OcrElement("   ", valid.inputQuad, valid.sourceQuad);
        OcrElement noGeometry = new OcrElement("1234", null, null);
        ReceiptLayout layout = new ReceiptLayoutAnalyzer().analyze(document(noGeometry, blank, valid));
        assertEquals(1, layout.tokenCount);
        assertEquals(1, layout.rows.size());
        assertEquals("합계", layout.rows.get(0).text);
    }

    @Test public void emptyDocumentIsSafe() {
        ReceiptLayout layout = new ReceiptLayoutAnalyzer().analyze(new OcrDocument("", 10, 10, Collections.emptyList()));
        assertTrue(layout.rows.isEmpty());
        assertEquals(0, layout.tokenCount);
    }

    private static OcrDocument document(OcrElement... elements) {
        OcrLine deliberatelyWrongSingleLine = new OcrLine("ignored", null, null, Arrays.asList(elements));
        OcrBlock block = new OcrBlock("ignored", null, null, Collections.singletonList(deliberatelyWrongSingleLine));
        return new OcrDocument("raw", 140, 140, Collections.singletonList(block));
    }

    private static OcrElement element(String text, double x, double baseY, double w, double h, double slope) {
        PointD tl = new PointD(x, baseY + slope * x);
        PointD tr = new PointD(x + w, baseY + slope * (x + w));
        PointD br = new PointD(x + w, baseY + h + slope * (x + w));
        PointD bl = new PointD(x, baseY + h + slope * x);
        Quad q = new Quad(tl, tr, br, bl);
        return new OcrElement(text, q, q);
    }
}
