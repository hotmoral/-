package com.receiptledger.v1.catalog;

import com.receiptledger.v1.product.ProductNameNormalizer;
import java.util.Objects;

/** Namespace for a confirmed/reusable alias. CP21 defines scope only, not resolver precedence. */
public final class AliasContext {
    public enum Scope { GLOBAL, MERCHANT }

    public final Scope scope;
    public final String merchantKey;

    private AliasContext(Scope scope, String merchantKey) {
        this.scope = Objects.requireNonNull(scope, "scope");
        this.merchantKey = merchantKey;
    }

    public static AliasContext global() {
        return new AliasContext(Scope.GLOBAL, null);
    }

    public static AliasContext merchant(String merchantKey) {
        String key = ProductNameNormalizer.key(merchantKey);
        if (key.isEmpty()) throw new IllegalArgumentException("merchant key");
        return new AliasContext(Scope.MERCHANT, key);
    }

    @Override public boolean equals(Object other) {
        if (this == other) return true;
        if (!(other instanceof AliasContext)) return false;
        AliasContext that = (AliasContext) other;
        return scope == that.scope && Objects.equals(merchantKey, that.merchantKey);
    }

    @Override public int hashCode() {
        return Objects.hash(scope, merchantKey);
    }

    @Override public String toString() {
        return scope == Scope.GLOBAL ? "GLOBAL" : "MERCHANT:" + merchantKey;
    }
}
