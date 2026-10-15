package com.receiptledger.v1.document;

import org.junit.Test;
import static org.junit.Assert.*;

public class ReceiptDocumentDetectorTest {
    @Test public void detectsBrightTrapezoidOnDarkBackground() {
        int w=120,h=120;byte[] data=new byte[w*h];
        for(int i=0;i<data.length;i++)data[i]=(byte)35;
        PointD tl=new PointD(22,14),tr=new PointD(98,20),br=new PointD(90,104),bl=new PointD(14,96);
        for(int y=0;y<h;y++)for(int x=0;x<w;x++)if(inside(x+0.5,y+0.5,tl,tr,br,bl))data[y*w+x]=(byte)230;
        DocumentDetection d=new ReceiptDocumentDetector().detect(new LumaPlane(w,h,data));
        assertTrue(d.reason,d.found);assertTrue(d.confidence>=0.55);assertTrue(d.quad.isConvex());
        assertEquals(tl.x,d.quad.topLeft.x,8.0);assertEquals(tr.x,d.quad.topRight.x,8.0);
        assertEquals(bl.y,d.quad.bottomLeft.y,8.0);assertEquals(br.y,d.quad.bottomRight.y,8.0);
    }

    @Test public void rejectsLowContrastSurface() {
        int w=80,h=80;byte[] data=new byte[w*h];
        for(int y=0;y<h;y++)for(int x=0;x<w;x++)data[y*w+x]=(byte)((x>10&&x<70&&y>10&&y<70)?207:200);
        DocumentDetection d=new ReceiptDocumentDetector().detect(new LumaPlane(w,h,data));
        assertFalse(d.found);assertEquals("LOW_CONTRAST",d.reason);
    }

    private static boolean inside(double x,double y,PointD... p){
        double sign=0;
        for(int i=0;i<4;i++){PointD a=p[i],b=p[(i+1)%4];double c=(b.x-a.x)*(y-a.y)-(b.y-a.y)*(x-a.x);if(Math.abs(c)<1e-9)continue;if(sign==0)sign=Math.signum(c);else if(Math.signum(c)!=sign)return false;}
        return true;
    }
}
