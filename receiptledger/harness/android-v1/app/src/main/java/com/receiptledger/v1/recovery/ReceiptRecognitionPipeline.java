package com.receiptledger.v1.recovery;

import com.receiptledger.v1.item.*;import com.receiptledger.v1.layout.*;import com.receiptledger.v1.ocr.OcrDocument;import com.receiptledger.v1.structure.*;import com.receiptledger.v1.validation.*;

public final class ReceiptRecognitionPipeline {
 private final ReceiptLayoutAnalyzer layout=new ReceiptLayoutAnalyzer();private final ReceiptStructureAnalyzer structure=new ReceiptStructureAnalyzer();private final ItemTupleSolver items=new ItemTupleSolver();private final ReceiptValidator validator=new ReceiptValidator();private final RecognitionQualityScorer scorer=new RecognitionQualityScorer();private final OcrCrossPassMerger merger=new OcrCrossPassMerger();
 public RecognitionCandidate evaluate(RecognitionPass pass,OcrDocument doc){ReceiptLayout l=layout.analyze(doc);ReceiptStructure s=structure.analyze(l);ItemTupleResult i=items.solve(s);ReceiptValidation v=validator.validate(s,i);QualitySignals signals=new QualitySignals(doc.rawText.length(),doc.elementCount(),i.items.size(),i.partialCount,s.date!=null,s.totalAmount!=null,v.status);return new RecognitionCandidate(pass,doc,l,s,i,v,signals,scorer.score(signals));}
 public boolean needsRecovery(RecognitionCandidate c){return scorer.needsRecovery(c.signals);}
 public RecognitionCandidate better(RecognitionCandidate a,RecognitionCandidate b){return b!=null&&b.score>a.score?b:a;}
 public RecognitionCandidate mergeCandidate(RecognitionCandidate a,RecognitionCandidate b){if(a==null||b==null)return null;OcrDocument doc=merger.merge(a.document,b.document);return doc==null?null:evaluate(RecognitionPass.MERGED,doc);}
 public boolean shouldAcceptMerged(RecognitionCandidate current,RecognitionCandidate merged){return merged!=null&&rank(merged.validation.status)>=rank(current.validation.status)&&merged.score>=current.score+3;}
 private static int rank(ValidationStatus s){switch(s){case PASS:return 3;case PASS_WITH_WARNINGS:return 2;case MISMATCH:return 1;default:return 0;}}
}
