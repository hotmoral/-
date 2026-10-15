package com.receiptledger.v1.product;

public final class IdentityResolution {
 public final ProductType type;public final CatalogProduct product;public final LinkSource source;
 private IdentityResolution(ProductType type,CatalogProduct product,LinkSource source){this.type=type;this.product=product;this.source=source;}
 public static IdentityResolution unclassified(){return new IdentityResolution(ProductType.UNCLASSIFIED,null,null);}public static IdentityResolution linked(CatalogProduct p,LinkSource s){return new IdentityResolution(p.type,p,s);}public boolean classified(){return product!=null;}
}
