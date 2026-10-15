package com.receiptledger.v1.recovery;
import com.receiptledger.v1.validation.ValidationStatus;
public final class QualitySignals {public final int chars,elements,itemCount,partialCount;public final boolean hasDate,hasTotal;public final ValidationStatus validation;public QualitySignals(int chars,int elements,int itemCount,int partialCount,boolean hasDate,boolean hasTotal,ValidationStatus validation){this.chars=chars;this.elements=elements;this.itemCount=itemCount;this.partialCount=partialCount;this.hasDate=hasDate;this.hasTotal=hasTotal;this.validation=validation;}}
