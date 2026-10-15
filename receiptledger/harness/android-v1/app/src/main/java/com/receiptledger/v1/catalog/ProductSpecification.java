package com.receiptledger.v1.catalog;

/** Packaged-product specification. Missing values remain unknown and are never defaulted. */
public final class ProductSpecification {
    public final PackageMeasure netContent;
    public final Integer packCount;
    public final PackageMeasure innerUnitContent;

    public ProductSpecification(PackageMeasure netContent, Integer packCount, PackageMeasure innerUnitContent) {
        if (packCount != null && packCount < 1) throw new IllegalArgumentException("packCount must be positive");
        if (innerUnitContent != null && packCount == null) {
            throw new IllegalArgumentException("innerUnitContent requires explicit packCount");
        }
        this.netContent = netContent;
        this.packCount = packCount;
        this.innerUnitContent = innerUnitContent;
    }

    public static ProductSpecification empty() {
        return new ProductSpecification(null, null, null);
    }

    /** Deterministic candidate descriptor only; it is never entity equality authority. */
    public String candidateToken() {
        return "NET=" + token(netContent)
                + "|PACK=" + (packCount == null ? "?" : packCount)
                + "|INNER=" + token(innerUnitContent);
    }

    private static String token(PackageMeasure measure) {
        return measure == null ? "?" : measure.canonicalToken();
    }
}
