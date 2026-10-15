package com.receiptledger.v1.catalog;

import java.util.Objects;

/** Stable category reference only; taxonomy/hierarchy belongs to CP25. */
public final class CategoryRef {
    public final String id;

    public CategoryRef(String id) {
        String value = id == null ? "" : id.trim();
        if (value.isEmpty()) throw new IllegalArgumentException("category id");
        this.id = value;
    }

    @Override public boolean equals(Object other) {
        return other instanceof CategoryRef && id.equals(((CategoryRef) other).id);
    }

    @Override public int hashCode() {
        return Objects.hash(id);
    }

    @Override public String toString() {
        return id;
    }
}
