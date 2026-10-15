package com.receiptledger.v1.persistence;

import com.receiptledger.v1.validation.ValidationStatus;
import java.util.*;

public final class ReceiptRecord {
    public final String id;public final long createdAtMillis;public final String purchaseDate,storeName,rawOcrText;public final Long printedTotal,itemLineSum,discountSum,computedNet,difference;public final ValidationStatus validationStatus;public final int sourceWidth,sourceHeight;public final boolean perspectiveCorrected;public final List<String> issues;public final List<PersistedItem> items;
    public ReceiptRecord(String id,long createdAtMillis,String purchaseDate,String storeName,String rawOcrText,Long printedTotal,Long itemLineSum,Long discountSum,Long computedNet,Long difference,ValidationStatus validationStatus,int sourceWidth,int sourceHeight,boolean perspectiveCorrected,List<String> issues,List<PersistedItem> items){if(id==null||id.isEmpty())throw new IllegalArgumentException("id");if(sourceWidth<1||sourceHeight<1)throw new IllegalArgumentException("source dimensions");this.id=id;this.createdAtMillis=createdAtMillis;this.purchaseDate=purchaseDate;this.storeName=storeName;this.rawOcrText=rawOcrText==null?"":rawOcrText;this.printedTotal=printedTotal;this.itemLineSum=itemLineSum;this.discountSum=discountSum;this.computedNet=computedNet;this.difference=difference;this.validationStatus=validationStatus==null?ValidationStatus.INCOMPLETE:validationStatus;this.sourceWidth=sourceWidth;this.sourceHeight=sourceHeight;this.perspectiveCorrected=perspectiveCorrected;this.issues=Collections.unmodifiableList(new ArrayList<>(issues==null?Collections.emptyList():issues));this.items=Collections.unmodifiableList(new ArrayList<>(items==null?Collections.emptyList():items));}
}
