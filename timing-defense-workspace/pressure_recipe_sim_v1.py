#!/usr/bin/env python3
"""Timing Defense concrete pressure-recipe calculator (v1).

Purpose:
- generate the v6 candidate S/E/X recipes for 2/3/4-player teams,
- calculate short-window spawn-density/readability metrics,
- calculate simple threat-index statistics,
- provide deterministic stage samples for later combat simulation.

This is NOT production encounter data and does not patch the playable game.
"""
from __future__ import annotations
import argparse, math, random, statistics

MON = {
    'GRUNT':  dict(hp=320, speed=.070, wall=90,  armor=1.00),
    'RUNNER': dict(hp=165, speed=.135, wall=60,  armor=1.00),
    'BRUTE':  dict(hp=900, speed=.040, wall=180, armor=1.00),
    'SHIELD': dict(hp=540, speed=.057, wall=120, armor=.72),
    'FLYER':  dict(hp=225, speed=.100, wall=70,  armor=1.00),
}

TIERS = {
    'T1': dict(comp={1:30,2:17,3:3},  occ={'S':25,'E':24,'X':24}, sforms={'line':8,'cluster':11,'scatter':6},  xforms={'line':7,'cluster':6,'split':11}, timing=[.22,.34,.28,.16], intensity=(.85,1.00)),
    'T2': dict(comp={1:21,2:23,3:6},  occ={'S':24,'E':37,'X':24}, sforms={'line':7,'cluster':11,'scatter':6},  xforms={'line':5,'cluster':6,'split':13}, timing=[.14,.36,.34,.16], intensity=(.95,1.08)),
    'T3': dict(comp={1:17,2:25,3:8},  occ={'S':40,'E':19,'X':32}, sforms={'line':22,'cluster':10,'scatter':8}, xforms={'line':14,'cluster':5,'split':13}, timing=[.16,.25,.34,.25], intensity=(1.00,1.12)),
    'T4': dict(comp={1:11,2:25,3:14}, occ={'S':32,'E':28,'X':43}, sforms={'line':8,'cluster':10,'scatter':14}, xforms={'line':9,'cluster':8,'split':26}, timing=[.18,.28,.30,.24], intensity=(1.04,1.16)),
    'T5': dict(comp={1:23,2:19,3:8},  occ={'S':30,'E':31,'X':24}, sforms={'line':9,'cluster':17,'scatter':4},  xforms={'line':6,'cluster':6,'split':12}, timing=[.10,.24,.30,.36], intensity=(1.08,1.24)),
}

def pick(rng, weights):
    keys=list(weights)
    return rng.choices(keys, weights=[weights[k] for k in keys], k=1)[0]

def sample_unique(rng, weights, k):
    pool=dict(weights); out=[]
    for _ in range(k):
        q=pick(rng,pool); out.append(q); pool.pop(q)
    return out

def sample_slots(rng, items, weights, k):
    items=list(items); weights=list(weights); out=[]
    for _ in range(k):
        i=rng.choices(range(len(items)),weights=weights,k=1)[0]
        out.append(items.pop(i)); weights.pop(i)
    return sorted(out)

