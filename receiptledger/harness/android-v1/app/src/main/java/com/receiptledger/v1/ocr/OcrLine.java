package com.receiptledger.v1.ocr;

import com.receiptledger.v1.document.Quad;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class OcrLine {
    public final String text;
    public final Quad inputQuad;
    public final Quad sourceQuad;
    public final List<OcrElement> elements;

    public OcrLine(String text, Quad inputQuad, Quad sourceQuad, List<OcrElement> elements){
        this.text=text==null?"":text;this.inputQuad=inputQuad;this.sourceQuad=sourceQuad;this.elements=Collections.unmodifiableList(new ArrayList<>(elements));
    }
}
