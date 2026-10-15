package com.receiptledger.v1.product;

public final class ItemLinkRef {
 public final String receiptId;public final int itemOrdinal;public final String productId;public final LinkSource source;
 public ItemLinkRef(String receiptId,int itemOrdinal,String productId,LinkSource source){this.receiptId=receiptId;this.itemOrdinal=itemOrdinal;this.productId=productId;this.source=source;}
}
