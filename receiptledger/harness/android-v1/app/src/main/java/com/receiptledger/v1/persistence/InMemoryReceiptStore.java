package com.receiptledger.v1.persistence;

import java.util.*;

public final class InMemoryReceiptStore implements ReceiptStore {
    private final Map<String,ReceiptRecord> records=new HashMap<>();
    public synchronized void save(ReceiptRecord record){if(record==null)throw new IllegalArgumentException("record");records.put(record.id,record);}
    public synchronized ReceiptRecord get(String id){return records.get(id);}
    public synchronized List<ReceiptRecord> listNewestFirst(int limit){if(limit<1)return Collections.emptyList();List<ReceiptRecord> out=new ArrayList<>(records.values());Collections.sort(out,(a,b)->{int c=Long.compare(b.createdAtMillis,a.createdAtMillis);return c!=0?c:b.id.compareTo(a.id);});if(out.size()>limit)out=new ArrayList<>(out.subList(0,limit));return Collections.unmodifiableList(out);}
    public synchronized Set<String> ids(){return Collections.unmodifiableSet(new HashSet<>(records.keySet()));}
    public synchronized int count(){return records.size();}
    public synchronized boolean delete(String id){return records.remove(id)!=null;}
    public void close(){}
}
