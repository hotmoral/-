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
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class DocumentPreviewView extends View {
    private final Paint imagePaint=new Paint(Paint.FILTER_BITMAP_FLAG|Paint.DITHER_FLAG);
    private final Paint quadPaint=new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint ocrPaint=new Paint(Paint.ANTI_ALIAS_FLAG);
    private final RectF bitmapRect=new RectF();
    private Bitmap bitmap; private Quad quad; private List<Quad> ocrQuads=Collections.emptyList();

    public DocumentPreviewView(Context context){super(context);float d=getResources().getDisplayMetrics().density;quadPaint.setStyle(Paint.Style.STROKE);quadPaint.setStrokeWidth(4*d);quadPaint.setColor(Color.rgb(0,150,90));ocrPaint.setStyle(Paint.Style.STROKE);ocrPaint.setStrokeWidth(1.5f*d);ocrPaint.setColor(Color.rgb(30,100,220));setBackgroundColor(Color.rgb(235,235,235));}
    public void setDocument(Bitmap bitmap,Quad quad){this.bitmap=bitmap;this.quad=quad;this.ocrQuads=Collections.emptyList();invalidate();}
    public void setOcrQuads(List<Quad> quads){this.ocrQuads=quads==null?Collections.emptyList():new ArrayList<>(quads);invalidate();}

    @Override protected void onDraw(Canvas canvas){super.onDraw(canvas);if(bitmap==null)return;float vw=getWidth(),vh=getHeight();float scale=Math.min(vw/bitmap.getWidth(),vh/bitmap.getHeight());float dw=bitmap.getWidth()*scale,dh=bitmap.getHeight()*scale;float ox=(vw-dw)/2f,oy=(vh-dh)/2f;bitmapRect.set(ox,oy,ox+dw,oy+dh);canvas.drawBitmap(bitmap,null,bitmapRect,imagePaint);if(quad!=null)drawQuad(canvas,quad,ox,oy,scale,quadPaint);for(Quad q:ocrQuads)drawQuad(canvas,q,ox,oy,scale,ocrPaint);}
    private static void drawQuad(Canvas canvas,Quad q,float ox,float oy,float scale,Paint paint){PointD[] p=q.points();for(int i=0;i<4;i++){PointD a=p[i],b=p[(i+1)%4];canvas.drawLine(ox+(float)a.x*scale,oy+(float)a.y*scale,ox+(float)b.x*scale,oy+(float)b.y*scale,paint);}}
}
