package com.receiptledger.v1.recovery;

import com.receiptledger.v1.item.*;import com.receiptledger.v1.layout.*;import com.receiptledger.v1.ocr.OcrDocument;import com.receiptledger.v1.structure.*;import com.receiptledger.v1.validation.*;

public final class ReceiptRecognitionPipeline {
 private final ReceiptLayoutAnalyzer layout=new ReceiptLayoutAnalyzer();private final ReceiptStructureAnalyzer structure=new ReceiptStructureAnalyzer();private final ItemTupleSolver items=new ItemTupleSolver();private final ReceiptValidator validator=new ReceiptValidator();private final RecognitionQualityScorer scorer=new RecognitionQualityScorer();
 public RecognitionCandidate evaluate(RecognitionPass pass,OcrDocument doc){ReceiptLayout l=layout.analyze(doc);ReceiptStructure s=structure.analyze(l);ItemTupleResult i=items.solve(s);ReceiptValidation v=validator.validate(s,i);QualitySignals signals=new QualitySignals(doc.rawText.length(),doc.elementCount(),i.items.size(),i.partialCount,s.date!=null,s.totalAmount!=null,v.status);return new RecognitionCandidate(pass,doc,l,s,i,v,signals,scorer.score(signals));}
 public boolean needsRecovery(RecognitionCandidate c){return scorer.needsRecovery(c.signals);}
 public RecognitionCandidate better(RecognitionCandidate a,RecognitionCandidate b){return b!=null&&b.score>a.score?b:a;}
}
