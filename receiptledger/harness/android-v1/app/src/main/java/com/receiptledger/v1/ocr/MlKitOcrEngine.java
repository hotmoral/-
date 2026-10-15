package com.receiptledger.v1.ocr;

import android.graphics.Bitmap;
import android.graphics.Point;
import android.graphics.Rect;

import com.google.mlkit.vision.common.InputImage;
import com.google.mlkit.vision.text.Text;
import com.google.mlkit.vision.text.TextRecognition;
import com.google.mlkit.vision.text.TextRecognizer;
import com.google.mlkit.vision.text.korean.KoreanTextRecognizerOptions;
import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.ProjectiveTransform;
import com.receiptledger.v1.document.Quad;

import java.util.ArrayList;
import java.util.List;

public final class MlKitOcrEngine implements AutoCloseable {
    private final TextRecognizer recognizer=TextRecognition.getClient(new KoreanTextRecognizerOptions.Builder().build());

    public interface Callback { void onSuccess(OcrDocument document); void onFailure(Exception error); }

    public void recognize(Bitmap bitmap, ProjectiveTransform inputToSource, Callback callback){
        InputImage image=InputImage.fromBitmap(bitmap,0);
        recognizer.process(image)
                .addOnSuccessListener(text->callback.onSuccess(convert(text,bitmap.getWidth(),bitmap.getHeight(),inputToSource)))
                .addOnFailureListener(callback::onFailure);
    }

    private static OcrDocument convert(Text result,int width,int height,ProjectiveTransform inputToSource){
        List<OcrBlock> blocks=new ArrayList<>();
        for(Text.TextBlock block:result.getTextBlocks()){
            List<OcrLine> lines=new ArrayList<>();
            for(Text.Line line:block.getLines()){
                List<OcrElement> elements=new ArrayList<>();
                for(Text.Element element:line.getElements()){
                    Quad input=quad(element.getCornerPoints(),element.getBoundingBox());
                    elements.add(new OcrElement(element.getText(),input,OcrGeometryMapper.map(input,inputToSource)));
                }
                Quad input=quad(line.getCornerPoints(),line.getBoundingBox());
                lines.add(new OcrLine(line.getText(),input,OcrGeometryMapper.map(input,inputToSource),elements));
            }
            Quad input=quad(block.getCornerPoints(),block.getBoundingBox());
            blocks.add(new OcrBlock(block.getText(),input,OcrGeometryMapper.map(input,inputToSource),lines));
        }
        return new OcrDocument(result.getText(),width,height,blocks);
    }

    private static Quad quad(Point[] points,Rect rect){
        if(points!=null&&points.length>=4)return new Quad(p(points[0]),p(points[1]),p(points[2]),p(points[3]));
        if(rect==null)return null;
        return OcrGeometryMapper.rectangle(rect.left,rect.top,rect.right,rect.bottom);
    }
    private static PointD p(Point p){return new PointD(p.x,p.y);}
    @Override public void close(){recognizer.close();}
}
