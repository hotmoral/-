#!/usr/bin/env python3
"""Timing Defense v0.16 exact-formula pressure diagnostic."""
from __future__ import annotations
import argparse, itertools, random, statistics, math
from dataclasses import dataclass
from collections import defaultdict
from pressure_recipe_sim_v1 import MON, TIERS, generate_stage

CLASSES=['Knight','Rogue','Tank','Archer','Mage']
PROFILES={'Average':dict(pN=.25,pG=.55,pP=.20,normal=1.14,heavy=1.68),'Skilled':dict(pN=.10,pG=.50,pP=.40,normal=1.04,heavy=1.54)}
AI_INTERVAL={'Knight':1.400,'Rogue':1.150,'Tank':1.650,'Archer':1.200,'Mage':1.500}
LEVELS=(6,11,16,21)
KNOCK={'GRUNT':.85,'RUNNER':1.0,'BRUTE':.38,'SHIELD':.62,'FLYER':.90}

@dataclass
class Mob:
    typ:str; hp:float; maxhp:float; speed:float; wall:float; armor:float; lane:int
    x:float=1.0; alive:bool=True; boss:bool=False

def instantiate(row):
    _,typ,lane,hm,_,_=row; d=MON[typ]; hp=d['hp']*hm
    return Mob(typ,hp,hp,d['speed'],d['wall'],d['armor'],lane)
def alive(mobs): return [m for m in mobs if m.alive]
def nearest(mobs):
    a=alive(mobs); return min(a,key=lambda m:m.x) if a else None
def jdraw(rng,p):
    u=rng.random();return 'N' if u<p['pN'] else 'G' if u<p['pN']+p['pG'] else 'P'
def base_damage(j): return {'N':100,'G':140,'P':200}[j]
def heavy_damage(a,b):
    if a==b=='P': return 600,'CRITICAL'
    w=(2 if a=='P' else 1 if a=='G' else 0)+(2 if b=='P' else 1 if b=='G' else 0)
    return (400,'SUPER') if w>=3 else (300,'GREAT') if w==2 else (230,'HEAVY+') if w==1 else (180,'HEAVY')
def hit(m,raw,armor_ignore=False,dagger=False):
    if not m or not m.alive:return False,0.0
    if dagger and m.boss: raw*=.70
    actual=max(1,round(raw*(1.0 if armor_ignore else m.armor)));m.hp-=actual
    if m.hp<=0:m.alive=False
    return (not m.alive),actual
def timing_attack(rng,p,no):
    h=(no%4==0)
    if h:
        a,b=jdraw(rng,p),jdraw(rng,p);d,t=heavy_damage(a,b);return h,d,t,(a=='P' or b=='P')
    a=jdraw(rng,p);return h,base_damage(a),a,(a=='P')
def choose_target(mobs,cls): return nearest(mobs)
def same_lane_forward(mobs,t,xdist,adjacent=False):
    return sorted([m for m in alive(mobs) if m is not t and m.x>=t.x and m.x-t.x<=xdist and abs(m.lane-t.lane)<=(1 if adjacent else 0)],key=lambda m:m.x)
def basic_knock_x(tier):
    if tier=='CRITICAL':return .047
    if tier in ('PERFECT','SUPER'):return .024
    if tier in ('GOOD','GREAT'):return .013
    return .006
def push(m,tier,mul=1.0):
    if m and m.alive:m.x=min(1.08,m.x+basic_knock_x(tier)*KNOCK[m.typ]*mul*(.40 if m.boss else 1.0))

