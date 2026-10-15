package com.receiptledger.v1.ocr;

import com.receiptledger.v1.document.Quad;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class OcrDocument {
    public final String rawText;
    public final int inputWidth;
    public final int inputHeight;
    public final List<OcrBlock> blocks;

    public OcrDocument(String rawText,int inputWidth,int inputHeight,List<OcrBlock> blocks){
        this.rawText=rawText==null?"":rawText;this.inputWidth=inputWidth;this.inputHeight=inputHeight;this.blocks=Collections.unmodifiableList(new ArrayList<>(blocks));
    }

    public int lineCount(){int n=0;for(OcrBlock b:blocks)n+=b.lines.size();return n;}
    public int elementCount(){int n=0;for(OcrBlock b:blocks)for(OcrLine l:b.lines)n+=l.elements.size();return n;}
    public List<Quad> inputElementQuads(){List<Quad> out=new ArrayList<>();for(OcrBlock b:blocks)for(OcrLine l:b.lines)for(OcrElement e:l.elements)if(e.inputQuad!=null)out.add(e.inputQuad);return out;}
}
