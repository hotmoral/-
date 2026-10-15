package com.receiptledger.v1.archive;

import org.junit.Test;import static org.junit.Assert.*;

public class ImageArchivePolicyTest {
    @Test public void safeReceiptIdsRoundTrip(){String id="0f8a2b8e-1234-4abc-9def-0123456789ab";String file=ImageArchivePolicy.fileName(id);assertEquals(id+".jpg",file);assertEquals(id,ImageArchivePolicy.receiptIdFromFileName(file));}
    @Test public void traversalAndForeignFilesRejected(){assertFalse(ImageArchivePolicy.isSafeId("../secret"));assertFalse(ImageArchivePolicy.isSafeId("a/b"));assertNull(ImageArchivePolicy.receiptIdFromFileName("notes.txt"));try{ImageArchivePolicy.fileName("../x");fail();}catch(IllegalArgumentException expected){}}
    @Test public void tempNamesDetected(){assertTrue(ImageArchivePolicy.isTempName("abc.jpg.tmp-123"));assertFalse(ImageArchivePolicy.isTempName("abc.jpg"));}
}
