package com.receiptledger.v1;

import android.app.Activity;
import android.content.ClipData;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.Gravity;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.receiptledger.v1.document.DocumentDetection;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.document.ReceiptDocumentDetector;
import com.receiptledger.v1.image.BitmapLumaAdapter;
import com.receiptledger.v1.image.ImageLoader;
import com.receiptledger.v1.image.PerspectiveWarp;
import com.receiptledger.v1.ui.DocumentPreviewView;

import java.io.File;
import java.io.IOException;
import java.util.Locale;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class MainActivity extends Activity {
    private static final int REQ_CAMERA=1001;
    private static final int REQ_PICK=1002;
    private final ExecutorService worker=Executors.newSingleThreadExecutor();
    private final ReceiptDocumentDetector detector=new ReceiptDocumentDetector();

    private DocumentPreviewView preview;
    private TextView status;
    private Button correctButton;
    private Button originalButton;
    private Uri pendingCaptureUri;
    private Bitmap sourceBitmap;
    private Bitmap correctedBitmap;
    private Quad detectedQuad;
    private long generation;

    @Override protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        int pad=dp(16);
        LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(pad,pad,pad,pad);root.setGravity(Gravity.CENTER_HORIZONTAL);
        TextView title=new TextView(this);title.setText(R.string.document_title);title.setTextSize(24);title.setGravity(Gravity.CENTER);
        LinearLayout actions=new LinearLayout(this);actions.setOrientation(LinearLayout.HORIZONTAL);actions.setGravity(Gravity.CENTER);
        Button camera=new Button(this);camera.setText(R.string.capture);camera.setOnClickListener(v->launchCamera());
        Button gallery=new Button(this);gallery.setText(R.string.gallery);gallery.setOnClickListener(v->launchPicker());
        correctButton=new Button(this);correctButton.setText(R.string.correct);correctButton.setEnabled(false);correctButton.setOnClickListener(v->correctPerspective());
        originalButton=new Button(this);originalButton.setText(R.string.original);originalButton.setEnabled(false);originalButton.setOnClickListener(v->{preview.setDocument(sourceBitmap,detectedQuad);status.setText(R.string.showing_original);});
        actions.addView(camera);actions.addView(gallery);actions.addView(correctButton);actions.addView(originalButton);
        preview=new DocumentPreviewView(this);preview.setLayoutParams(new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,0,1f));
        status=new TextView(this);status.setText(R.string.document_body);status.setTextSize(14);status.setPadding(0,pad,0,0);
        root.addView(title,new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,ViewGroup.LayoutParams.WRAP_CONTENT));
        root.addView(actions,new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,ViewGroup.LayoutParams.WRAP_CONTENT));
        root.addView(preview,new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,0,1f));
        root.addView(status,new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,ViewGroup.LayoutParams.WRAP_CONTENT));
        setContentView(root);
    }

    private void launchCamera(){
        try{
            File dir=new File(getCacheDir(),"captures");if(!dir.exists()&&!dir.mkdirs())throw new IOException("Cannot create capture directory");
            File file=File.createTempFile("receipt_",".jpg",dir);
            pendingCaptureUri=new Uri.Builder().scheme("content").authority(getPackageName()+".capture").appendPath(file.getName()).build();
            Intent intent=new Intent(MediaStore.ACTION_IMAGE_CAPTURE);intent.putExtra(MediaStore.EXTRA_OUTPUT,pendingCaptureUri);intent.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION|Intent.FLAG_GRANT_READ_URI_PERMISSION);intent.setClipData(ClipData.newRawUri("ReceiptLedger capture",pendingCaptureUri));
            if(intent.resolveActivity(getPackageManager())==null){Toast.makeText(this,R.string.no_camera,Toast.LENGTH_SHORT).show();return;}
            startActivityForResult(intent,REQ_CAMERA);
        }catch(IOException e){Toast.makeText(this,getString(R.string.load_failed,e.getMessage()),Toast.LENGTH_LONG).show();}
    }

    private void launchPicker(){
        Intent intent=new Intent(Intent.ACTION_OPEN_DOCUMENT);intent.addCategory(Intent.CATEGORY_OPENABLE);intent.setType("image/*");intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION|Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);startActivityForResult(intent,REQ_PICK);
    }

    @Override protected void onActivityResult(int requestCode,int resultCode,Intent data){
        super.onActivityResult(requestCode,resultCode,data);
        if(resultCode!=RESULT_OK)return;
        Uri uri=null;
        if(requestCode==REQ_CAMERA)uri=pendingCaptureUri;
        else if(requestCode==REQ_PICK&&data!=null){uri=data.getData();if(uri!=null){try{getContentResolver().takePersistableUriPermission(uri,Intent.FLAG_GRANT_READ_URI_PERMISSION);}catch(SecurityException ignored){}}}
        if(uri!=null)loadImage(uri);
    }

    private void loadImage(Uri uri){
        long ticket=++generation;status.setText(R.string.loading);correctButton.setEnabled(false);originalButton.setEnabled(false);
        worker.execute(()->{
            try{
                ImageLoader.LoadedImage loaded=ImageLoader.load(this,uri);
                BitmapLumaAdapter.Sampled sampled=BitmapLumaAdapter.sample(loaded.bitmap,480);
                DocumentDetection d=detector.detect(sampled.plane);
                Quad q=d.found?sampled.toSource(d.quad):null;
                runOnUiThread(()->{
                    if(ticket!=generation){loaded.bitmap.recycle();return;}
                    if(sourceBitmap!=null&&sourceBitmap!=loaded.bitmap)sourceBitmap.recycle();if(correctedBitmap!=null){correctedBitmap.recycle();correctedBitmap=null;}
                    sourceBitmap=loaded.bitmap;detectedQuad=q;preview.setDocument(sourceBitmap,detectedQuad);correctButton.setEnabled(q!=null);originalButton.setEnabled(false);
                    status.setText(d.found?getString(R.string.detected,d.confidence,loaded.bitmap.getWidth(),loaded.bitmap.getHeight(),loaded.exifOrientation):getString(R.string.not_detected,d.reason,loaded.bitmap.getWidth(),loaded.bitmap.getHeight()));
                });
            }catch(Exception e){runOnUiThread(()->{if(ticket==generation)status.setText(getString(R.string.load_failed,e.getMessage()));});}
        });
    }

    private void correctPerspective(){
        final Bitmap bitmap=sourceBitmap;final Quad quad=detectedQuad;if(bitmap==null||quad==null)return;long ticket=generation;status.setText(R.string.correcting);correctButton.setEnabled(false);
        worker.execute(()->{
            try{
                PerspectiveWarp.Result result=PerspectiveWarp.warp(bitmap,quad);
                runOnUiThread(()->{if(ticket!=generation){result.bitmap.recycle();return;}if(correctedBitmap!=null)correctedBitmap.recycle();correctedBitmap=result.bitmap;preview.setDocument(correctedBitmap,null);originalButton.setEnabled(true);correctButton.setEnabled(true);status.setText(getString(R.string.corrected,result.plan.outputWidth,result.plan.outputHeight));});
            }catch(Exception e){runOnUiThread(()->{if(ticket==generation){correctButton.setEnabled(true);status.setText(getString(R.string.correction_failed,e.getMessage()));}});}
        });
    }

    @Override protected void onDestroy(){generation++;worker.shutdownNow();super.onDestroy();}
    private int dp(int v){return Math.round(v*getResources().getDisplayMetrics().density);}
}