def local_attack(mobs,cls,p,rng,no,level,stats):
    h,dmg,tier,has_perfect=timing_attack(rng,p,no);t=choose_target(mobs,cls)
    if not t:return dict(has_perfect=has_perfect,heavy=h,cycle_delta=0)
    mult=1.0
    if cls=='Knight' and level>=6:mult+=.12
    if cls=='Archer' and level>=11:mult+=.10
    if cls=='Knight' and level>=16 and has_perfect:mult*=1.18
    if cls=='Knight' and level>=21 and h:mult*=1.20
    if cls=='Mage' and level>=21 and h:mult*=1.20
    raw=dmg*mult
    if cls=='Rogue' and level>=11 and rng.random()<.06:raw=round(raw*1.5);stats['proc_crit']+=1
    if cls=='Knight':
        _,a=hit(t,raw);stats['damage']+=a;km=1.20 if level>=16 and has_perfect else 1.0;push(t,tier,km)
        if level>=11:
            n=(3 if level>=21 else 2) if h else 1
            for m in same_lane_forward(mobs,t,.28 if h else .20,adjacent=h)[:n]:_,q=hit(m,round(raw*.85));stats['damage']+=q;push(m,tier,km)
    elif cls=='Rogue':
        _,a=hit(t,raw,dagger=True);stats['damage']+=a;push(t,tier)
        if level>=6:
            n=4 if h and level>=21 else 1;sc=.45 if h and level>=21 else .55
            for _ in range(n):
                q=t if t.alive else choose_target(mobs,cls)
                if not q:break
                _,z=hit(q,round(raw*sc),dagger=True);stats['damage']+=z;push(q,'SKILL')
    elif cls=='Tank':
        _,a=hit(t,raw);stats['damage']+=a;km=(2.0 if h and level>=21 else 1.30) if level>=6 else 1.0;push(t,tier,km)
        if h and level>=21:
            for m in [m for m in alive(mobs) if m is not t and abs(m.x-t.x)<=.16 and abs(m.lane-t.lane)<=1]:_,z=hit(m,raw);stats['damage']+=z;push(m,tier,km)
    elif cls=='Archer':
        armor_ignore=(level>=16 and has_perfect);preserve=armor_ignore;launch_lane=t.lane;launch_x=t.x
        _,a=hit(t,raw,armor_ignore=armor_ignore);stats['damage']+=a;push(t,tier)
        if level>=6:
            for m in sorted([m for m in alive(mobs) if m is not t and m.lane==launch_lane and m.x>=launch_x],key=lambda m:m.x)[:2]:
                pr=raw if preserve else round(raw*.52);_,z=hit(m,pr,armor_ignore=armor_ignore);stats['damage']+=z;push(m,tier)
        if h and level>=21:
            for _ in range(2):
                candidates=sorted([m for m in alive(mobs) if m.lane==launch_lane and m.x>=launch_x-.02],key=lambda m:m.x)
                q=t if t.alive and t.lane==launch_lane else (candidates[0] if candidates else None)
                if not q:continue
                sr=round(raw*.65);_,z=hit(q,sr,armor_ignore=armor_ignore);stats['damage']+=z;push(q,'SKILL')
                for m in sorted([m for m in alive(mobs) if m is not q and m.lane==launch_lane and m.x>=q.x],key=lambda m:m.x)[:2]:
                    pr=sr if preserve else round(sr*.52);_,zz=hit(m,pr,armor_ignore=armor_ignore);stats['damage']+=zz;push(m,'SKILL')
    else:
        _,a=hit(t,raw);stats['damage']+=a;push(t,tier)
        if level>=6:
            rx=.105*(1.35 if level>=11 else 1.0)*(1.60 if h and level>=21 else 1.0);lane_tol=2 if h and level>=21 else 1;splash=.60 if level>=11 else .50
            near=sorted([m for m in alive(mobs) if m is not t and abs(m.x-t.x)<rx and abs(m.lane-t.lane)<=lane_tol],key=lambda m:abs(m.x-t.x))[:3]
            for m in near:_,z=hit(m,round(raw*splash));stats['damage']+=z;push(m,'SKILL')
            if level>=16 and has_perfect:
                ring=[]
                for m in alive(mobs):
                    if m is t:continue
                    nd=math.hypot(abs(m.x-t.x)/max(rx,1e-6),abs(m.lane-t.lane)*.75)
                    if .32<=nd<=1.05:ring.append((nd,m))
                for _,m in sorted(ring,key=lambda z:z[0])[:4]:_,z=hit(m,round(raw*.55));stats['damage']+=z;push(m,'SKILL')
    delta=0.0
    if cls=='Rogue' and level>=16 and has_perfect:delta-=.078
    if cls=='Archer' and level>=11:delta-=.028
    if cls=='Mage' and level>=21 and h:delta+=.0504
    return dict(has_perfect=has_perfect,heavy=h,cycle_delta=delta)

