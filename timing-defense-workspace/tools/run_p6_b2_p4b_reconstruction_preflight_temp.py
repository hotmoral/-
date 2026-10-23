#!/usr/bin/env python3
from __future__ import annotations
import json, math, statistics
from dataclasses import dataclass
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
RECIPES=ROOT/'legacy-game-structure'/'data'/'model_a_representative_recipes_v0_1.yaml'
COMBAT=ROOT/'legacy-game-structure'/'data'/'model_a_combat_sensitivity_anchor_v0_1.yaml'
HIST=ROOT/'legacy-game-structure'/'data'/'p4b_combat_feedback_divergence_v0_1.json'
LEVELS=(6,11,16,21)
CLASSES=('knight','rogue','tank','archer','mage')
BASE={'NORMAL':100,'GOOD':140,'PERFECT':200,'HEAVY':180,'HEAVY+':230,'GREAT':300,'SUPER':400,'CRITICAL':600}

@dataclass
class M:
    id:int; typ:str; x:float; y:float; hp:float; armor:float; alive:bool=True; generation:int=0

def qtile(a,p):
    a=sorted(a); pos=(len(a)-1)*p; lo=math.floor(pos); hi=math.ceil(pos); f=pos-lo
    return a[lo]*(1-f)+a[hi]*f

def combo_bonus(c): return .15 if c>=30 else .12 if c>=20 else .08 if c>=10 else .05 if c>=5 else 0.0

def milestone(c):
    if c in (5,10,20,30): return c
    if c>30 and c%10==0:return c
    return 0

def n3_budget(m): return 210 if m>=30 else 150 if m>=20 else 90 if m>=10 else 60

def n3_weights(cls,m):
    if cls=='rogue':
        n=5 if m>=30 else 4 if m>=20 else 3 if m>=10 else 2; return [1/n]*n
    if cls=='knight': return [.67,.33]
    if cls=='tank': return [.60,.20,.20]
    if cls=='archer': return [.70,.30]
    return [.55,.15,.15,.15]

def allocate(b,w):
    ex=[b*x for x in w]; out=[math.floor(x) for x in ex]; rem=b-sum(out)
    order=sorted(range(len(w)),key=lambda i:(-(ex[i]-math.floor(ex[i])),i))
    for k in range(rem):out[order[k%len(order)]]+=1
    return out

class Judge:
    def __init__(self): self.i=0
    def one(self):
        # historical Layer-A central deterministic bracket: 55 PERFECT then one GOOD
        q='GOOD' if self.i%56==55 else 'PERFECT'; self.i+=1; return q

def heavy(a,b):
    if a==b=='PERFECT':return 'CRITICAL'
    w=(2 if a=='PERFECT' else 1 if a=='GOOD' else 0)+(2 if b=='PERFECT' else 1 if b=='GOOD' else 0)
    return 'SUPER' if w>=3 else 'GREAT' if w==2 else 'HEAVY+' if w==1 else 'HEAVY'

def alive(ms):return [m for m in ms if m.alive]
def front(ms):
    a=alive(ms); return min(a,key=lambda m:(m.x,m.id)) if a else None

def hit(m,raw,ignore=False):
    if not m or not m.alive:return
    m.hp-=max(1,round(raw*(1.0 if ignore else m.armor)))
    if m.hp<=0:m.alive=False

def line_targets(ms,primary,max_count):
    # Mirrors the current continuous-Y Layer-A strict-line geometry.
    ax,ay=.105,.30; bx,by=primary.x,primary.y-.035
    dx,dy=bx-ax,by-ay; l2=dx*dx+dy*dy or 1.0; out=[]
    for m in alive(ms):
        if m.id==primary.id:continue
        qy=m.y-.035; t=((m.x-ax)*dx+(qy-ay)*dy)/l2
        if t<=1.025:continue
        px,py=ax+t*dx,ay+t*dy
        if math.hypot(m.x-px,qy-py)<=.042:out.append((t,m.id,m))
    out.sort(); return [x[2] for x in out[:max_count]]

def near(ms,p,dx,dy,n):
    out=[]
    for m in alive(ms):
        if m.id==p.id:continue
        if abs(m.x-p.x)<dx and abs(m.y-p.y)<dy:out.append((math.hypot(m.x-p.x,m.y-p.y),m.id,m))
    out.sort();return [z[2] for z in out[:n]]

def spawn_children(ms,m,stats,next_id):
    if m.typ!='SPLITTER' or m.generation!=0:return next_id
    d=stats['SPLITTER']
    for dy in (-.018,.018):
        ms.append(M(next_id,'SPLITTER_CHILD',m.x,m.y+dy,float(d['childHp']),float(d['childArmor']),True,1));next_id+=1
    return next_id

