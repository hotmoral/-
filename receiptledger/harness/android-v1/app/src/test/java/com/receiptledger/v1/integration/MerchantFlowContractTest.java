package com.receiptledger.v1.integration;

import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.ocr.*;
import com.receiptledger.v1.persistence.*;
import com.receiptledger.v1.recovery.*;
import com.receiptledger.v1.review.*;
import com.receiptledger.v1.validation.ValidationStatus;
import org.junit.Test;

import java.util.*;

import static org.junit.Assert.*;

public class MerchantFlowContractTest {
    @Test public void merchantFlowsFromHeaderThroughReview() {
        List<OcrElement> all = new ArrayList<>();
        Collections.addAll(all,
                token("영수증",10,10,30),
                token("가상마트",10,30,45),
                token("2026-10-15",10,50,58),
                token("서울우유1L",10,70,52), token("3,200",95,70,30),
                token("신라면5입",10,90,48), token("4,990",95,90,30),
                token("쿠폰할인",10,110,40), token("-500",98,110,27),
                token("합계",10,130,20), token("7,690",95,130,30));
        Collections.reverse(all);
        OcrDocument doc = new OcrDocument("raw",150,160,
                Collections.singletonList(new OcrBlock("all",null,null,
                        Collections.singletonList(new OcrLine("wrong",null,null,all)))));
        RecognitionCandidate candidate = new ReceiptRecognitionPipeline().evaluate(RecognitionPass.ORIGINAL,doc);
        ReceiptRecord base = ReceiptRecordFactory.create("merchant-1",1L,doc,candidate.structure,candidate.items,candidate.validation,150,160,false);

        assertEquals("가상마트",base.storeName);
        assertEquals(ValidationStatus.PASS,base.validationStatus);

        List<ReviewItemInput> unchanged = new ArrayList<>();
        for(PersistedItem item:base.items) unchanged.add(new ReviewItemInput(item.name,item.quantity,item.unitPrice,item.lineAmount));
        ReceiptRecord reviewed = new ReceiptReviewEngine().apply(base,"가상마트 강서점",base.purchaseDate,base.printedTotal,base.discountSum,unchanged);

        assertEquals("가상마트 강서점",reviewed.storeName);
        assertEquals(ValidationStatus.PASS_WITH_WARNINGS,reviewed.validationStatus);
        assertTrue(reviewed.issues.contains("USER_EDITED_STORE"));
    }

    private static OcrElement token(String text,double x,double y,double w){Quad q=new Quad(new PointD(x,y),new PointD(x+w,y),new PointD(x+w,y+10),new PointD(x,y+10));return new OcrElement(text,q,q);}
}
