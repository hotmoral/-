package com.receiptledger.v1.product;

import java.util.List;

public interface ProductCatalogStore extends AutoCloseable {
 IdentityResolution confirm(String receiptId,int itemOrdinal,String rawAlias,ProductType type,String canonicalName,long now);
 IdentityResolution resolveAndLinkExact(String receiptId,int itemOrdinal,String rawAlias);
 IdentityResolution itemResolution(String receiptId,int itemOrdinal);
 List<CatalogProduct> listProducts();
 void unlinkItem(String receiptId,int itemOrdinal);
 void unlinkReceipt(String receiptId);
 @Override void close();
}
