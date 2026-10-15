package com.receiptledger.v1.ocr;

import com.receiptledger.v1.document.Quad;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class OcrBlock {
    public final String text;
    public final Quad inputQuad;
    public final Quad sourceQuad;
    public final List<OcrLine> lines;

    public OcrBlock(String text, Quad inputQuad, Quad sourceQuad, List<OcrLine> lines){
        this.text=text==null?"":text;this.inputQuad=inputQuad;this.sourceQuad=sourceQuad;this.lines=Collections.unmodifiableList(new ArrayList<>(lines));
    }
}
