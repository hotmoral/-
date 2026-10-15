package com.receiptledger.v1.image;

import android.graphics.Bitmap;
import com.receiptledger.v1.document.LumaPlane;
import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;

public final class BitmapLumaAdapter {
    private BitmapLumaAdapter() {}

    public static Sampled sample(Bitmap bitmap,int maxDimension){
        int sw=bitmap.getWidth(),sh=bitmap.getHeight();
        double scale=Math.min(1.0,maxDimension/(double)Math.max(sw,sh));
        int w=Math.max(1,(int)Math.round(sw*scale)),h=Math.max(1,(int)Math.round(sh*scale));
        byte[] luma=new byte[w*h]; int[] row=new int[sw];
        for(int y=0;y<h;y++){
            int sy=Math.min(sh-1,(int)((y+0.5)*sh/h)); bitmap.getPixels(row,0,sw,0,sy,sw,1);
            for(int x=0;x<w;x++){
                int sx=Math.min(sw-1,(int)((x+0.5)*sw/w));int c=row[sx];int r=(c>>16)&255,g=(c>>8)&255,b=c&255;luma[y*w+x]=(byte)((77*r+150*g+29*b)>>8);
            }
        }
        return new Sampled(new LumaPlane(w,h,luma),sw/(double)w,sh/(double)h);
    }

    public static final class Sampled {
        public final LumaPlane plane; private final double scaleX,scaleY;
        Sampled(LumaPlane plane,double scaleX,double scaleY){this.plane=plane;this.scaleX=scaleX;this.scaleY=scaleY;}
        public Quad toSource(Quad q){return new Quad(p(q.topLeft),p(q.topRight),p(q.bottomRight),p(q.bottomLeft));}
        private PointD p(PointD p){return new PointD(p.x*scaleX,p.y*scaleY);}
    }
}
