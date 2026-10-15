package com.receiptledger.v1.item;

import com.receiptledger.v1.layout.LayoutToken;
import com.receiptledger.v1.structure.MoneyCandidate;
import java.text.Normalizer;
import java.util.Locale;

public final class QuantityCandidate {
    public final int quantity;
    public final String rawText;
    public final LayoutToken token;

    private QuantityCandidate(int quantity, String rawText, LayoutToken token) {
        this.quantity=quantity;this.rawText=rawText;this.token=token;
    }

    public static QuantityCandidate parse(LayoutToken token) {
        if(token==null||token.text==null||MoneyCandidate.parse(token)!=null)return null;
        String raw=Normalizer.normalize(token.text.trim(),Normalizer.Form.NFKC).toUpperCase(Locale.ROOT).replace(" ","");
        if(raw.isEmpty())return null;
        String digits=raw;
        if(digits.startsWith("X"))digits=digits.substring(1);
        if(digits.endsWith("X"))digits=digits.substring(0,digits.length()-1);
        if(digits.endsWith("개"))digits=digits.substring(0,digits.length()-1);
        else if(digits.endsWith("EA"))digits=digits.substring(0,digits.length()-2);
        else if(digits.endsWith("PCS"))digits=digits.substring(0,digits.length()-3);
        if(!digits.matches("[0-9]{1,2}"))return null;
        int q=Integer.parseInt(digits);
        return q>=1&&q<=99?new QuantityCandidate(q,raw,token):null;
    }
}