def recipe(fam, form, n, intensity, rng):
    mobs=[]
    if fam=='S':
        if form=='line':
            g,r={2:(5,3),3:(7,4),4:(9,5)}[n]; lane=rng.randrange(3)
            seq=['GRUNT']*g+['RUNNER']*r; rng.shuffle(seq)
            mobs=[(i*.20,t,lane,1.0) for i,t in enumerate(seq)]
        elif form=='cluster':
            g,f={2:(5,2),3:(7,3),4:(9,4)}[n]; center=rng.randrange(3)
            seq=['GRUNT']*g+['FLYER']*f; rng.shuffle(seq)
            for i,t in enumerate(seq):
                lane=max(0,min(2,center+rng.choice([-1,0,0,0,1])))
                mobs.append((i*.18,t,lane,1.0))
        else:
            g,r,f={2:(3,4,2),3:(4,5,3),4:(5,7,4)}[n]
            seq=['GRUNT']*g+['RUNNER']*r+['FLYER']*f; rng.shuffle(seq)
            mobs=[(i*.24,t,rng.randrange(3),1.0) for i,t in enumerate(seq)]
    elif fam=='E':
        # Stress-envelope effective durability; not final literal production HP.
        pscale={2:1.80,3:2.30,4:2.80}[n]
        variant=rng.choice(['brute','shield','mixed'])
        if variant=='brute':
            base={2:[('BRUTE',1.45)],3:[('BRUTE',1.55),('BRUTE',1.0)],4:[('BRUTE',1.65),('BRUTE',1.25)]}[n]
        elif variant=='shield':
            base={2:[('SHIELD',1.35),('SHIELD',1.0)],3:[('SHIELD',1.35),('SHIELD',1.25),('SHIELD',1.0)],4:[('SHIELD',1.50),('SHIELD',1.35),('SHIELD',1.15)]}[n]
        else:
            base={2:[('BRUTE',1.15),('SHIELD',1.0)],3:[('BRUTE',1.30),('SHIELD',1.25)],4:[('BRUTE',1.45),('SHIELD',1.35),('SHIELD',1.0)]}[n]
        mobs=[(i*.55,t,rng.randrange(3),m*pscale) for i,(t,m) in enumerate(base)]
    else:
        xscale={2:1.50,3:1.90,4:2.30}[n]
        if form=='line':
            sh,r,f={2:(1,3,2),3:(2,4,2),4:(2,5,3)}[n]; lane=rng.randrange(3)
            seq=['SHIELD']*sh+['RUNNER']*r+['FLYER']*f+(['BRUTE']*(n-2) if n>=3 else [])
            mobs=[(i*.26,t,lane,xscale if t in ('SHIELD','BRUTE') else 1.0) for i,t in enumerate(seq)]
        elif form=='cluster':
            sh,g,f={2:(1,3,2),3:(2,4,3),4:(2,5,4)}[n]; center=rng.randrange(3)
            seq=['SHIELD']*sh+['GRUNT']*g+['FLYER']*f+(['BRUTE']*(n-2) if n>=3 else []); rng.shuffle(seq)
            for i,t in enumerate(seq):
                lane=max(0,min(2,center+rng.choice([-1,0,0,1])))
                mobs.append((i*.22,t,lane,xscale if t in ('SHIELD','BRUTE') else 1.0))
        else:
            sh,r,f={2:(1,3,2),3:(2,5,3),4:(2,6,4)}[n]
            seq=['SHIELD']*sh+['RUNNER']*r+['FLYER']*f+(['BRUTE']*(n-2) if n>=3 else [])
            for i,t in enumerate(seq):
                mobs.append((i*.24,t,0 if i%2==0 else 2,xscale if t in ('SHIELD','BRUTE') else 1.0))
    hp_intensity=.94+.18*intensity
    out=[(t,typ,lane,m*hp_intensity) for t,typ,lane,m in mobs]
    if fam=='S' and intensity>1.12:
        extra=max(1,round((intensity-1.0)*4))
        last=max(x[0] for x in out)
        for j in range(extra):
            out.append((last+.14*(j+1),rng.choice(['GRUNT','RUNNER']),rng.randrange(3),hp_intensity))
    return out

