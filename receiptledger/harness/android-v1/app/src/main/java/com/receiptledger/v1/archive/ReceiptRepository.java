package com.receiptledger.v1.archive;

import android.content.Context;import android.graphics.Bitmap;import com.receiptledger.v1.persistence.*;import java.io.IOException;import java.util.*;

public final class ReceiptRepository implements AutoCloseable {
    private final SqliteReceiptStore store;private final ReceiptImageArchive archive;
    public ReceiptRepository(Context context){store=new SqliteReceiptStore(context);archive=new ReceiptImageArchive(context);}
    public ReceiptImageArchive.ArchiveEntry save(ReceiptRecord record,Bitmap normalizedSource) throws IOException {if(store.get(record.id)!=null)throw new IllegalStateException("receipt id already exists");ReceiptImageArchive.ArchiveEntry image=archive.save(record.id,normalizedSource);try{store.save(record);return image;}catch(RuntimeException e){archive.delete(record.id);throw e;}}
    public ReceiptRecord get(String id){return store.get(id);}public List<ReceiptRecord> listNewestFirst(int limit){return store.listNewestFirst(limit);}public int count(){return store.count();}
    public int reconcileOrphans(){return archive.reconcile(store.ids());}
    public boolean delete(String id){boolean removed=store.delete(id);archive.delete(id);return removed;}
    public boolean hasImage(String id){return archive.exists(id);}
    @Override public void close(){store.close();}
}
