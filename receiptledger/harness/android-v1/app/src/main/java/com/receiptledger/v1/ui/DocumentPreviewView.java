package com.receiptledger.v1.ui;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RectF;
import android.view.View;

import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;

public final class DocumentPreviewView extends View {
    private final Paint imagePaint=new Paint(Paint.FILTER_BITMAP_FLAG|Paint.DITHER_FLAG);
    private final Paint quadPaint=new Paint(Paint.ANTI_ALIAS_FLAG);
    private Bitmap bitmap; private Quad quad;

    public DocumentPreviewView(Context context){super(context);quadPaint.setStyle(Paint.Style.STROKE);quadPaint.setStrokeWidth(4*getResources().getDisplayMetrics().density);quadPaint.setColor(Color.rgb(0,150,90));setBackgroundColor(Color.rgb(235,235,235));}
    public void setDocument(Bitmap bitmap,Quad quad){this.bitmap=bitmap;this.quad=quad;invalidate();}

    @Override protected void onDraw(Canvas canvas){super.onDraw(canvas);if(bitmap==null)return;float vw=getWidth(),vh=getHeight();float scale=Math.min(vw/bitmap.getWidth(),vh/bitmap.getHeight());float dw=bitmap.getWidth()*scale,dh=bitmap.getHeight()*scale;float ox=(vw-dw)/2f,oy=(vh-dh)/2f;RectF dst=new RectF(ox,oy,ox+dw,oy+dh);canvas.drawBitmap(bitmap,null,dst,imagePaint);if(quad!=null){PointD[] p=quad.points();for(int i=0;i<4;i++){PointD a=p[i],b=p[(i+1)%4];canvas.drawLine(ox+(float)a.x*scale,oy+(float)a.y*scale,ox+(float)b.x*scale,oy+(float)b.y*scale,quadPaint);}}}
}
