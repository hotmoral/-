package com.receiptledger.v1.product;

import java.text.Normalizer;import java.util.Locale;

public final class ProductNameNormalizer {
 private ProductNameNormalizer(){}
 public static String key(String raw){if(raw==null)return "";String s=Normalizer.normalize(raw,Normalizer.Form.NFKC).trim().replaceAll("\\s+"," ");return s.toUpperCase(Locale.ROOT);}
}
