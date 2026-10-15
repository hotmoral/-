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
import com.receiptledger.v1.document.PerspectivePlan;
import com.receiptledger.v1.document.ProjectiveTransform;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.document.ReceiptDocumentDetector;
import com.receiptledger.v1.image.BitmapLumaAdapter;
import com.receiptledger.v1.image.ImageLoader;
import com.receiptledger.v1.image.PerspectiveWarp;
import com.receiptledger.v1.ocr.MlKitOcrEngine;
import com.receiptledger.v1.ocr.OcrDocument;
import com.receiptledger.v1.ui.DocumentPreviewView;

import java.io.File;
import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class MainActivity extends Activity {
    private static final int REQ_CAMERA=1001,REQ_PICK=1002;
    private final ExecutorService worker=Executors.newSingleThreadExecutor();
    private final ReceiptDocumentDetector detector=new ReceiptDocumentDetector();
    private final MlKitOcrEngine ocrEngine=new MlKitOcrEngine();
    private DocumentPreviewView preview;private TextView status,ocrText;private Button correctButton,originalButton,ocrButton;
    private Uri pendingCaptureUri;private Bitmap sourceBitmap,correctedBitmap,displayBitmap;private Quad detectedQuad;private PerspectivePlan correctedPlan;private ProjectiveTransform displayToSource=ProjectiveTransform.identity();
    private long generation,displayRevision;

    @Override protected void onCreate(Bundle savedInstanceState){super.onCreate(savedInstanceState);int pad=dp(12);LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(pad,pad,pad,pad);root.setGravity(Gravity.CENTER_HORIZONTAL);TextView title=new TextView(this);title.setText(R.string.document_title);title.setTextSize(23);title.setGravity(Gravity.CENTER);LinearLayout actions=new LinearLayout(this);actions.setOrientation(LinearLayout.HORIZONTAL);actions.setGravity(Gravity.CENTER);Button camera=button(R.string.capture,v->launchCamera());Button gallery=button(R.string.gallery,v->launchPicker());correctButton=button(R.string.correct,v->correctPerspective());originalButton=button(R.string.original,v->showOriginal());ocrButton=button(R.string.run_ocr,v->runOcr());correctButton.setEnabled(false);originalButton.setEnabled(false);ocrButton.setEnabled(false);actions.addView(camera);actions.addView(gallery);actions.addView(correctButton);actions.addView(originalButton);actions.addView(ocrButton);preview=new DocumentPreviewView(this);status=new TextView(this);status.setText(R.string.ocr_body);status.setTextSize(14);status.setPadding(0,pad,0,0);ocrText=new TextView(this);ocrText.setTextSize(13);ocrText.setMaxLines(6);ocrText.setTextIsSelectable(true);ocrText.setPadding(0,dp(8),0,0);root.addView(title,new LinearLayout.LayoutParams(-1,-2));root.addView(actions,new LinearLayout.LayoutParams(-1,-2));root.addView(preview,new LinearLayout.LayoutParams(-1,0,1f));root.addView(status,new LinearLayout.LayoutParams(-1,-2));root.addView(ocrText,new LinearLayout.LayoutParams(-1,-2));setContentView(root);}
    private Button button(int text,android.view.View.OnClickListener listener){Button b=new Button(this);b.setText(text);b.setOnClickListener(listener);return b;}

    private void launchCamera(){try{File dir=new File(getCacheDir(),"captures");if(!dir.exists()&&!dir.mkdirs())throw new IOException("Cannot create capture directory");File file=File.createTempFile("receipt_",".jpg",dir);pendingCaptureUri=new Uri.Builder().scheme("content").authority(getPackageName()+".capture").appendPath(file.getName()).build();Intent i=new Intent(MediaStore.ACTION_IMAGE_CAPTURE);i.putExtra(MediaStore.EXTRA_OUTPUT,pendingCaptureUri);i.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION|Intent.FLAG_GRANT_READ_URI_PERMISSION);i.setClipData(ClipData.newRawUri("ReceiptLedger capture",pendingCaptureUri));if(i.resolveActivity(getPackageManager())==null){Toast.makeText(this,R.string.no_camera,Toast.LENGTH_SHORT).show();return;}startActivityForResult(i,REQ_CAMERA);}catch(IOException e){Toast.makeText(this,getString(R.string.load_failed,e.getMessage()),Toast.LENGTH_LONG).show();}}
    private void launchPicker(){Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.addCategory(Intent.CATEGORY_OPENABLE);i.setType("image/*");i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION|Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);startActivityForResult(i,REQ_PICK);}
    @Override protected void onActivityResult(int requestCode,int resultCode,Intent data){super.onActivityResult(requestCode,resultCode,data);if(resultCode!=RESULT_OK)return;Uri uri=null;if(requestCode==REQ_CAMERA)uri=pendingCaptureUri;else if(requestCode==REQ_PICK&&data!=null){uri=data.getData();if(uri!=null)try{getContentResolver().takePersistableUriPermission(uri,Intent.FLAG_GRANT_READ_URI_PERMISSION);}catch(SecurityException ignored){}}if(uri!=null)loadImage(uri);}

    private void loadImage(Uri uri){long ticket=++generation;displayRevision++;status.setText(R.string.loading);ocrText.setText("");correctButton.setEnabled(false);originalButton.setEnabled(false);ocrButton.setEnabled(false);worker.execute(()->{try{ImageLoader.LoadedImage loaded=ImageLoader.load(this,uri);BitmapLumaAdapter.Sampled sampled=BitmapLumaAdapter.sample(loaded.bitmap,480);DocumentDetection d=detector.detect(sampled.plane);Quad q=d.found?sampled.toSource(d.quad):null;runOnUiThread(()->{if(ticket!=generation){loaded.bitmap.recycle();return;}if(sourceBitmap!=null&&sourceBitmap!=loaded.bitmap)sourceBitmap.recycle();if(correctedBitmap!=null){correctedBitmap.recycle();correctedBitmap=null;}sourceBitmap=loaded.bitmap;correctedPlan=null;detectedQuad=q;displayBitmap=sourceBitmap;displayToSource=ProjectiveTransform.identity();displayRevision++;preview.setDocument(sourceBitmap,detectedQuad);correctButton.setEnabled(q!=null);originalButton.setEnabled(false);ocrButton.setEnabled(true);status.setText(d.found?getString(R.string.detected,d.confidence,loaded.bitmap.getWidth(),loaded.bitmap.getHeight(),loaded.exifOrientation):getString(R.string.not_detected,d.reason,loaded.bitmap.getWidth(),loaded.bitmap.getHeight()));});}catch(Exception e){runOnUiThread(()->{if(ticket==generation)status.setText(getString(R.string.load_failed,e.getMessage()));});}});}

    private void correctPerspective(){final Bitmap bitmap=sourceBitmap;final Quad quad=detectedQuad;if(bitmap==null||quad==null)return;long ticket=generation;status.setText(R.string.correcting);correctButton.setEnabled(false);worker.execute(()->{try{PerspectiveWarp.Result result=PerspectiveWarp.warp(bitmap,quad);runOnUiThread(()->{if(ticket!=generation){result.bitmap.recycle();return;}if(correctedBitmap!=null)correctedBitmap.recycle();correctedBitmap=result.bitmap;correctedPlan=result.plan;displayBitmap=correctedBitmap;displayToSource=correctedPlan.outputToSource;displayRevision++;preview.setDocument(correctedBitmap,null);ocrText.setText("");originalButton.setEnabled(true);correctButton.setEnabled(true);ocrButton.setEnabled(true);status.setText(getString(R.string.corrected,result.plan.outputWidth,result.plan.outputHeight));});}catch(Exception e){runOnUiThread(()->{if(ticket==generation){correctButton.setEnabled(true);status.setText(getString(R.string.correction_failed,e.getMessage()));}});}});}
    private void showOriginal(){if(sourceBitmap==null)return;displayBitmap=sourceBitmap;displayToSource=ProjectiveTransform.identity();displayRevision++;preview.setDocument(sourceBitmap,detectedQuad);ocrText.setText("");status.setText(R.string.showing_original);ocrButton.setEnabled(true);}

    private void runOcr(){final Bitmap input=displayBitmap;if(input==null)return;final ProjectiveTransform mapper=displayToSource;final long imageTicket=generation,viewTicket=displayRevision;ocrButton.setEnabled(false);status.setText(R.string.ocr_running);preview.setOcrQuads(null);ocrEngine.recognize(input,mapper,new MlKitOcrEngine.Callback(){@Override public void onSuccess(OcrDocument doc){if(imageTicket!=generation||viewTicket!=displayRevision)return;ocrButton.setEnabled(true);preview.setOcrQuads(doc.inputElementQuads());ocrText.setText(doc.rawText);status.setText(getString(R.string.ocr_done,doc.blocks.size(),doc.lineCount(),doc.elementCount(),doc.rawText.length()));}@Override public void onFailure(Exception error){if(imageTicket!=generation||viewTicket!=displayRevision)return;ocrButton.setEnabled(true);status.setText(getString(R.string.ocr_failed,error.getMessage()));}});}

    @Override protected void onDestroy(){generation++;displayRevision++;worker.shutdownNow();ocrEngine.close();super.onDestroy();}
    private int dp(int v){return Math.round(v*getResources().getDisplayMetrics().density);}
}
