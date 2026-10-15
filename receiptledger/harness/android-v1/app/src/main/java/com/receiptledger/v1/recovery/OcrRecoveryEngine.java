package com.receiptledger.v1.recovery;

import android.graphics.Bitmap;
import android.os.Handler;
import android.os.Looper;
import com.receiptledger.v1.document.ProjectiveTransform;
import com.receiptledger.v1.ocr.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;

public final class OcrRecoveryEngine implements AutoCloseable {
    public static final int MAX_PASSES=3;
    private final MlKitOcrEngine ocr=new MlKitOcrEngine();
    private final ReceiptRecognitionPipeline pipeline=new ReceiptRecognitionPipeline();
    private final ExecutorService prep=Executors.newSingleThreadExecutor();
    private final AtomicLong sequence=new AtomicLong();
    private final Handler main=new Handler(Looper.getMainLooper());

    public interface Callback { void onSuccess(RecoveryResult result); void onFailure(Exception error); }

    public void cancelPending(){sequence.incrementAndGet();}

    public void recognize(Bitmap input,ProjectiveTransform inputToSource,Callback callback){
        long id=sequence.incrementAndGet();
        ocr.recognize(input,inputToSource,new MlKitOcrEngine.Callback(){
            @Override public void onSuccess(OcrDocument doc){
                if(id!=sequence.get())return;
                RecognitionCandidate original=pipeline.evaluate(RecognitionPass.ORIGINAL,doc);
                List<PassDiagnostic> ds=new ArrayList<>();
                ds.add(new PassDiagnostic(original));
                if(!pipeline.needsRecovery(original)){
                    deliverSuccess(id,new RecoveryResult(original,ds),callback);
                    return;
                }
                prepareRecovery(id,input,inputToSource,original,ds,callback);
            }
            @Override public void onFailure(Exception e){deliverFailure(id,e,callback);}
        });
    }

    private void prepareRecovery(long id,Bitmap input,ProjectiveTransform mapper,RecognitionCandidate original,List<PassDiagnostic> ds,Callback cb){
        prep.execute(()->{
            if(id!=sequence.get())return;
            ReceiptImagePreprocessor.PreparedImage prepared;
            try{
                prepared=ReceiptImagePreprocessor.prepareContrast(input,mapper);
            }catch(OutOfMemoryError|RuntimeException e){
                deliverSuccess(id,new RecoveryResult(original,ds),cb);
                return;
            }
            if(id!=sequence.get()){
                recycle(prepared.bitmap);
                return;
            }
            runContrast(id,prepared,original,ds,cb);
        });
    }

    private void runContrast(long id,ReceiptImagePreprocessor.PreparedImage prepared,RecognitionCandidate best,List<PassDiagnostic> ds,Callback cb){
        ocr.recognize(prepared.bitmap,prepared.inputToSource,new MlKitOcrEngine.Callback(){
            @Override public void onSuccess(OcrDocument doc){
                if(id!=sequence.get()){
                    recycle(prepared.bitmap);
                    return;
                }
                RecognitionCandidate candidate=pipeline.evaluate(RecognitionPass.CONTRAST,doc);
                RecognitionCandidate next=pipeline.better(best,candidate);
                ds.add(new PassDiagnostic(candidate));
                if(!pipeline.needsRecovery(next)||ds.size()>=MAX_PASSES){
                    recycle(prepared.bitmap);
                    deliverSuccess(id,new RecoveryResult(next,ds),cb);
                    return;
                }
                prep.execute(()->{
                    if(id!=sequence.get()){
                        recycle(prepared.bitmap);
                        return;
                    }
                    try{
                        ReceiptImagePreprocessor.adaptiveBinaryInPlace(prepared.bitmap);
                    }catch(OutOfMemoryError|RuntimeException e){
                        recycle(prepared.bitmap);
                        deliverSuccess(id,new RecoveryResult(next,ds),cb);
                        return;
                    }
                    runBinary(id,prepared,next,ds,cb);
                });
            }

            @Override public void onFailure(Exception ignored){
                if(id!=sequence.get()){
                    recycle(prepared.bitmap);
                    return;
                }
                prep.execute(()->{
                    if(id!=sequence.get()){
                        recycle(prepared.bitmap);
                        return;
                    }
                    try{
                        ReceiptImagePreprocessor.adaptiveBinaryInPlace(prepared.bitmap);
                        runBinary(id,prepared,best,ds,cb);
                    }catch(OutOfMemoryError|RuntimeException e){
                        recycle(prepared.bitmap);
                        deliverSuccess(id,new RecoveryResult(best,ds),cb);
                    }
                });
            }
        });
    }

    private void runBinary(long id,ReceiptImagePreprocessor.PreparedImage prepared,RecognitionCandidate best,List<PassDiagnostic> ds,Callback cb){
        ocr.recognize(prepared.bitmap,prepared.inputToSource,new MlKitOcrEngine.Callback(){
            @Override public void onSuccess(OcrDocument doc){
                if(id!=sequence.get()){
                    recycle(prepared.bitmap);
                    return;
                }
                RecognitionCandidate candidate=pipeline.evaluate(RecognitionPass.BINARY,doc);
                RecognitionCandidate next=pipeline.better(best,candidate);
                ds.add(new PassDiagnostic(candidate));
                recycle(prepared.bitmap);
                deliverSuccess(id,new RecoveryResult(next,ds),cb);
            }
            @Override public void onFailure(Exception ignored){
                recycle(prepared.bitmap);
                deliverSuccess(id,new RecoveryResult(best,ds),cb);
            }
        });
    }

    private void deliverSuccess(long id,RecoveryResult result,Callback cb){
        main.post(()->{if(id==sequence.get())cb.onSuccess(result);});
    }

    private void deliverFailure(long id,Exception error,Callback cb){
        main.post(()->{if(id==sequence.get())cb.onFailure(error);});
    }

    private static void recycle(Bitmap bitmap){
        if(bitmap!=null&&!bitmap.isRecycled())bitmap.recycle();
    }

    @Override public void close(){
        cancelPending();
        prep.shutdownNow();
        ocr.close();
    }
}
