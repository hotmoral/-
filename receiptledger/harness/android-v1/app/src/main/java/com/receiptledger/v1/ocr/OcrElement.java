package com.receiptledger.v1.ocr;

import com.receiptledger.v1.document.Quad;

public final class OcrElement {
    public final String text;
    public final Quad inputQuad;
    public final Quad sourceQuad;

    public OcrElement(String text, Quad inputQuad, Quad sourceQuad) {
        this.text=text==null?"":text;
        this.inputQuad=inputQuad;
        this.sourceQuad=sourceQuad;
    }
}
