package com.receiptledger.v1.review;

public final class ReviewItemInput {
    public final String name;public final Integer quantity;public final Long unitPrice,lineAmount;
    public ReviewItemInput(String name,Integer quantity,Long unitPrice,Long lineAmount){this.name=name;this.quantity=quantity;this.unitPrice=unitPrice;this.lineAmount=lineAmount;}
}
