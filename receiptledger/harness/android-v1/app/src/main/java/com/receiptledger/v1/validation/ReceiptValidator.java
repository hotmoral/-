package com.receiptledger.v1.validation;

import com.receiptledger.v1.item.*;import com.receiptledger.v1.structure.*;import java.util.ArrayList;import java.util.List;

public final class ReceiptValidator {
    public ReceiptValidation validate(ReceiptStructure structure,ItemTupleResult items){
        List<String> issues=new ArrayList<>();boolean complete=true;long itemSum=0;long discountSum=0;
        if(items==null){complete=false;issues.add("ITEM_RESULT_MISSING");}else for(ItemTuple item:items.items){if(item.lineAmount==null){complete=false;issues.add("ITEM_LINE_AMOUNT_MISSING@"+item.rowIndex);}else{Long n=add(itemSum,item.lineAmount);if(n==null){complete=false;issues.add("ITEM_SUM_OVERFLOW");}else itemSum=n;}}
        if(structure==null){complete=false;issues.add("STRUCTURE_MISSING");}
        else for(StructuredRow row:structure.rows)if(row.role==RowRole.DISCOUNT){MoneyCandidate m=row.rightmostMoney();if(m==null){complete=false;issues.add("DISCOUNT_AMOUNT_MISSING@"+row.index);continue;}long effect=m.amount>0?-m.amount:m.amount;Long n=add(discountSum,effect);if(n==null){complete=false;issues.add("DISCOUNT_SUM_OVERFLOW");}else discountSum=n;}
        Long total=structure==null?null:structure.totalAmount;if(total==null){complete=false;issues.add("PRINTED_TOTAL_MISSING");}
        Long net=complete?add(itemSum,discountSum):null;if(complete&&net==null){complete=false;issues.add("NET_SUM_OVERFLOW");}
        if(!complete)return new ReceiptValidation(ValidationStatus.INCOMPLETE,itemSum,discountSum,net,total,null,issues);
        Long difference=subtract(net,total);if(difference==null){issues.add("DIFFERENCE_OVERFLOW");return new ReceiptValidation(ValidationStatus.INCOMPLETE,itemSum,discountSum,net,total,null,issues);}
        if(difference!=0){issues.add("RECEIPT_TOTAL_MISMATCH");return new ReceiptValidation(ValidationStatus.MISMATCH,itemSum,discountSum,net,total,difference,issues);}
        if(items!=null&&items.partialCount>0){issues.add("PARTIAL_ITEM_TUPLE");return new ReceiptValidation(ValidationStatus.PASS_WITH_WARNINGS,itemSum,discountSum,net,total,0L,issues);}
        return new ReceiptValidation(ValidationStatus.PASS,itemSum,discountSum,net,total,0L,issues);
    }
    private static Long add(long a,long b){if((b>0&&a>Long.MAX_VALUE-b)||(b<0&&a<Long.MIN_VALUE-b))return null;return a+b;}
    private static Long subtract(long a,long b){if(b==Long.MIN_VALUE)return a>=0?null:a-b;if((b<0&&a>Long.MAX_VALUE+b)||(b>0&&a<Long.MIN_VALUE+b))return null;return a-b;}
}
