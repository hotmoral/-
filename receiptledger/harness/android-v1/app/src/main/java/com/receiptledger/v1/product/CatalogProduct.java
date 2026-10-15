package com.receiptledger.v1.product;

public final class CatalogProduct {
 public final String id;public final ProductType type;public final String canonicalName,canonicalKey;public final long createdAtMillis;
 public CatalogProduct(String id,ProductType type,String canonicalName,long createdAtMillis){if(id==null||id.isEmpty())throw new IllegalArgumentException("id");if(type==null||type==ProductType.UNCLASSIFIED)throw new IllegalArgumentException("classified product type required");String name=canonicalName==null?"":canonicalName.trim(),key=ProductNameNormalizer.key(name);if(key.isEmpty())throw new IllegalArgumentException("canonical name");this.id=id;this.type=type;this.canonicalName=name;this.canonicalKey=key;this.createdAtMillis=createdAtMillis;}
}
