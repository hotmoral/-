package com.receiptledger.v1.item;

import java.util.ArrayList;import java.util.Collections;import java.util.List;

public final class ItemTupleResult {
    public final List<ItemTuple> items;public final int exactCount;public final int inferredCount;public final int partialCount;
    ItemTupleResult(List<ItemTuple> items){this.items=Collections.unmodifiableList(new ArrayList<>(items));int e=0,i=0,p=0;for(ItemTuple item:items){if(item.resolution==ItemResolution.EXACT)e++;else if(item.resolution==ItemResolution.INFERRED)i++;else p++;}exactCount=e;inferredCount=i;partialCount=p;}
}
