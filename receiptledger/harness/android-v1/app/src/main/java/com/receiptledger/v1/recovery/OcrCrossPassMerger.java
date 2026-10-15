package com.receiptledger.v1.recovery;

import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.ocr.*;
import java.util.*;

public final class OcrCrossPassMerger {
    public OcrDocument merge(OcrDocument primary,OcrDocument supplement){
        if(primary==null||supplement==null)return null;
        List<OcrElement> base=normalized(primary),extra=normalized(supplement);
        if(base.isEmpty()||extra.isEmpty())return null;
        List<OcrElement> out=new ArrayList<>(base);
        int novel=0,maxNovel=Math.max(3,Math.min(12,base.size()/2+2));
        for(OcrElement e:extra){
            if(isDuplicate(e,out))continue;
            out.add(e);novel++;
            if(novel>maxNovel)return null;
        }
        if(novel==0)return null;
        StringBuilder raw=new StringBuilder();
        for(OcrElement e:out){if(raw.length()>0)raw.append(' ');raw.append(e.text);}
        OcrLine line=new OcrLine(raw.toString(),null,null,out);
        OcrBlock block=new OcrBlock(raw.toString(),null,null,Collections.singletonList(line));
        return new OcrDocument(raw.toString(),Math.max(primary.inputWidth,supplement.inputWidth),Math.max(primary.inputHeight,supplement.inputHeight),Collections.singletonList(block));
    }

    private static List<OcrElement> normalized(OcrDocument doc){
        List<OcrElement> out=new ArrayList<>();
        for(OcrBlock b:doc.blocks)for(OcrLine l:b.lines)for(OcrElement e:l.elements){
            String text=e.text==null?"":e.text.trim();Quad q=e.sourceQuad!=null?e.sourceQuad:e.inputQuad;
            if(text.isEmpty()||q==null)continue;
            out.add(new OcrElement(text,q,q));
        }
        return out;
    }

    private static boolean isDuplicate(OcrElement candidate,List<OcrElement> existing){
        Box a=Box.of(candidate.sourceQuad);
        for(OcrElement e:existing){
            Box b=Box.of(e.sourceQuad);
            double yTolerance=Math.max(4.0,Math.max(a.height(),b.height())*0.70);
            if(Math.abs(a.cy()-b.cy())>yTolerance)continue;
            double xOverlap=overlap(a.left,a.right,b.left,b.right)/Math.max(1.0,Math.min(a.width(),b.width()));
            double yOverlap=overlap(a.top,a.bottom,b.top,b.bottom)/Math.max(1.0,Math.min(a.height(),b.height()));
            if(xOverlap>=0.45&&yOverlap>=0.35)return true;
            if(normalizedText(candidate.text).equals(normalizedText(e.text))&&Math.abs(a.cx()-b.cx())<=Math.max(6.0,Math.max(a.width(),b.width())*0.65))return true;
        }
        return false;
    }

    private static double overlap(double a1,double a2,double b1,double b2){return Math.max(0.0,Math.min(a2,b2)-Math.max(a1,b1));}
    private static String normalizedText(String s){return s==null?"":s.replaceAll("[\\s,._-]+","").toLowerCase(Locale.ROOT);}

    private static final class Box{
        final double left,top,right,bottom;
        Box(double left,double top,double right,double bottom){this.left=left;this.top=top;this.right=right;this.bottom=bottom;}
        static Box of(Quad q){PointD[] p=q.points();double l=Double.POSITIVE_INFINITY,t=Double.POSITIVE_INFINITY,r=Double.NEGATIVE_INFINITY,b=Double.NEGATIVE_INFINITY;for(PointD x:p){l=Math.min(l,x.x);t=Math.min(t,x.y);r=Math.max(r,x.x);b=Math.max(b,x.y);}return new Box(l,t,r,b);}
        double width(){return right-left;}double height(){return bottom-top;}double cx(){return (left+right)*0.5;}double cy(){return (top+bottom)*0.5;}
    }
}
