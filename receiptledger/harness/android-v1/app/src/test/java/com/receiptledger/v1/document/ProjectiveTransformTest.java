package com.receiptledger.v1.document;

import org.junit.Test;
import static org.junit.Assert.*;

public class ProjectiveTransformTest {
    @Test public void cornersAndInverseRoundTrip() {
        Quad q = new Quad(new PointD(12,10),new PointD(92,16),new PointD(84,96),new PointD(18,88));
        PerspectivePlan plan = PerspectivePlan.create(q, 3000, 8_000_000);
        PointD[] source=q.points();
        PointD[] expected={new PointD(0,0),new PointD(plan.outputWidth-1,0),new PointD(plan.outputWidth-1,plan.outputHeight-1),new PointD(0,plan.outputHeight-1)};
        for(int i=0;i<4;i++){
            PointD mapped=plan.sourceToOutput.map(source[i]);
            assertEquals(expected[i].x,mapped.x,1e-6);
            assertEquals(expected[i].y,mapped.y,1e-6);
            PointD back=plan.outputToSource.map(mapped);
            assertEquals(source[i].x,back.x,1e-6);
            assertEquals(source[i].y,back.y,1e-6);
        }
        PointD p=new PointD(50,50);PointD back=plan.outputToSource.map(plan.sourceToOutput.map(p));
        assertEquals(p.x,back.x,1e-6);assertEquals(p.y,back.y,1e-6);
    }
}
