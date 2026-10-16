package com.receiptledger.v1.structure;

import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.layout.ReceiptLayout;
import com.receiptledger.v1.layout.ReceiptLayoutAnalyzer;
import com.receiptledger.v1.ocr.*;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import static org.junit.Assert.*;

public class ReceiptStructureAnalyzerTest {
    @Test public void classifiesSyntheticReceiptWithoutUsingMlKitLines() {
        List<OcrElement> all = new ArrayList<>();
        addRow(all, 10, token("가상마트",10,10,45));
        addRow(all, 30, token("2026-10-15",10,30,58));
        addRow(all, 50, token("서울우유1L",10,50,52), token("3,200",95,50,30));
        addRow(all, 70, token("신라면5입",10,70,48), token("4,990",95,70,30));
        addRow(all, 90, token("쿠폰할인",10,90,40), token("-500",98,90,27));
        addRow(all,110, token("합계",10,110,20), token("7,690",95,110,30));
        addRow(all,130, token("신용카드",10,130,42), token("7,690",95,130,30));
        Collections.reverse(all);
        OcrLine wrong = new OcrLine("all-in-one", null, null, all);
        OcrDocument doc = new OcrDocument("raw",150,160,Collections.singletonList(new OcrBlock("all",null,null,Collections.singletonList(wrong))));
        ReceiptLayout layout = new ReceiptLayoutAnalyzer().analyze(doc);
        ReceiptStructure structure = new ReceiptStructureAnalyzer().analyze(layout);

        assertEquals(7, structure.rows.size());
        assertEquals(RowRole.HEADER, structure.rows.get(0).role);
        assertEquals(RowRole.DATE, structure.rows.get(1).role);
        assertEquals(RowRole.ITEM, structure.rows.get(2).role);
        assertEquals(RowRole.ITEM, structure.rows.get(3).role);
        assertEquals(RowRole.DISCOUNT, structure.rows.get(4).role);
        assertEquals(RowRole.TOTAL, structure.rows.get(5).role);
        assertEquals(RowRole.PAYMENT, structure.rows.get(6).role);
        assertEquals(2, structure.itemRows.size());
        assertEquals(Long.valueOf(7690), structure.totalAmount);
        assertNotNull(structure.date);
        assertEquals(2026, structure.date.year);assertEquals(10, structure.date.month);assertEquals(15, structure.date.day);
    }

    @Test public void suppressesAddressLikeMoneyRowBeforeDateWhenBodyExistsBelow() {
        List<OcrElement> all = new ArrayList<>();
        addRow(all, 10, token("가상마트",10,10,45));
        addRow(all, 30, token("서울 강서구 테스트로",10,30,75), token("1234",100,30,28));
        addRow(all, 55, token("2026-10-15",10,55,58));
        addRow(all, 90, token("서울우유1L",10,90,52), token("3,200",95,90,30));
        addRow(all,110, token("신라면5입",10,110,48), token("4,990",95,110,30));
        addRow(all,130, token("합계",10,130,20), token("8,190",95,130,30));
        OcrDocument doc = document(all, 150, 150);
        ReceiptStructure structure = new ReceiptStructureAnalyzer().analyze(new ReceiptLayoutAnalyzer().analyze(doc));

        assertEquals(RowRole.HEADER, structure.rows.get(1).role);
        assertEquals("ITEM_BEFORE_DATE_WITH_BODY_BELOW", structure.rows.get(1).reason);
        assertEquals(2, structure.itemRows.size());
        assertEquals("서울우유1L", structure.itemRows.get(0).row.tokens.get(0).text);
    }

    @Test public void doesNotSuppressSingleItemReceiptJustBecauseDateIsBelowCandidate() {
        List<OcrElement> all = new ArrayList<>();
        addRow(all, 20, token("테스트상품",10,20,50), token("3,200",95,20,30));
        addRow(all, 45, token("2026-10-15",10,45,58));
        addRow(all, 70, token("합계",10,70,20), token("3,200",95,70,30));
        ReceiptStructure structure = new ReceiptStructureAnalyzer().analyze(
                new ReceiptLayoutAnalyzer().analyze(document(all, 150, 100)));

        assertEquals(RowRole.ITEM, structure.rows.get(0).role);
        assertEquals(1, structure.itemRows.size());
    }

    @Test public void quantityLikeOneDigitIsNotMoney() {
        MoneyCandidate one = MoneyCandidate.parse(com.receiptledger.v1.layout.LayoutToken.from(token("2",10,10,10)));
        assertNull(one);
        MoneyCandidate price = MoneyCandidate.parse(com.receiptledger.v1.layout.LayoutToken.from(token("2,000",10,10,30)));
        assertNotNull(price);assertEquals(2000,price.amount);
    }

    @Test public void rejectsInvalidCalendarDate() {
        assertNull(ReceiptDateCandidate.find("2026-02-30 10:00"));
        assertNotNull(ReceiptDateCandidate.find("2024-02-29 10:00"));
    }

    private static OcrDocument document(List<OcrElement> all, int w, int h) {
        OcrLine wrong = new OcrLine("all-in-one", null, null, all);
        return new OcrDocument("raw",w,h,Collections.singletonList(new OcrBlock("all",null,null,Collections.singletonList(wrong))));
    }
    private static void addRow(List<OcrElement> all, double y, OcrElement... e) { Collections.addAll(all,e); }
    private static OcrElement token(String text,double x,double y,double w) { Quad q=new Quad(new PointD(x,y),new PointD(x+w,y),new PointD(x+w,y+10),new PointD(x,y+10));return new OcrElement(text,q,q); }
}
