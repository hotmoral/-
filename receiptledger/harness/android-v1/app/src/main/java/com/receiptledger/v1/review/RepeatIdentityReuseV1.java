package com.receiptledger.v1.review;

import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;

/** Best-effort post-save reuse of already-confirmed exact aliases. */
public final class RepeatIdentityReuseV1 {
    public interface ExactAliasLinker {
        boolean link(String receiptId, int itemOrdinal, String rawName);
    }

    public static final class Result {
        public final int linkedCount;
        public final int unknownCount;
        public final int failureCount;
        Result(int linkedCount, int unknownCount, int failureCount) {
            this.linkedCount = linkedCount;
            this.unknownCount = unknownCount;
            this.failureCount = failureCount;
        }
    }

    public Result apply(ReceiptRecord receipt, ExactAliasLinker linker) {
        if (receipt == null || linker == null) throw new IllegalArgumentException("repeat reuse");
        int linked = 0;
        int unknown = 0;
        int failed = 0;
        for (PersistedItem item : receipt.items) {
            try {
                if (linker.link(receipt.id, item.ordinal, item.name)) linked++;
                else unknown++;
            } catch (RuntimeException e) {
                failed++;
            }
        }
        return new Result(linked, unknown, failed);
    }
}
