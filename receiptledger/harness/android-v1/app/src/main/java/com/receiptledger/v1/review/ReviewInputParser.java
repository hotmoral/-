package com.receiptledger.v1.review;

import java.text.Normalizer;import java.util.regex.Pattern;

public final class ReviewInputParser {
    private static final Pattern DATE=Pattern.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}");
    private ReviewInputParser(){}
    public static Long nullableMoney(String text){String s=clean(text);if(s.isEmpty())return null;try{return Long.valueOf(s);}catch(NumberFormatException e){throw new IllegalArgumentException("금액 형식이 올바르지 않습니다: "+text);}}
    public static Integer nullableQuantity(String text){String s=clean(text);if(s.isEmpty())return null;try{return Integer.valueOf(s);}catch(NumberFormatException e){throw new IllegalArgumentException("수량 형식이 올바르지 않습니다: "+text);}}
    public static String nullableDate(String text){String s=text==null?"":Normalizer.normalize(text,Normalizer.Form.NFKC).trim();if(s.isEmpty())return null;if(!DATE.matcher(s).matches())throw new IllegalArgumentException("날짜는 YYYY-MM-DD 형식이어야 합니다.");int y=Integer.parseInt(s.substring(0,4)),m=Integer.parseInt(s.substring(5,7)),d=Integer.parseInt(s.substring(8,10));if(y<2000||y>2199||m<1||m>12||d<1||d>days(y,m))throw new IllegalArgumentException("존재하지 않는 날짜입니다: "+s);return s;}
    private static String clean(String text){if(text==null)return "";return Normalizer.normalize(text,Normalizer.Form.NFKC).replace(",","").replace("원","").replaceAll("\\s+","").trim();}
    private static int days(int y,int m){int[] a={31,28,31,30,31,30,31,31,30,31,30,31};if(m==2&&((y%4==0&&y%100!=0)||y%400==0))return 29;return a[m-1];}
}
