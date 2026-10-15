package com.receiptledger.v1.item;

public final class ItemTuple {
    public final int rowIndex;
    public final String name;
    public final Integer quantity;
    public final Long unitPrice;
    public final Long lineAmount;
    public final ValueOrigin quantityOrigin;
    public final ValueOrigin unitPriceOrigin;
    public final ValueOrigin lineAmountOrigin;
    public final ItemResolution resolution;
    public final String reason;

    ItemTuple(int rowIndex,String name,Integer quantity,Long unitPrice,Long lineAmount,
              ValueOrigin quantityOrigin,ValueOrigin unitPriceOrigin,ValueOrigin lineAmountOrigin,
              ItemResolution resolution,String reason){
        this.rowIndex=rowIndex;this.name=name;this.quantity=quantity;this.unitPrice=unitPrice;this.lineAmount=lineAmount;
        this.quantityOrigin=quantityOrigin;this.unitPriceOrigin=unitPriceOrigin;this.lineAmountOrigin=lineAmountOrigin;
        this.resolution=resolution;this.reason=reason;
    }
}
