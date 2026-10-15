package com.receiptledger.v1.validation;

import java.util.ArrayList;import java.util.Collections;import java.util.List;

public final class ReceiptValidation {
    public final ValidationStatus status;public final Long itemLineSum;public final Long discountSum;public final Long computedNet;public final Long printedTotal;public final Long difference;public final List<String> issues;
    ReceiptValidation(ValidationStatus status,Long itemLineSum,Long discountSum,Long computedNet,Long printedTotal,Long difference,List<String> issues){this.status=status;this.itemLineSum=itemLineSum;this.discountSum=discountSum;this.computedNet=computedNet;this.printedTotal=printedTotal;this.difference=difference;this.issues=Collections.unmodifiableList(new ArrayList<>(issues));}
}
