package com.receiptledger.v1.ocr;

import com.receiptledger.v1.document.*;
import org.junit.Test;
import static org.junit.Assert.*;

public class OcrGeometryMapperTest {
    @Test public void correctedElementMapsBackToSource(){
        Quad source=new Quad(new PointD(10,20),new PointD(110,25),new PointD(100,225),new PointD(20,210));
        PerspectivePlan plan=PerspectivePlan.create(source,3000,8_000_000);
        Quad input=OcrGeometryMapper.rectangle(0,0,plan.outputWidth-1,plan.outputHeight-1);
        Quad mapped=OcrGeometryMapper.map(input,plan.outputToSource);
        assertEquals(source.topLeft.x,mapped.topLeft.x,1e-6);assertEquals(source.topLeft.y,mapped.topLeft.y,1e-6);
        assertEquals(source.bottomRight.x,mapped.bottomRight.x,1e-6);assertEquals(source.bottomRight.y,mapped.bottomRight.y,1e-6);
    }
}
