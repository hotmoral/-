package com.receiptledger.v1.category;

import java.util.Objects;

/** Immutable node in the bounded V1 browse taxonomy. Category identity is the stable id only. */
public final class CategoryNodeV1 {
    public final String id;
    public final String parentId;
    public final String displayNameKo;

    public CategoryNodeV1(String id, String parentId, String displayNameKo) {
        this.id = required(id, "id");
        this.parentId = parentId == null ? null : required(parentId, "parentId");
        this.displayNameKo = required(displayNameKo, "displayNameKo");
        if (this.id.equals(this.parentId)) throw new IllegalArgumentException("category cannot parent itself");
    }

    public boolean isRoot() { return parentId == null; }

    @Override public boolean equals(Object other) {
        return other instanceof CategoryNodeV1 && id.equals(((CategoryNodeV1) other).id);
    }

    @Override public int hashCode() { return Objects.hash(id); }

    private static String required(String value, String name) {
        String clean = value == null ? "" : value.trim();
        if (clean.isEmpty()) throw new IllegalArgumentException(name);
        return clean;
    }
}