def damage_and_split(ms,m,raw,stats,ignore=False,next_id=1000):
    was=m.alive; hit(m,raw,ignore)
    if was and not m.alive:next_id=spawn_children(ms,m,stats,next_id)
    return next_id

def knight_pen(ms,p,raw,heavy_action,level,stats,next_id):
    if level<11:return next_id
    n=(3 if level>=21 else 2) if heavy_action else 1
    cand=[]
    for m in alive(ms):
        if m.id==p.id or m.x<p.x:continue
        if m.x-p.x<=(.28 if heavy_action else .20) and abs(m.y-p.y)<=(.16 if heavy_action else .10):cand.append((m.x,abs(m.y-p.y),m.id,m))
    cand.sort()
    for _,_,_,m in cand[:n]:next_id=damage_and_split(ms,m,round(raw*.85),stats,False,next_id)
    return next_id

def archer_arrow(ms,p,raw,level,perfect,stats,next_id,scale=1.0):
    ignore=level>=16 and perfect; base=raw*scale
    next_id=damage_and_split(ms,p,base,stats,ignore,next_id)
    if level>=6:
        secondaries=line_targets(ms,p,2)
        for m in secondaries:
            pr=base if ignore else round(base*.52)
            next_id=damage_and_split(ms,m,pr,stats,ignore,next_id)
    return next_id

def n3(ms,cls,mil,stats,next_id):
    p=front(ms)
    if not p:return next_id
    parts=allocate(n3_budget(mil),n3_weights(cls,mil))
    if cls=='rogue':
        for raw in parts:
            q=p if p.alive else front(ms)
            if not q:break
            next_id=damage_and_split(ms,q,raw,stats,False,next_id)
    elif cls=='knight':
        next_id=damage_and_split(ms,p,parts[0],stats,False,next_id)
        q=front(ms)
        if len(parts)>1 and q:next_id=damage_and_split(ms,q,parts[1],stats,False,next_id)
    elif cls=='tank':
        next_id=damage_and_split(ms,p,parts[0],stats,False,next_id)
        for q,raw in zip(near(ms,p,.13,.16,2),parts[1:]):next_id=damage_and_split(ms,q,raw,stats,False,next_id)
    elif cls=='archer':
        next_id=archer_arrow(ms,p,parts[0],6,False,stats,next_id,1.0)
        q=front(ms)
        if len(parts)>1 and q:next_id=damage_and_split(ms,q,parts[1],stats,False,next_id)
    else:
        next_id=damage_and_split(ms,p,parts[0],stats,False,next_id)
        for q,raw in zip(near(ms,p,.12,.16,3),parts[1:]):next_id=damage_and_split(ms,q,raw,stats,False,next_id)
    return next_id

