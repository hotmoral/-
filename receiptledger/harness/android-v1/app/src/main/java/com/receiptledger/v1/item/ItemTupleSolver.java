package com.receiptledger.v1.item;

import com.receiptledger.v1.layout.LayoutToken;
import com.receiptledger.v1.structure.MoneyCandidate;
import com.receiptledger.v1.structure.ReceiptStructure;
import com.receiptledger.v1.structure.StructuredRow;
import java.util.ArrayList;import java.util.Comparator;import java.util.List;

public final class ItemTupleSolver {
    public ItemTupleResult solve(ReceiptStructure structure){List<ItemTuple> out=new ArrayList<>();if(structure!=null)for(StructuredRow row:structure.itemRows)out.add(solveRow(row));return new ItemTupleResult(out);}

    private ItemTuple solveRow(StructuredRow row){
        List<MoneyCandidate> money=new ArrayList<>();for(MoneyCandidate m:row.moneyCandidates)if(m.amount>=0)money.add(m);money.sort(Comparator.comparingDouble(m->m.token.centerX));
        List<QuantityCandidate> quantities=new ArrayList<>();for(LayoutToken token:row.row.tokens){QuantityCandidate q=QuantityCandidate.parse(token);if(q!=null)quantities.add(q);}quantities.sort(Comparator.comparingDouble(q->q.token.centerX));
        MoneyCandidate line=money.isEmpty()?null:money.get(money.size()-1);
        if(line==null)return new ItemTuple(row.index,joinName(row,Double.POSITIVE_INFINITY),null,null,null,ValueOrigin.UNKNOWN,ValueOrigin.UNKNOWN,ValueOrigin.UNKNOWN,ItemResolution.PARTIAL,"NO_LINE_AMOUNT");

        Exact exact=findExact(money,quantities,line);
        if(exact!=null){double cutoff=Math.min(exact.unit.token.centerX,exact.quantity.token.centerX);return new ItemTuple(row.index,joinName(row,cutoff),exact.quantity.quantity,exact.unit.amount,line.amount,ValueOrigin.PRINTED,ValueOrigin.PRINTED,ValueOrigin.PRINTED,ItemResolution.EXACT,"PRINTED_UNIT_X_QTY_EQUALS_LINE");}

        if(money.size()==1&&!quantities.isEmpty()){
            QuantityCandidate q=nearestQuantityBeforeOrAfter(quantities,line.token.centerX);
            if(q!=null&&q.quantity>0){
                if(q.token.centerX<line.token.centerX&&line.amount%q.quantity==0){long unit=line.amount/q.quantity;return new ItemTuple(row.index,joinName(row,q.token.centerX),q.quantity,unit,line.amount,ValueOrigin.PRINTED,ValueOrigin.INFERRED_ARITHMETIC,ValueOrigin.PRINTED,ItemResolution.INFERRED,"PRINTED_QTY_AND_LINE_INFER_UNIT");}
                if(q.token.centerX>line.token.centerX){Long inferred=safeMultiply(line.amount,q.quantity);if(inferred!=null)return new ItemTuple(row.index,joinName(row,line.token.centerX),q.quantity,line.amount,inferred,ValueOrigin.PRINTED,ValueOrigin.PRINTED,ValueOrigin.INFERRED_ARITHMETIC,ItemResolution.INFERRED,"PRINTED_UNIT_AND_QTY_INFER_LINE");}
            }
        }

        if(money.size()==1&&quantities.isEmpty())return new ItemTuple(row.index,joinName(row,line.token.centerX),1,line.amount,line.amount,ValueOrigin.DEFAULT_ONE,ValueOrigin.PRINTED,ValueOrigin.PRINTED,ItemResolution.INFERRED,"SINGLE_AMOUNT_DEFAULT_QTY_ONE");

        return new ItemTuple(row.index,joinName(row,money.get(0).token.centerX),null,null,line.amount,ValueOrigin.UNKNOWN,ValueOrigin.UNKNOWN,ValueOrigin.PRINTED,ItemResolution.PARTIAL,"NO_EXACT_ARITHMETIC_SOLUTION");
    }

    private static Exact findExact(List<MoneyCandidate> money,List<QuantityCandidate> quantities,MoneyCandidate line){Exact best=null;double bestScore=Double.POSITIVE_INFINITY;for(QuantityCandidate q:quantities)for(MoneyCandidate unit:money){if(unit==line||unit.amount<=0)continue;Long product=safeMultiply(unit.amount,q.quantity);if(product==null||product!=line.amount)continue;double score=Math.abs(unit.token.centerX-q.token.centerX)+(unit.token.centerX>line.token.centerX?10000:0);if(score<bestScore){bestScore=score;best=new Exact(unit,q);}}return best;}
    private static QuantityCandidate nearestQuantityBeforeOrAfter(List<QuantityCandidate> qs,double x){QuantityCandidate best=null;double distance=Double.POSITIVE_INFINITY;for(QuantityCandidate q:qs){double d=Math.abs(q.token.centerX-x);if(d<distance){distance=d;best=q;}}return best;}
    private static Long safeMultiply(long a,int b){if(a<0||b<0)return null;if(b!=0&&a>Long.MAX_VALUE/b)return null;return a*b;}
    private static String joinName(StructuredRow row,double cutoff){StringBuilder out=new StringBuilder();for(LayoutToken token:row.row.tokens){if(token.centerX>=cutoff)break;if(out.length()>0)out.append(' ');out.append(token.text);}return out.toString().trim();}
    private static final class Exact{final MoneyCandidate unit;final QuantityCandidate quantity;Exact(MoneyCandidate u,QuantityCandidate q){unit=u;quantity=q;}}
}
