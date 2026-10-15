package com.receiptledger.v1.archive;

import android.content.Context;import android.graphics.Bitmap;import java.io.*;import java.security.*;import java.util.*;

public final class ReceiptImageArchive {
    public static final int JPEG_QUALITY=95;private final File dir;
    public ReceiptImageArchive(Context context){dir=new File(context.getFilesDir(),"receipt-images");}
    public ArchiveEntry save(String receiptId,Bitmap bitmap) throws IOException {if(bitmap==null)throw new IllegalArgumentException("bitmap");if(!dir.exists()&&!dir.mkdirs())throw new IOException("cannot create image archive");String name=ImageArchivePolicy.fileName(receiptId);File target=new File(dir,name),temp=new File(dir,name+".tmp-"+UUID.randomUUID());try(FileOutputStream out=new FileOutputStream(temp)){if(!bitmap.compress(Bitmap.CompressFormat.JPEG,JPEG_QUALITY,out))throw new IOException("JPEG compression failed");out.flush();out.getFD().sync();}if(target.exists()&&!target.delete()){temp.delete();throw new IOException("cannot replace archived image");}if(!temp.renameTo(target)){temp.delete();throw new IOException("atomic image rename failed");}return new ArchiveEntry(target,target.length(),sha256(target));}
    public boolean exists(String receiptId){return new File(dir,ImageArchivePolicy.fileName(receiptId)).isFile();}
    public boolean delete(String receiptId){File f=new File(dir,ImageArchivePolicy.fileName(receiptId));return !f.exists()||f.delete();}
    public int reconcile(Set<String> liveIds){if(!dir.exists())return 0;int removed=0;File[] files=dir.listFiles();if(files==null)return 0;for(File f:files){String name=f.getName();if(ImageArchivePolicy.isTempName(name)){if(f.delete())removed++;continue;}String id=ImageArchivePolicy.receiptIdFromFileName(name);if(id!=null&&!liveIds.contains(id)&&f.delete())removed++;}return removed;}
    private static String sha256(File f) throws IOException {try{MessageDigest d=MessageDigest.getInstance("SHA-256");byte[] b=new byte[8192];try(InputStream in=new FileInputStream(f)){for(int n;(n=in.read(b))>=0;)if(n>0)d.update(b,0,n);}StringBuilder s=new StringBuilder();for(byte x:d.digest())s.append(String.format(Locale.ROOT,"%02x",x&255));return s.toString();}catch(NoSuchAlgorithmException e){throw new AssertionError(e);}}
    public static final class ArchiveEntry {public final File file;public final long bytes;public final String sha256;ArchiveEntry(File file,long bytes,String sha256){this.file=file;this.bytes=bytes;this.sha256=sha256;}}
}