def generate_stage(tier_key,n,rng,stage_idx):
    cfg=TIERS[tier_key]
    complexity=pick(rng,cfg['comp'])
    fams=sample_unique(rng,cfg['occ'],complexity)
    intensity=rng.uniform(*cfg['intensity'])*(.92+.16*(stage_idx-1)/49)
    spawn=[]
    base_n={2:10,3:12,4:14}[n]
    for i in range(base_n):
        typ=rng.choices(['GRUNT','RUNNER','FLYER'],weights=[.62,.25,.13],k=1)[0]
        t=1+i*(42/(base_n-1))+rng.uniform(-.4,.4)
        spawn.append((max(.15,t),typ,rng.randrange(3),.95+.12*intensity,'B','scatter'))
    total={2:{1:4,2:5,3:5},3:{1:5,2:6,3:6},4:{1:5,2:6,3:6}}[n][complexity]
    if complexity==1:
        seq=[fams[0]]*total
    else:
        if tier_key=='T2' and 'E' in fams: dom='E'
        elif tier_key=='T3' and 'S' in fams: dom='S'
        elif tier_key=='T4' and 'X' in fams: dom='X'
        elif tier_key=='T5': dom=rng.choice(fams)
        else: dom=max(fams,key=lambda f:cfg['occ'][f])
        if complexity==2:
            nd=math.ceil(total*.6); other=[f for f in fams if f!=dom][0]
            seq=[dom]*nd+[other]*(total-nd)
        else:
            nd=math.ceil(total*.45); rem=total-nd; others=[f for f in fams if f!=dom]
            seq=[dom]*nd+[others[i%2] for i in range(rem)]
        rng.shuffle(seq)
    slots=[4,9,15,21,28,35,43]
    cats=['early','early','mid','mid','late','late','final']
    weights=[cfg['timing'][0] if c=='early' else cfg['timing'][1] if c=='mid' else cfg['timing'][2] if c=='late' else cfg['timing'][3] for c in cats]
    chosen=sample_slots(rng,slots,weights,total); rng.shuffle(seq)
    for fam,et in zip(seq,chosen):
        form=pick(rng,cfg['sforms']) if fam=='S' else pick(rng,cfg['xforms']) if fam=='X' else 'elite'
        fm=1.0
        if tier_key=='T2' and fam=='E': fm*=1.15
        if tier_key=='T3' and fam=='S': fm*=1.12
        if tier_key=='T4' and fam=='X': fm*=1.14
        if tier_key=='T5': fm*=1.12
        for off,typ,lane,hm in recipe(fam,form,n,intensity*fm,rng):
            spawn.append((et+rng.uniform(-.35,.35)+off,typ,lane,hm,fam,form))
    spawn.sort()
    return spawn

def percentile(xs,p):
    a=sorted(xs)
    if not a:return 0.0
    q=(len(a)-1)*p/100; lo=int(q); hi=min(len(a)-1,lo+1); f=q-lo
    return a[lo]*(1-f)+a[hi]*f

def threat(spawn):
    total=0.0
    for _,typ,_,hm,_,_ in spawn:
        v=MON[typ]; effhp=v['hp']*hm/v['armor']
        total+=(effhp/320)*(v['speed']/.07)**.6*(v['wall']/90)**.7
    return total

def max_window(times,w):
    ts=sorted(times); best=0; j=0
    for i,t in enumerate(ts):
        if j<i:j=i
        while j<len(ts) and ts[j]<=t+w:j+=1
        best=max(best,j-i)
    return best

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--seed',type=int,default=110000)
    args=ap.parse_args()
    for n in (2,3,4):
        totals=[]; peaks4=[]; peaks6=[]; threats=[]
        print(f'\n== {n} players ==')
        for ti,tier in enumerate(TIERS):
            rt=[]; rp4=[]; rp6=[]; rth=[]
            for stage in range(1,51):
                rng=random.Random(args.seed+n*10000+ti*100+stage)
                sp=generate_stage(tier,n,rng,stage)
                ts=[x[0] for x in sp]
                rt.append(len(sp)); rp4.append(max_window(ts,4)); rp6.append(max_window(ts,6)); rth.append(threat(sp))
            totals+=rt;peaks4+=rp4;peaks6+=rp6;threats+=rth
            print(f'{tier}: meanN={statistics.mean(rt):.1f} p95N={percentile(rt,95):.1f} p95_4s={percentile(rp4,95):.1f} p95_6s={percentile(rp6,95):.1f} meanThreat={statistics.mean(rth):.1f}')
        print(f'ALL: meanN={statistics.mean(totals):.1f} p95N={percentile(totals,95):.1f} mean4s={statistics.mean(peaks4):.1f} p95_4s={percentile(peaks4,95):.1f} p95_6s={percentile(peaks6,95):.1f} meanThreat={statistics.mean(threats):.1f}')

if __name__=='__main__':
    main()
