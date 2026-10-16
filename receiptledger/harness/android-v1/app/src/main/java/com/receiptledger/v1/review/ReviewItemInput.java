package com.receiptledger.v1.review;

public final class ReviewItemInput {
    public final String name;
    public final Integer quantity;
    public final Long unitPrice,lineAmount;
    public final boolean removed;

    public ReviewItemInput(String name,Integer quantity,Long unitPrice,Long lineAmount){
        this(name,quantity,unitPrice,lineAmount,false);
    }

    private ReviewItemInput(String name,Integer quantity,Long unitPrice,Long lineAmount,boolean removed){
        this.name=name;
        this.quantity=quantity;
        this.unitPrice=unitPrice;
        this.lineAmount=lineAmount;
        this.removed=removed;
    }

    public static ReviewItemInput removed(){
        return new ReviewItemInput(null,null,null,null,true);
    }
}
