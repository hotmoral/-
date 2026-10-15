package com.receiptledger.v1.product;
import org.junit.Test;import static org.junit.Assert.*;
public class ProductNameNormalizerTest {@Test public void normalizationIsConservative(){assertEquals("서울우유 1L",ProductNameNormalizer.key("  서울우유   1l "));assertNotEquals(ProductNameNormalizer.key("서울우유1L"),ProductNameNormalizer.key("서울우유 1L"));assertEquals("ABC 1KG",ProductNameNormalizer.key("Ａｂｃ 1kg"));}}
