package com.receiptledger.v1.persistence;

import java.util.List;

public interface ReceiptStore extends AutoCloseable {
    void save(ReceiptRecord record);
    ReceiptRecord get(String id);
    List<ReceiptRecord> listNewestFirst(int limit);
    int count();
    boolean delete(String id);
    @Override void close();
}