def simulate(recipe,stats,cls,level):
    ms=[]; next_id=1
    for s in recipe['spawns']:
        typ=s['type']; d=stats[typ]
        # Spawn chronology becomes reduced-order front/back depth; no wall/movement lifecycle in this probe.
        x=.34+float(s['tMs'])/10000.0
        ms.append(M(next_id,typ,x,float(s['y']),float(d['hp']),float(d['armor'])));next_id+=1
    j=Judge(); combo=0; actions=0
    while alive(ms) and actions<500:
        actions+=1; heavy_action=(actions%4==0)
        if heavy_action:
            a,b=j.one(),j.one(); tier=heavy(a,b); perfect=(a=='PERFECT' or b=='PERFECT'); qs=(a,b)
        else:
            a=j.one(); tier=a; perfect=(a=='PERFECT'); qs=(a,)
        # Combo follows judgment events; non-PERFECT breaks. Trigger N3 for each crossed milestone.
        crossed=[]
        for q in qs:
            combo=combo+1 if q=='PERFECT' else 0
            mm=milestone(combo)
            if mm:crossed.append(mm)
        p=front(ms)
        if not p:break
        raw=BASE[tier]*(1+combo_bonus(combo))
        if cls=='knight' and level>=6:raw*=1.12
        if cls=='archer' and level>=11:raw*=1.10
        if cls=='knight' and level>=16 and perfect:raw*=1.18
        if cls=='knight' and level>=21 and heavy_action:raw*=1.20
        if cls=='mage' and level>=21 and heavy_action:raw*=1.20
        raw=max(1,round(raw))
        if cls=='knight':
            next_id=damage_and_split(ms,p,raw,stats,False,next_id)
            next_id=knight_pen(ms,p,raw,heavy_action,level,stats,next_id)
        elif cls=='rogue':
            # deterministic equivalent of current +6pp proc crit at Lv11: 1 in 17 root actions.
            rr=round(raw*1.5) if level>=11 and actions%17==0 else raw
            next_id=damage_and_split(ms,p,rr,stats,False,next_id)
            if level>=6:
                count=4 if heavy_action and level>=21 else 1; sc=.45 if heavy_action and level>=21 else .55
                for _ in range(count):
                    q=p if p.alive else front(ms)
                    if not q:break
                    next_id=damage_and_split(ms,q,round(raw*sc),stats,False,next_id)
        elif cls=='tank':
            next_id=damage_and_split(ms,p,raw,stats,False,next_id)
            if heavy_action and level>=21:
                for q in near(ms,p,.16,.18,20):next_id=damage_and_split(ms,q,raw,stats,False,next_id)
        elif cls=='archer':
            next_id=archer_arrow(ms,p,raw,level,perfect,stats,next_id,1.0)
            if heavy_action and level>=21:
                # two side arrows inherit strict launch-line behavior and 65% root damage.
                for _ in range(2):
                    q=front(ms)
                    if not q:break
                    next_id=archer_arrow(ms,q,raw,level,perfect,stats,next_id,.65)
        else:
            next_id=damage_and_split(ms,p,raw,stats,False,next_id)
            if level>=6:
                radius=.105*(1.35 if level>=11 else 1.0)*(1.60 if heavy_action and level>=21 else 1.0)
                splash=.60 if level>=11 else .50
                for q in near(ms,p,radius,.18 if level<21 or not heavy_action else .30,3):next_id=damage_and_split(ms,q,round(raw*splash),stats,False,next_id)
                if level>=16 and perfect:
                    ring=[]
                    for q in alive(ms):
                        if q.id==p.id:continue
                        nd=math.hypot(abs(q.x-p.x)/max(radius,1e-6),abs(q.y-p.y)/.18)
                        if .32<=nd<=1.05:ring.append((nd,q.id,q))
                    ring.sort()
                    for _,_,q in ring[:4]:next_id=damage_and_split(ms,q,round(raw*.55),stats,False,next_id)
        for mm in crossed:next_id=n3(ms,cls,mm,stats,next_id)
    return actions

def main():
    recipes=yaml.safe_load(RECIPES.read_text())['recipes']
    combat=yaml.safe_load(COMBAT.read_text())['monsters']
    hist=json.loads(HIST.read_text())
    if len(recipes)!=20:raise AssertionError(f'expected 20 representative recipes, got {len(recipes)}')
    targets=hist['all20ActionRatioVsLv1Median']; ranges=hist['all20ActionRatioRanges']
    result={'version':'p6-b2-p4b-reconstruction-preflight-temp-v0.1','recipeCount':len(recipes),'method':'reduced-order static action-count response using archived representative recipes + v0.16 skill semantics; no shop','perClass':{},'status':'PREFLIGHT_ONLY'}
    max_med=0; max_edge=0
    for cls in CLASSES:
        base=[simulate(r,combat,cls,1) for r in recipes]
        rec={'lv1Actions':dict(zip([r['id'] for r in recipes],base)),'levels':{}}
        for lv in LEVELS:
            acts=[simulate(r,combat,cls,lv) for r in recipes]
            ratios=[a/b for a,b in zip(acts,base)]
            med=statistics.median(ratios); lo=min(ratios); hi=max(ratios)
            t=float(targets[cls][f'Lv{lv}']); tr=ranges[cls][f'Lv{lv}']
            md=abs(med-t); ed=max(abs(lo-float(tr[0])),abs(hi-float(tr[1])))
            max_med=max(max_med,md);max_edge=max(max_edge,ed)
            rec['levels'][f'Lv{lv}']={'actions':dict(zip([r['id'] for r in recipes],acts)),'ratios':[round(x,6) for x in ratios],'median':round(med,6),'range':[round(lo,6),round(hi,6)],'historicalMedian':t,'historicalRange':tr,'medianAbsDiff':round(md,6),'maxRangeEdgeAbsDiff':round(ed,6)}
        result['perClass'][cls]=rec
    result['summary']={'maxMedianAbsDiff':round(max_med,6),'maxRangeEdgeAbsDiff':round(max_edge,6),'exactHistoricalReproduction':max_med<0.0005 and max_edge<0.0005,'noShopInjected':True,'productionAuthority':False}
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))

if __name__=='__main__':main()
