package com.receiptledger.v1.archive;

import java.util.regex.Pattern;

public final class ImageArchivePolicy {
    private static final Pattern SAFE_ID=Pattern.compile("[A-Za-z0-9._-]{1,128}");
    private ImageArchivePolicy(){}
    public static String fileName(String receiptId){if(!isSafeId(receiptId))throw new IllegalArgumentException("unsafe receipt id");return receiptId+".jpg";}
    public static boolean isSafeId(String id){return id!=null&&SAFE_ID.matcher(id).matches()&&!id.equals(".")&&!id.equals("..");}
    public static String receiptIdFromFileName(String name){if(name==null||!name.endsWith(".jpg"))return null;String id=name.substring(0,name.length()-4);return isSafeId(id)?id:null;}
    public static boolean isTempName(String name){return name!=null&&name.contains(".tmp-");}
}
