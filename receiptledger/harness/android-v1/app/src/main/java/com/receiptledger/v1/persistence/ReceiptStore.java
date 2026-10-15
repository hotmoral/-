package com.receiptledger.v1.persistence;

import java.util.List;import java.util.Set;

public interface ReceiptStore extends AutoCloseable {
    void save(ReceiptRecord record);
    ReceiptRecord get(String id);
    List<ReceiptRecord> listNewestFirst(int limit);
    Set<String> ids();
    int count();
    boolean delete(String id);
    @Override void close();
}
