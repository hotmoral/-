package com.receiptledger.v1.ocr;

import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.ProjectiveTransform;
import com.receiptledger.v1.document.Quad;

public final class OcrGeometryMapper {
    private OcrGeometryMapper() {}
    public static Quad map(Quad q, ProjectiveTransform transform){if(q==null)return null;return new Quad(transform.map(q.topLeft),transform.map(q.topRight),transform.map(q.bottomRight),transform.map(q.bottomLeft));}
    public static Quad rectangle(double left,double top,double right,double bottom){return new Quad(new PointD(left,top),new PointD(right,top),new PointD(right,bottom),new PointD(left,bottom));}
}
