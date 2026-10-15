package com.receiptledger.v1.image;

import android.content.ContentResolver;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.net.Uri;

import java.io.IOException;
import java.io.InputStream;

public final class ImageLoader {
    private static final int MAX_EDGE=4096;
    private static final long MAX_PIXELS=12_000_000L;
    private ImageLoader() {}

    public static LoadedImage load(Context context, Uri uri) throws IOException {
        ContentResolver resolver=context.getContentResolver();
        int orientation=1;
        try(InputStream in=resolver.openInputStream(uri)){ if(in==null)throw new IOException("Cannot open image"); orientation=ExifOrientationParser.readOrientation(in); }
        BitmapFactory.Options bounds=new BitmapFactory.Options(); bounds.inJustDecodeBounds=true;
        try(InputStream in=resolver.openInputStream(uri)){ if(in==null)throw new IOException("Cannot open image"); BitmapFactory.decodeStream(in,null,bounds); }
        if(bounds.outWidth<=0||bounds.outHeight<=0)throw new IOException("Unsupported image");
        int sample=1;
        while ((bounds.outWidth/sample)>MAX_EDGE || (bounds.outHeight/sample)>MAX_EDGE || ((long)bounds.outWidth*bounds.outHeight)/(sample*(long)sample)>MAX_PIXELS) sample*=2;
        BitmapFactory.Options opts=new BitmapFactory.Options();opts.inSampleSize=sample;opts.inPreferredConfig=Bitmap.Config.ARGB_8888;
        Bitmap decoded;
        try(InputStream in=resolver.openInputStream(uri)){ if(in==null)throw new IOException("Cannot open image"); decoded=BitmapFactory.decodeStream(in,null,opts); }
        if(decoded==null)throw new IOException("Image decode failed");
        Bitmap normalized=applyOrientation(decoded,orientation);
        if(normalized!=decoded)decoded.recycle();
        return new LoadedImage(normalized,bounds.outWidth,bounds.outHeight,sample,orientation);
    }

    private static Bitmap applyOrientation(Bitmap source,int o){
        if(o==1)return source; Matrix m=new Matrix();
        switch(o){
            case 2: m.setScale(-1,1); break;
            case 3: m.setRotate(180); break;
            case 4: m.setScale(1,-1); break;
            case 5: m.setRotate(90); m.postScale(-1,1); break;
            case 6: m.setRotate(90); break;
            case 7: m.setRotate(-90); m.postScale(-1,1); break;
            case 8: m.setRotate(-90); break;
            default: return source;
        }
        try { return Bitmap.createBitmap(source,0,0,source.getWidth(),source.getHeight(),m,true); }
        catch (RuntimeException e) { return source; }
    }

    public static final class LoadedImage {
        public final Bitmap bitmap; public final int encodedWidth,encodedHeight,sampleSize,exifOrientation;
        LoadedImage(Bitmap bitmap,int encodedWidth,int encodedHeight,int sampleSize,int exifOrientation){this.bitmap=bitmap;this.encodedWidth=encodedWidth;this.encodedHeight=encodedHeight;this.sampleSize=sampleSize;this.exifOrientation=exifOrientation;}
    }
}
