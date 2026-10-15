package com.receiptledger.v1.price;

import com.receiptledger.v1.product.CatalogProduct;import java.util.*;

public final class PriceHistory {
 public final CatalogProduct product;public final boolean comparableTrend;public final List<PriceObservation> observations;public final Long latest,min,max,average;
 public PriceHistory(CatalogProduct product,boolean comparableTrend,List<PriceObservation> observations,Long latest,Long min,Long max,Long average){this.product=product;this.comparableTrend=comparableTrend;this.observations=Collections.unmodifiableList(new ArrayList<>(observations));this.latest=latest;this.min=min;this.max=max;this.average=average;}
}
