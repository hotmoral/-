package com.receiptledger.v1.ui;

import com.receiptledger.v1.persistence.*;import java.text.*;import java.util.*;

public final class ReceiptDisplayFormatter {
    private ReceiptDisplayFormatter(){}
    public static String summary(ReceiptRecord r){String date=r.purchaseDate==null?"날짜 미인식":r.purchaseDate;String total=r.printedTotal==null?"합계 ?":money(r.printedTotal)+"원";return date+"  ·  "+total+"  ·  "+r.items.size()+"개  ·  "+r.validationStatus;}
    public static String detail(ReceiptRecord r){StringBuilder s=new StringBuilder();s.append("날짜: ").append(r.purchaseDate==null?"미인식":r.purchaseDate).append('\n').append("합계: ").append(r.printedTotal==null?"?":money(r.printedTotal)+"원").append('\n').append("검증: ").append(r.validationStatus).append(" · diff=").append(r.difference).append('\n').append("이미지: ").append(r.sourceWidth).append('×').append(r.sourceHeight).append(r.perspectiveCorrected?" · 보정 OCR":" · 원본 OCR").append("\n\n상품\n");for(PersistedItem i:r.items)s.append("• ").append(i.name).append(" | q=").append(i.quantity).append(" | unit=").append(i.unitPrice).append(" | amount=").append(i.lineAmount).append(" [").append(i.resolution).append("]\n");if(!r.issues.isEmpty()){s.append("\n검증 이슈\n");for(String issue:r.issues)s.append("• ").append(issue).append('\n');}return s.toString();}
    private static String money(long value){return NumberFormat.getIntegerInstance(Locale.KOREA).format(value);}
}