def ai_attack(mobs,cls,rng,no):
    t=nearest(mobs)
    if not t:return 0.0
    r=rng.random();h=(no%4==0)
    if h:dmg=400 if r<.15 else 300 if r<.65 else 230;tier='SUPER' if r<.15 else 'GREAT' if r<.65 else 'HEAVY+'
    else:dmg=200 if r<.18 else 140 if r<.72 else 100;tier='PERFECT' if r<.18 else 'GOOD' if r<.72 else 'NORMAL'
    _,a=hit(t,dmg)
    if t and t.alive:
        kb=.007 if tier in ('PERFECT','SUPER') else .004 if tier in ('GOOD','GREAT') else .002
        t.x=min(1.08,t.x+kb*KNOCK[t.typ]*(.40 if t.boss else 1.0))
    return a

def simulate(tier,n,team,local,pname,level,seed,stage_idx=25):
    rng=random.Random(seed);schedule=generate_stage(tier,n,rng,stage_idx);mobs=[];idx=0;wall=2000.;shield=0.;shield_until=0.;t=0.;dt=.10
    next_at=[.10+i*.15 for i in range(n)];attack_no=[0]*n;max_active=0;local_index=team.index(local);p=PROFILES[pname];stats=defaultdict(float)
    while t<90:
        while idx<len(schedule) and schedule[idx][0]<=t:mobs.append(instantiate(schedule[idx]));idx+=1
        max_active=max(max_active,len(alive(mobs)))
        if shield>0 and t>=shield_until:shield=0
        for i,cls in enumerate(team):
            if t+1e-9>=next_at[i] and alive(mobs):
                attack_no[i]+=1
                if i==local_index:
                    out=local_attack(mobs,cls,p,rng,attack_no[i],level,stats);cyc=p['heavy'] if out['heavy'] else p['normal'];next_at[i]=t+max(.25,cyc+out['cycle_delta'])
                    if cls=='Tank' and level>=16 and out['has_perfect']:shield=80.;shield_until=t+3.0
                else:ai_attack(mobs,cls,rng,attack_no[i]);next_at[i]=t+AI_INTERVAL[cls]+rng.uniform(-.14,.17)
        for m in alive(mobs):
            m.x-=m.speed*dt
            if m.x<=.155:
                incoming=m.wall*(.90 if local=='Tank' and level>=11 else 1);absorb=min(shield,incoming) if t<shield_until else 0;shield-=absorb;wall-=incoming-absorb;m.alive=False
        if wall<=0:return False,0,max_active,t,stats
        if idx>=len(schedule) and not alive(mobs):return True,wall,max_active,t,stats
        t+=dt
    return wall>0,max(0,wall),max_active,t,stats

def run_matrix(seeds=10):
    rows=[]
    for level in LEVELS:
        for n in (2,3,4):
            for pname in ('Average','Skilled'):
                vals=[];by_tier=defaultdict(list)
                for ti,tier in enumerate(TIERS):
                    for ci,team in enumerate(itertools.combinations(CLASSES,n)):
                        for local in team:
                            for s in range(seeds):
                                seed=1_600_000+level*100_000+n*20_000+ti*3000+(0 if pname=='Average' else 1500)+ci*200+CLASSES.index(local)*30+s
                                r=simulate(tier,n,team,local,pname,level,seed);vals.append(r);by_tier[tier].append(r)
                rows.append((level,n,pname,len(vals),sum(v[0] for v in vals)/len(vals),statistics.mean(v[1] for v in vals),statistics.mean(v[2] for v in vals),{k:sum(x[0] for x in q)/len(q) for k,q in by_tier.items()}))
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seeds',type=int,default=10);ap.add_argument('--level',type=int,choices=LEVELS,default=0);args=ap.parse_args()
    if args.level:globals()['LEVELS']=(args.level,)
    for level,n,pname,runs,clr,wall,ma,tiers in run_matrix(args.seeds):print(f'L{level:02d} {n}P {pname:7s} runs={runs:4d} clear={clr*100:5.1f}% wall={wall:7.1f} maxActive={ma:4.1f} '+' '.join(f'{k}={v*100:4.1f}' for k,v in tiers.items()))
if __name__=='__main__':main()
