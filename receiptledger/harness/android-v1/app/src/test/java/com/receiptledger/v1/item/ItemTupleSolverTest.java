package com.receiptledger.v1.item;

import com.receiptledger.v1.document.PointD;import com.receiptledger.v1.document.Quad;import com.receiptledger.v1.layout.*;import com.receiptledger.v1.ocr.*;import com.receiptledger.v1.structure.*;import org.junit.Test;import java.util.*;import static org.junit.Assert.*;

public class ItemTupleSolverTest {
    @Test public void solvesExactInferredDefaultAndPartialRows(){
        List<OcrElement> e=new ArrayList<>();
        row(e,10,t("우유",10,10,25),t("3,200",100,10,30));
        row(e,30,t("라면",10,30,25),t("4,500",70,30,30),t("2",105,30,10),t("9,000",125,30,30));
        row(e,50,t("만두",10,50,25),t("3",85,50,10),t("12,000",120,50,35));
        row(e,70,t("과자",10,70,25),t("2,000",70,70,30),t("3",105,70,10),t("5,000",125,70,30));
        Collections.reverse(e);OcrDocument doc=doc(e);ReceiptLayout layout=new ReceiptLayoutAnalyzer().analyze(doc);ReceiptStructure structure=new ReceiptStructureAnalyzer().analyze(layout);ItemTupleResult result=new ItemTupleSolver().solve(structure);
        assertEquals(4,result.items.size());
        ItemTuple a=result.items.get(0);assertEquals(ItemResolution.INFERRED,a.resolution);assertEquals(Integer.valueOf(1),a.quantity);assertEquals(Long.valueOf(3200),a.unitPrice);assertEquals(Long.valueOf(3200),a.lineAmount);assertEquals(ValueOrigin.DEFAULT_ONE,a.quantityOrigin);
        ItemTuple b=result.items.get(1);assertEquals(ItemResolution.EXACT,b.resolution);assertEquals(Integer.valueOf(2),b.quantity);assertEquals(Long.valueOf(4500),b.unitPrice);assertEquals(Long.valueOf(9000),b.lineAmount);
        ItemTuple c=result.items.get(2);assertEquals(ItemResolution.INFERRED,c.resolution);assertEquals(Integer.valueOf(3),c.quantity);assertEquals(Long.valueOf(4000),c.unitPrice);assertEquals(Long.valueOf(12000),c.lineAmount);assertEquals(ValueOrigin.INFERRED_ARITHMETIC,c.unitPriceOrigin);
        ItemTuple d=result.items.get(3);assertEquals(ItemResolution.PARTIAL,d.resolution);assertNull(d.quantity);assertNull(d.unitPrice);assertEquals(Long.valueOf(5000),d.lineAmount);
        assertEquals(1,result.exactCount);assertEquals(2,result.inferredCount);assertEquals(1,result.partialCount);
    }
    @Test public void parsesMarkedQuantities(){LayoutToken x2=LayoutToken.from(t("x2",10,10,12));LayoutToken ea=LayoutToken.from(t("3EA",10,10,20));assertEquals(2,QuantityCandidate.parse(x2).quantity);assertEquals(3,QuantityCandidate.parse(ea).quantity);}
    private static OcrDocument doc(List<OcrElement> e){OcrLine l=new OcrLine("wrong",null,null,e);return new OcrDocument("raw",180,100,Collections.singletonList(new OcrBlock("b",null,null,Collections.singletonList(l))));}
    private static void row(List<OcrElement> out,double y,OcrElement... e){Collections.addAll(out,e);}private static OcrElement t(String s,double x,double y,double w){Quad q=new Quad(new PointD(x,y),new PointD(x+w,y),new PointD(x+w,y+10),new PointD(x,y+10));return new OcrElement(s,q,q);}
}
