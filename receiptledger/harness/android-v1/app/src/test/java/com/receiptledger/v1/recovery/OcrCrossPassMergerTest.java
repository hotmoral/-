package com.receiptledger.v1.recovery;

import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.ocr.*;
import com.receiptledger.v1.validation.ValidationStatus;
import org.junit.Test;

import java.util.*;

import static org.junit.Assert.*;

public class OcrCrossPassMergerTest {
    @Test public void complementaryPassesProduceValidatedMergedCandidate() {
        OcrDocument primary = doc(
                token("가상마트",10,10,45), token("2026-10-15",10,30,58),
                token("서울우유1L",10,50,52), token("3,200",95,50,30),
                token("신라면5입",10,70,48),
                token("쿠폰할인",10,90,40), token("-500",98,90,27),
                token("합계",10,110,20), token("7,690",95,110,30));
        OcrDocument supplement = doc(
                token("가상마트",10,10,45), token("2026-10-15",10,30,58),
                token("신라면5입",10,70,48), token("4,990",95,70,30),
                token("쿠폰할인",10,90,40), token("-500",98,90,27),
                token("합계",10,110,20), token("7690",95,110,30));

        ReceiptRecognitionPipeline pipeline = new ReceiptRecognitionPipeline();
        RecognitionCandidate a = pipeline.evaluate(RecognitionPass.ORIGINAL,primary);
        RecognitionCandidate b = pipeline.evaluate(RecognitionPass.CONTRAST,supplement);
        RecognitionCandidate merged = pipeline.mergeCandidate(a,b);
        RecognitionCandidate current = pipeline.better(a,b);

        assertNotNull(merged);
        assertEquals(RecognitionPass.MERGED,merged.pass);
        assertEquals(2,merged.items.items.size());
        assertEquals(ValidationStatus.PASS,merged.validation.status);
        assertTrue(merged.score>current.score);
        assertTrue(pipeline.shouldAcceptMerged(current,merged));
        assertEquals(10,merged.document.elementCount());
    }

    @Test public void geometryPreventsDuplicateTextVariants() {
        OcrDocument a=doc(token("3,200",95,50,30));
        OcrDocument b=doc(token("3200",95,50,30));
        assertNull(new OcrCrossPassMerger().merge(a,b));
    }

    @Test public void mergedDiagnosticDoesNotConsumeOcrBudget() {
        ReceiptRecognitionPipeline pipeline=new ReceiptRecognitionPipeline();
        RecognitionCandidate a=pipeline.evaluate(RecognitionPass.ORIGINAL,doc(token("가상마트",10,10,45)));
        RecognitionCandidate b=pipeline.evaluate(RecognitionPass.CONTRAST,doc(token("2026-10-15",10,30,58)));
        RecognitionCandidate merged=pipeline.mergeCandidate(a,b);
        assertNotNull(merged);
        RecoveryResult result=new RecoveryResult(merged,Arrays.asList(new PassDiagnostic(a),new PassDiagnostic(b),new PassDiagnostic(merged)));
        assertEquals(2,result.attemptedPasses());
        assertEquals(1,result.derivedCandidates());
    }

    private static OcrDocument doc(OcrElement... elements){List<OcrElement> e=new ArrayList<>(Arrays.asList(elements));Collections.reverse(e);OcrLine l=new OcrLine("all",null,null,e);return new OcrDocument("raw",150,140,Collections.singletonList(new OcrBlock("all",null,null,Collections.singletonList(l))));}
    private static OcrElement token(String text,double x,double y,double w){Quad q=new Quad(new PointD(x,y),new PointD(x+w,y),new PointD(x+w,y+10),new PointD(x,y+10));return new OcrElement(text,q,q);}
}
