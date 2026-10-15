package com.receiptledger.v1.image;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.graphics.Color;

import com.receiptledger.v1.document.PerspectivePlan;
import com.receiptledger.v1.document.Quad;

public final class PerspectiveWarp {
    private PerspectiveWarp() {}

    public static Result warp(Bitmap source, Quad quad) {
        PerspectivePlan plan=PerspectivePlan.create(quad,3200,8_000_000L);
        Bitmap out=Bitmap.createBitmap(plan.outputWidth,plan.outputHeight,Bitmap.Config.ARGB_8888);
        Canvas canvas=new Canvas(out); canvas.drawColor(Color.WHITE);
        Matrix matrix=new Matrix(); double[] d=plan.sourceToOutput.values(); float[] f=new float[9]; for(int i=0;i<9;i++)f[i]=(float)d[i]; matrix.setValues(f);
        Paint paint=new Paint(Paint.ANTI_ALIAS_FLAG|Paint.FILTER_BITMAP_FLAG|Paint.DITHER_FLAG);
        canvas.drawBitmap(source,matrix,paint);
        return new Result(out,plan);
    }

    public static final class Result {
        public final Bitmap bitmap; public final PerspectivePlan plan;
        Result(Bitmap bitmap,PerspectivePlan plan){this.bitmap=bitmap;this.plan=plan;}
    }
}
