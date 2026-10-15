package com.receiptledger.v1.price;

import com.receiptledger.v1.item.ValueOrigin;import com.receiptledger.v1.product.LinkSource;import com.receiptledger.v1.validation.ValidationStatus;

public final class PriceObservation {
 public final String receiptId,purchaseDate,storeName,rawItemName;public final long createdAtMillis,unitPrice;public final Integer quantity;public final Long lineAmount;public final ValueOrigin priceOrigin;public final LinkSource linkSource;public final ValidationStatus receiptValidation;
 public PriceObservation(String receiptId,String purchaseDate,long createdAtMillis,String rawItemName,long unitPrice,Integer quantity,Long lineAmount,ValueOrigin priceOrigin,LinkSource linkSource,ValidationStatus receiptValidation){this(receiptId,purchaseDate,null,createdAtMillis,rawItemName,unitPrice,quantity,lineAmount,priceOrigin,linkSource,receiptValidation);}
 public PriceObservation(String receiptId,String purchaseDate,String storeName,long createdAtMillis,String rawItemName,long unitPrice,Integer quantity,Long lineAmount,ValueOrigin priceOrigin,LinkSource linkSource,ValidationStatus receiptValidation){this.receiptId=receiptId;this.purchaseDate=purchaseDate;this.storeName=storeName;this.createdAtMillis=createdAtMillis;this.rawItemName=rawItemName;this.unitPrice=unitPrice;this.quantity=quantity;this.lineAmount=lineAmount;this.priceOrigin=priceOrigin;this.linkSource=linkSource;this.receiptValidation=receiptValidation;}
}
