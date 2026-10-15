package com.receiptledger.v1.persistence;

import com.receiptledger.v1.item.ItemResolution;
import com.receiptledger.v1.item.ItemTuple;
import com.receiptledger.v1.item.ValueOrigin;

public final class PersistedItem {
    public final int ordinal,rowIndex;public final String name;public final Integer quantity;public final Long unitPrice,lineAmount;public final ValueOrigin quantityOrigin,unitPriceOrigin,lineAmountOrigin;public final ItemResolution resolution;public final String reason;
    public PersistedItem(int ordinal,int rowIndex,String name,Integer quantity,Long unitPrice,Long lineAmount,ValueOrigin quantityOrigin,ValueOrigin unitPriceOrigin,ValueOrigin lineAmountOrigin,ItemResolution resolution,String reason){this.ordinal=ordinal;this.rowIndex=rowIndex;this.name=name==null?"":name;this.quantity=quantity;this.unitPrice=unitPrice;this.lineAmount=lineAmount;this.quantityOrigin=quantityOrigin==null?ValueOrigin.UNKNOWN:quantityOrigin;this.unitPriceOrigin=unitPriceOrigin==null?ValueOrigin.UNKNOWN:unitPriceOrigin;this.lineAmountOrigin=lineAmountOrigin==null?ValueOrigin.UNKNOWN:lineAmountOrigin;this.resolution=resolution==null?ItemResolution.PARTIAL:resolution;this.reason=reason;}
    public static PersistedItem from(int ordinal,ItemTuple item){return new PersistedItem(ordinal,item.rowIndex,item.name,item.quantity,item.unitPrice,item.lineAmount,item.quantityOrigin,item.unitPriceOrigin,item.lineAmountOrigin,item.resolution,item.reason);}
}
