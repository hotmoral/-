package com.receiptledger.v1.price;

import java.text.NumberFormat;import java.util.Locale;

public final class PriceHistoryFormatter {
 private PriceHistoryFormatter(){}public static String format(PriceHistory h){StringBuilder s=new StringBuilder().append(h.product.canonicalName).append(" [").append(h.product.type).append("]\n");if(h.observations.isEmpty())return s.append("가격 관측이 없습니다.").toString();s.append("최근: ").append(m(h.latest)).append("원\n");if(h.comparableTrend)s.append("최저: ").append(m(h.min)).append("원 · 최고: ").append(m(h.max)).append("원 · 평균: ").append(m(h.average)).append("원\n");else s.append("NON_STANDARD는 단위 변환 전이므로 관측 목록만 표시합니다.\n");s.append("\n이력\n");for(PriceObservation o:h.observations)s.append("• ").append(o.purchaseDate==null?"날짜 미인식":o.purchaseDate).append(" · ").append(m(o.unitPrice)).append("원 · ").append(o.rawItemName).append(" · ").append(o.priceOrigin).append(" · ").append(o.linkSource).append('\n');return s.toString();}private static String m(Long v){return v==null?"?":NumberFormat.getIntegerInstance(Locale.KOREA).format(v);}
}
