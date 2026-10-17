package com.receiptledger.v1.persistence;

import com.receiptledger.v1.devicevalidation.CandidateStructureDiagnosticsV1;import com.receiptledger.v1.item.*;import com.receiptledger.v1.ocr.OcrDocument;import com.receiptledger.v1.structure.*;import com.receiptledger.v1.validation.*;import java.util.*;

public final class ReceiptRecordFactory {
    private ReceiptRecordFactory(){}
    public static ReceiptRecord create(String id,long createdAt,OcrDocument doc,ReceiptStructure structure,ItemTupleResult tupleResult,ReceiptValidation validation,int sourceWidth,int sourceHeight,boolean corrected){List<PersistedItem> items=new ArrayList<>();for(int i=0;i<tupleResult.items.size();i++)items.add(PersistedItem.from(i,tupleResult.items.get(i)));String date=null;if(structure.date!=null)date=String.format(Locale.ROOT,"%04d-%02d-%02d",structure.date.year,structure.date.month,structure.date.day);String storeName=ReceiptMerchantResolver.resolve(structure);ReceiptRecord record=new ReceiptRecord(id,createdAt,date,storeName,doc==null?"":doc.rawText,validation.printedTotal,validation.itemLineSum,validation.discountSum,validation.computedNet,validation.difference,validation.status,sourceWidth,sourceHeight,corrected,validation.issues,items);CandidateStructureDiagnosticsV1.publishForReceipt(id,structure,tupleResult);return record;}
}
