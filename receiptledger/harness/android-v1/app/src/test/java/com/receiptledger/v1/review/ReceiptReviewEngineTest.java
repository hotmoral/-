package com.receiptledger.v1.review;

import com.receiptledger.v1.item.*;import com.receiptledger.v1.persistence.*;import com.receiptledger.v1.validation.*;import org.junit.Test;import java.util.*;import static org.junit.Assert.*;

public class ReceiptReviewEngineTest {
 private static ReceiptRecord base(){List<PersistedItem> items=Arrays.asList(new PersistedItem(0,1,"우유",1,3200L,3200L,ValueOrigin.DEFAULT_ONE,ValueOrigin.INFERRED_ARITHMETIC,ValueOrigin.PRINTED,ItemResolution.INFERRED,"auto"),new PersistedItem(1,2,"라면",1,4500L,4500L,ValueOrigin.DEFAULT_ONE,ValueOrigin.INFERRED_ARITHMETIC,ValueOrigin.PRINTED,ItemResolution.INFERRED,"auto"));return new ReceiptRecord("id",10,"2026-10-15",null,"RAW OCR",7700L,7700L,0L,7700L,0L,ValidationStatus.PASS,1800,2400,false,Collections.emptyList(),items);}
 @Test public void unchangedReviewRecomputesPass(){ReceiptRecord b=base();ReceiptRecord r=new ReceiptReviewEngine().apply(b,b.purchaseDate,b.printedTotal,b.discountSum,Arrays.asList(new ReviewItemInput("우유",1,3200L,3200L),new ReviewItemInput("라면",1,4500L,4500L)));assertEquals(ValidationStatus.PASS,r.validationStatus);assertEquals("RAW OCR",r.rawOcrText);assertEquals(0,r.issues.size());}
 @Test public void correctionMarksUserOriginAndWarnings(){ReceiptRecord b=base();ReceiptRecord r=new ReceiptReviewEngine().apply(b,b.purchaseDate,7800L,0L,Arrays.asList(new ReviewItemInput("우유",1,3300L,3300L),new ReviewItemInput("라면",1,4500L,4500L)));assertEquals(ValidationStatus.PASS_WITH_WARNINGS,r.validationStatus);assertEquals(ValueOrigin.USER_EDITED,r.items.get(0).unitPriceOrigin);assertEquals(ValueOrigin.USER_EDITED,r.items.get(0).lineAmountOrigin);assertEquals(Long.valueOf(7800),r.computedNet);}
 @Test public void arithmeticMismatchNeverAutoRepairs(){ReceiptRecord b=base();ReceiptRecord r=new ReceiptReviewEngine().apply(b,b.purchaseDate,7900L,0L,Arrays.asList(new ReviewItemInput("우유",2,1700L,3400L),new ReviewItemInput("라면",1,4500L,4500L)));assertEquals(ValidationStatus.PASS_WITH_WARNINGS,r.validationStatus);ReceiptRecord bad=new ReceiptReviewEngine().apply(b,b.purchaseDate,7800L,0L,Arrays.asList(new ReviewItemInput("우유",2,1700L,3300L),new ReviewItemInput("라면",1,4500L,4500L)));assertEquals(ValidationStatus.MISMATCH,bad.validationStatus);assertEquals(Long.valueOf(3300),bad.items.get(0).lineAmount);assertTrue(bad.issues.get(1).contains("ITEM_ARITHMETIC_MISMATCH")||bad.issues.toString().contains("ITEM_ARITHMETIC_MISMATCH"));}
 @Test public void clearedAmountIsIncomplete(){ReceiptRecord b=base();ReceiptRecord r=new ReceiptReviewEngine().apply(b,b.purchaseDate,b.printedTotal,0L,Arrays.asList(new ReviewItemInput("우유",1,3200L,null),new ReviewItemInput("라면",1,4500L,4500L)));assertEquals(ValidationStatus.INCOMPLETE,r.validationStatus);assertNull(r.itemLineSum);assertNull(r.computedNet);}
 @Test public void explicitFalseItemRemovalPreservesOrdinalAndCanFinishReview(){
  List<PersistedItem> items=Arrays.asList(
    new PersistedItem(0,1,"주소오검출",1,1234L,1234L,ValueOrigin.DEFAULT_ONE,ValueOrigin.PRINTED,ValueOrigin.PRINTED,ItemResolution.INFERRED,"auto"),
    new PersistedItem(1,5,"라면",1,4500L,4500L,ValueOrigin.PRINTED,ValueOrigin.PRINTED,ValueOrigin.PRINTED,ItemResolution.EXACT,"printed"));
  ReceiptRecord b=new ReceiptRecord("id2",10,"2026-10-15","마트","RAW",4500L,5734L,0L,5734L,1234L,ValidationStatus.MISMATCH,1800,2400,false,Collections.singletonList("RECEIPT_TOTAL_MISMATCH:1234"),items);
  ReceiptRecord r=new ReceiptReviewEngine().apply(b,b.storeName,b.purchaseDate,b.printedTotal,0L,Arrays.asList(ReviewItemInput.removed(),new ReviewItemInput("라면",1,4500L,4500L)));
  assertEquals(1,r.items.size());
  assertEquals(1,r.items.get(0).ordinal);
  assertEquals(Long.valueOf(4500L),r.itemLineSum);
  assertEquals(Long.valueOf(4500L),r.computedNet);
  assertEquals(Long.valueOf(0L),r.difference);
  assertEquals(ValidationStatus.PASS_WITH_WARNINGS,r.validationStatus);
  assertTrue(r.issues.contains("USER_REMOVED_ITEM:0"));
  assertEquals(CaptureReviewAssessmentV2.Decision.AUTO_CONFIRMED,CaptureReviewAssessmentV2.assess(r).decision);
 }
}
