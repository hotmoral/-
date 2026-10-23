#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'legacy-game-structure'/'data'
P4A=DATA/'p4a_marker_opportunity_corpus_v0_1.json'; P4AS=DATA/'p4a_marker_inverse_design_summary_v0_1.json'
REC=DATA/'model_a_representative_recipes_v0_1.yaml'; KIN=DATA/'model_a_kinematic_anchor_v0_1.yaml'
COMBAT=DATA/'model_a_combat_sensitivity_anchor_v0_1.yaml'; SKILLED=DATA/'skilled_v2_central_sequence_candidate_v0_1.yaml'
SHOP=DATA/'p5_shop_economy_spend_capacity_fixture_v0_1.json'; P4D2=DATA/'p4d2_lv31_pressure_probe_fixture_v0_1.json'
CLASSES=('knight','rogue','tank','archer','mage'); FXS=('T1_CENTRAL','T2_CENTRAL','T3_CENTRAL','T4_CENTRAL')
LEVELS=(6,11,16,21,26,31); MILESTONES=()
XP={'NORMAL':1.0,'GOOD':1.5,'PERFECT':2.25,'HEAVY':1.25,'HEAVY+':1.75,'GREAT':2.25,'SUPER':2.875,'CRITICAL':3.5}
BASE={'NORMAL':100,'GOOD':140,'PERFECT':200,'HEAVY':180,'HEAVY+':230,'GREAT':300,'SUPER':400,'CRITICAL':600}
CATS=('atk','crit','critdmg','fort','def','knock'); MASK=0xffffffff; FNV=2166136261; PRIME=16777619; ZERO=0x6D2B79F5
ACTION_MS=1100; STEP_MS=50; GAP_MS=1500; LINE_Y=.06; MAGE_RX=.105; MAGE_RY=.16; TANK_DX=.16; TANK_DY=.10; ZONE_MS=1500; ZONE_MULT=.75

def seed(base,domain):
 h=FNV
 for b in f'{base}|{domain}'.encode(): h=((h^b)*PRIME)&MASK
 return h or ZERO
class RNG:
 def __init__(self,s): self.state=s&MASK or ZERO
 def unit(self):
  x=self.state; x^=(x<<13)&MASK; x^=(x>>17)&MASK; x^=(x<<5)&MASK; self.state=x&MASK; return self.state/4294967296
def choose(d,u):
 a=0.; last=None
 for k,v in d.items():
  last=k; a+=float(v)
  if u<a:return k
 return last
def cb(c): return .15 if c>=30 else .12 if c>=20 else .08 if c>=10 else .05 if c>=5 else 0.
def mile(c): return c if c in (5,10,20,30) or (c>30 and c%10==0) else 0
def budget(m): return 210 if m>=30 else 150 if m>=20 else 90 if m>=10 else 60
def weights(c,m):
 if c=='rogue':
  n=5 if m>=30 else 4 if m>=20 else 3 if m>=10 else 2; return [1/n]*n
 return {'knight':[.67,.33],'tank':[.6,.2,.2],'archer':[.7,.3],'mage':[.55,.15,.15,.15]}[c]
def alloc(total,w):
 ex=[total*x for x in w]; out=[math.floor(x) for x in ex]; rem=total-sum(out); order=sorted(range(len(w)),key=lambda i:(-(ex[i]%1),i))
 for k in range(rem):out[order[k%len(order)]]+=1
 return out
def heavy(a,b):
 if a==b=='PERFECT':return 'CRITICAL'
 w=(2 if a=='PERFECT' else 1 if a=='GOOD' else 0)+(2 if b=='PERFECT' else 1 if b=='GOOD' else 0)
 return 'SUPER' if w>=3 else 'GREAT' if w==2 else 'HEAVY+' if w==1 else 'HEAVY'
def knock(t): return .047 if t=='CRITICAL' else .024 if t in ('PERFECT','SUPER') else .013 if t in ('GOOD','GREAT','HEAVY+') else .006
def jsround(x):return math.floor(x+.5)

def load():
 global MILESTONES
 p4a=json.loads(P4A.read_text()); sm=json.loads(P4AS.read_text()); rec=yaml.safe_load(REC.read_text()); kin=yaml.safe_load(KIN.read_text()); combat=yaml.safe_load(COMBAT.read_text()); skilled=yaml.safe_load(SKILLED.read_text()); shop=json.loads(SHOP.read_text()); p4d2=json.loads(P4D2.read_text())
 MILESTONES=tuple((lv,float(sm['firstPassMidpointAnchorCandidates'][str(lv)])) for lv in LEVELS)
 assert p4a['status']=='SYNTHETIC_CALIBRATION_FIXTURE_NOT_PRODUCTION_AUTHORING'; assert sm['status']=='P4A_MARKER_ONLY_DIAGNOSTIC_PASS_CANDIDATE_THRESHOLDS_NOT_FROZEN'; assert skilled['status']=='PROVISIONAL_DESIGN_CANDIDATE_NOT_PRODUCTION_FROZEN'; assert p4a['qualityCredit']==XP
 fxs={x['id']:x for x in p4a['fixtures'] if x['id'] in FXS}; byarch={r['archetype']:r for r in rec['recipes']}; assert set(fxs)==set(FXS); assert all(len(x['stages'])==50 for x in fxs.values())
 refs={a for f in fxs.values() for row in f['stages'] for a in row[0].split('+')}; assert refs.issubset(byarch),sorted(refs-set(byarch))
 return p4a,sm,fxs,byarch,kin,combat,skilled,shop,p4d2

def defs(p4d2):
 out={}
 for typ,row in p4d2['monsterAnchors'].items():
  out[typ]={'hp':float(row['hp']),'armor':float(row['armor']),'knockResist':float(row['knockResist']),'speed':float(row['speed'])}
  if typ=='SPLITTER':
   c=row['children']; out['SPLITTER_CHILD']={'hp':float(c['hp']),'armor':float(c['armor']),'knockResist':float(c['knockResist']),'speed':float(c['speed'])}
 return out

def shop_path(fx):
 costs={c:[jsround(v*fx['categoryMultipliers'][c]) for v in fx['rankBaseCosts']] for c in CATS}; assert sum(sum(v) for v in costs.values())==fx['fullShopReferenceCost']
 first=fx['stageIncomeWeight']['firstStage']; last=fx['stageIncomeWeight']['lastShopStage']; w={s:55+12*s for s in range(first,last+1)}; wt=sum(w.values()); wallet=0.; ranks={c:0 for c in CATS}; after={0:0}; total=fx['fullShopReferenceCost']*.50
 for stage in range(first,last+1):
  wallet+=total*w[stage]/wt
  while True:
   opts=[]
   for i,c in enumerate(CATS):
    r=ranks[c]
    if r<len(costs[c]) and wallet+1e-9>=costs[c][r]:opts.append((r,costs[c][r],i,c))
   if not opts:break
   _,price,_,c=min(opts); wallet-=price; ranks[c]+=1
  after[stage]=ranks['atk']
 entry={1:0}
 for s in range(2,51):entry[s]=after.get(s-1,after[last])
 assert ranks=={'atk':8,'crit':7,'critdmg':7,'fort':8,'def':7,'knock':8},ranks
 return entry,ranks

def stage_specs(fx,stage,byarch,kin):
 bundle=fx['stages'][stage-1][0].split('+'); out=[]; off=0; xoffs=kin.get('formationXOffsets',{})
 for arch in bundle:
  r=byarch[arch]; last=0; form=r.get('formation','F01')
  for q in r['spawns']:
   last=max(last,int(q['tMs'])); typ=q['type']; out.append({'tMs':off+int(q['tMs']),'type':typ,'y':float(q['y']),'xOffset':float(xoffs.get(form,{}).get(typ,0.)),'recipe':r['id']})
  off+=last+GAP_MS
 out.sort(key=lambda q:(q['tMs'],q['recipe'],q['type'],q['y'])); return out,bundle

def newrun(cls,sv,shop_on,skilled,fixed=None):
 model=skilled['model']; g=RNG(seed(sv,'JUDGMENT')); state=choose(model['initialState'],g.unit())
 return {'class':cls,'seed':sv,'shopOn':shop_on,'level':fixed or 1,'fixedLevel':fixed,'xp':0.,'combo':0,'comboPeak':0,'charge':0,'judgmentRng':g.state,'judgmentState':state,'procRng':seed(sv,'COMBAT_PROC'),'rootActions':0,'judgments':0,'expAwards':0,'n3Triggers':0,'generatedHits':0,'heavyActions':0,'pxpHeavy':0,'milestoneReach':{},'stageRows':[]}
def judge(r,skilled):
 model=skilled['model']; g=RNG(r['judgmentRng']); st=model['states'][r['judgmentState']]; j=choose(st['judgmentDistribution'],g.unit()); r['judgmentState']=choose(st['transitionAfterJudgment'],g.unit()); r['judgmentRng']=g.state; r['judgments']+=1; return j
def combo(r,j):
 if j=='PERFECT':
  r['combo']+=1; r['comboPeak']=max(r['comboPeak'],r['combo']); m=mile(r['combo']); return [m] if m else []
 r['combo']=0; return []
def levelof(xp):
 out=1
 for lv,thr in MILESTONES:
  if xp+1e-12>=thr:out=lv
 return out
def award(r,tier,stage):
 r['xp']+=XP[tier]; r['expAwards']+=1
 if r['fixedLevel'] is not None:return
 old=r['level']; new=levelof(r['xp'])
 if new>old:
  for lv,thr in MILESTONES:
   if old<lv<=new and str(lv) not in r['milestoneReach']:r['milestoneReach'][str(lv)]={'stage':stage,'rootActionIndex':r['rootActions'],'xp':round(r['xp'],6),'threshold':thr}
  r['level']=new

def alive(st):return [m for m in st['monsters'] if m['alive']]
def front(st):
 a=alive(st); return min(a,key=lambda m:(m['x'],m['id'])) if a else None
def find(st,mid):return next((m for m in st['monsters'] if m['id']==mid and m['alive']),None)
def behind(st,p,n,dy=LINE_Y):return sorted([m for m in alive(st) if m['id']!=p['id'] and m['x']>=p['x'] and abs(m['y']-p['y'])<=dy],key=lambda m:(m['x'],m['id']))[:n]
def nearby(st,p,dx,dy,n,exclude=()):
 ex=set(exclude)|{p['id']}; q=[]
 for m in alive(st):
  if m['id'] not in ex and abs(m['x']-p['x'])<=dx and abs(m['y']-p['y'])<=dy:q.append((math.hypot(m['x']-p['x'],m['y']-p['y']),m['id'],m))
 q.sort(); return [z[2] for z in q[:n]]
def spawn_children(st,p,d):
 for dy in (-.025,.025):
  y=max(.2,min(.72,p['y']+dy)); st['monsters'].append({'id':st['nextId'],'type':'SPLITTER_CHILD','x':p['x'],'y':y,'baseY':y,'hp':d['SPLITTER_CHILD']['hp'],'alive':True,'phase':'ADVANCE','phaseUntil':0,'bornMs':st['at']}); st['nextId']+=1
def hit(st,t,raw,tier,d,ignore=False,km=1.,defer_split=None):
 if not t or not t['alive']:return False
 md=d[t['type']]; t['hp']-=max(1,round(raw*(1. if ignore else md['armor']))); t['x']=min(1.2,t['x']+knock(tier)*md['knockResist']*km)
 if t['hp']<=0:
  t['alive']=False
  if t['type']=='SPLITTER':
   if defer_split is None:spawn_children(st,t,d)
   else:defer_split.append({'x':t['x'],'y':t['y']})
  return True
 return False
def spawn_deferred(st,rows,d):
 for q in rows:spawn_children(st,{'x':q['x'],'y':q['y']},d)
def critproc(r):
 g=RNG(r['procRng']); u=g.unit(); r['procRng']=g.state; return u<.06

def n3(r,st,d,m):
 p=front(st)
 if not p:return
 r['n3Triggers']+=1; parts=alloc(budget(m),weights(r['class'],m)); c=r['class']
 if c=='rogue':
  t=p
  for raw in parts:
   if not t or not t['alive']:t=front(st)
   if not t:break
   hit(st,t,raw,'NORMAL',d);r['generatedHits']+=1
  return
 hit(st,p,parts[0],'NORMAL',d,km=1.3 if c=='tank' and r['level']>=6 else 1.);r['generatedHits']+=1
 qs=behind(st,p,1) if c in ('knight','archer') else nearby(st,p,.13,.16,2) if c=='tank' else nearby(st,p,.12,.17,3)
 for q,raw in zip(qs,parts[1:]):hit(st,q,raw,'NORMAL',d,km=1.3 if c=='tank' and r['level']>=6 else 1.);r['generatedHits']+=1

def action(r,st,d,skilled,atk_rank):
 p=front(st)
 if not p:return ACTION_MS
 action_lv=r['level']; r['rootActions']+=1; st['rootActions']+=1; isheavy=r['charge']>=3; a=judge(r,skilled); b=judge(r,skilled) if isheavy else None; miles=[]
 if isheavy:
  r['heavyActions']+=1;miles+=combo(r,a);pred=r['combo']+1 if b=='PERFECT' else 0;tier=heavy(a,b);miles+=combo(r,b);r['pxpHeavy']+=1 if tier=='CRITICAL' else 0
 else:pred=r['combo']+1 if a=='PERFECT' else 0;tier=a;miles+=combo(r,a)
 hasp=a=='PERFECT' or b=='PERFECT';award(r,tier,st['stage']);raw=BASE[tier]*(1+cb(pred))*(1+.08*atk_rank);c=r['class'];lv=action_lv;p=front(st)
 if not p:return ACTION_MS
 lx,ly,pid=p['x'],p['y'],p['id']
 if c=='knight':
  if lv>=6:raw*=1.12
  if lv>=16 and hasp:raw*=1.18
  if lv>=21 and isheavy:raw*=1.20
  km=1.2 if lv>=16 and hasp else 1.;hit(st,p,raw,tier,d,km=km)
  if lv>=11:
   n=(3 if lv>=21 else 2) if isheavy else 1;coeff=1. if lv>=26 else .85
   for i,q in enumerate(behind(st,{'id':pid,'x':lx,'y':ly},n,.10 if isheavy else LINE_Y)):hit(st,q,raw*coeff,tier,d,km=km*((1.15+.15*i) if lv>=26 else 1.));r['generatedHits']+=1
 elif c=='rogue':
  if lv>=11 and critproc(r):raw=round(raw*1.5)
  hit(st,p,raw,tier,d)
  if lv>=6:
   count=4 if isheavy and lv>=21 else 1;coeff=.45 if isheavy and lv>=21 else .55;t=find(st,pid)
   for _ in range(count):
    if not t:t=front(st)
    if not t:break
    hit(st,t,raw*coeff,'NORMAL',d);r['generatedHits']+=1
    if not t['alive']:t=None
  if lv>=26 and hasp:
   cand=[m for m in alive(st) if m['id']!=pid]
   if cand:
    q=min(cand,key=lambda m:(math.hypot(m['x']-lx,m['y']-ly),m['id']));hit(st,q,raw*.45,'NORMAL',d);r['generatedHits']+=1
 elif c=='tank':
  km=(2. if isheavy and lv>=21 else 1.3) if lv>=6 else 1.;hit(st,p,raw,tier,d,km=km)
  if isheavy and lv>=21:
   for q in nearby(st,{'id':pid,'x':lx,'y':ly},TANK_DX,TANK_DY,999):hit(st,q,raw,tier,d,km=km);r['generatedHits']+=1
   if lv>=26:st['zones'].append({'x':lx,'y':ly,'expires':st['at']+ZONE_MS})
 elif c=='archer':
  if lv>=11:raw*=1.10
  ignore=lv>=16 and hasp;hit(st,p,raw,tier,d,ignore=ignore);extra=(4 if lv>=26 and hasp else 2) if lv>=6 else 0
  for q in behind(st,{'id':pid,'x':lx,'y':ly},extra):hit(st,q,raw if ignore else raw*.52,tier,d,ignore=ignore);r['generatedHits']+=1
  if isheavy and lv>=21:
   for _ in range(2):
    cand=[m for m in alive(st) if abs(m['y']-ly)<=LINE_Y and m['x']>=lx-.02];q=min(cand,key=lambda m:(m['x'],m['id'])) if cand else None
    if not q:continue
    sr=raw*.65;hit(st,q,sr,'NORMAL',d,ignore=ignore);r['generatedHits']+=1
    for qq in behind(st,{'id':q['id'],'x':q['x'],'y':q['y']},extra):hit(st,qq,sr if ignore else sr*.52,'NORMAL',d,ignore=ignore);r['generatedHits']+=1
 else:
  if lv>=21 and isheavy:raw*=1.20
  deferred=[];hit(st,p,raw,tier,d,defer_split=deferred);immediate={pid}
  if lv>=6:
   rx=MAGE_RX*(1.35 if lv>=11 else 1.)*(1.60 if isheavy and lv>=21 else 1.);ry=MAGE_RY*(1.35 if lv>=11 else 1.)*(1.60 if isheavy and lv>=21 else 1.);sp=.60 if lv>=11 else .50;origin={'id':pid,'x':lx,'y':ly}
   for q in nearby(st,origin,rx,ry,3):immediate.add(q['id']);hit(st,q,raw*sp,'NORMAL',d,defer_split=deferred);r['generatedHits']+=1
   spawn_deferred(st,deferred,d)
   if lv>=26 and len(immediate)>=2:
    cand=[m for m in alive(st) if m['id'] not in immediate];cand.sort(key=lambda m:(math.hypot(m['x']-lx,m['y']-ly),m['id']))
    for q in cand[:2]:hit(st,q,raw*.35,'NORMAL',d);r['generatedHits']+=1
   if lv>=16 and hasp:
    ring=[]
    for q in alive(st):
     if q['id']==pid:continue
     nd=math.hypot((q['x']-lx)/max(rx,1e-6),(q['y']-ly)/max(ry,1e-6))
     if .32<=nd<=1.05:ring.append((nd,q['id'],q))
    for _,_,q in sorted(ring)[:4]:hit(st,q,raw*.55,'NORMAL',d);r['generatedHits']+=1
  elif deferred:spawn_deferred(st,deferred,d)
 for m in miles:
  if m:n3(r,st,d,m)
 r['charge']=0 if isheavy else min(3,r['charge']+1)
 return round(ACTION_MS*.8) if c=='rogue' and lv>=16 and hasp else ACTION_MS

def advance(st,to,d,kin):
 while st['at']<to:
  dt=min(STEP_MS,to-st['at']);st['at']+=dt;st['zones']=[z for z in st['zones'] if z['expires']>st['at']];live=alive(st);support=[m for m in live if m['type']=='SUPPORTER']
  for m in live:
   typ=m['type'];speed=d[typ]['speed']
   if typ=='SIEGER' and m['x']<=float(kin['monsters']['SIEGER']['standoffX']):m['x']=float(kin['monsters']['SIEGER']['standoffX']);continue
   if typ=='CHARGER':
    trig=float(kin['monsters']['CHARGER']['triggerX'])
    if m['phase']=='ADVANCE' and m['x']<=trig:m['phase']='WINDUP';m['phaseUntil']=st['at']+int(kin['monsters']['CHARGER']['windupMs'])
    if m['phase']=='WINDUP':
     if st['at']>=m['phaseUntil']:m['phase']='CHARGE'
     else:speed=0.
    if m['phase']=='CHARGE':speed=float(kin['monsters']['CHARGER']['chargeSpeed'])
   if typ!='SUPPORTER':
    for s in support:
     if math.hypot(m['x']-s['x'],m['y']-s['y'])<=float(kin['monsters']['SUPPORTER']['auraRadius']):speed*=float(kin['monsters']['SUPPORTER']['auraSpeedMultiplier']);break
   for z in st['zones']:
    if abs(m['x']-z['x'])<=TANK_DX and abs(m['y']-z['y'])<=TANK_DY:speed*=ZONE_MULT;break
   m['x']=max(float(kin['world']['wallX']),m['x']-speed*dt/1000.)
   if typ=='FLYER':
    age=(st['at']-m['bornMs'])/1000.;m['y']=m['baseY']+float(kin['monsters']['FLYER']['oscillationAmplitude'])*math.sin(float(kin['monsters']['FLYER']['oscillationOmega'])*age)

def simstage(r,fx,stage,byarch,kin,d,skilled,atk):
 specs,bundle=stage_specs(fx,stage,byarch,kin);st={'stage':stage,'at':0,'idx':0,'nextId':1,'monsters':[],'rootActions':0,'zones':[]};next_action=0;maxlive=0
 while True:
  ns=specs[st['idx']]['tMs'] if st['idx']<len(specs) else None
  if not alive(st) and ns is None:break
  if not alive(st) and ns is not None and ns>st['at']:advance(st,ns,d,kin)
  while st['idx']<len(specs) and specs[st['idx']]['tMs']<=st['at']:
   q=specs[st['idx']];typ=q['type'];md=d[typ];st['monsters'].append({'id':st['nextId'],'type':typ,'x':float(kin['world']['spawnX'])+q['xOffset'],'y':q['y'],'baseY':q['y'],'hp':md['hp'],'alive':True,'phase':'ADVANCE','phaseUntil':0,'bornMs':st['at']});st['nextId']+=1;st['idx']+=1
  maxlive=max(maxlive,len(alive(st)))
  if alive(st):
   if next_action<st['at']:next_action=st['at']
   ev=min(next_action,specs[st['idx']]['tMs'] if st['idx']<len(specs) else next_action)
   if ev>st['at']:advance(st,ev,d,kin);continue
   if next_action<=st['at']:
    next_action=st['at']+action(r,st,d,skilled,atk)
    if r['level']>=31:break
  if st['at']>180000:raise RuntimeError(f'horizon {fx["id"]} S{stage} {r["class"]}')
 return {'stage':stage,'recipes':bundle,'rootActions':st['rootActions'],'maxLive':maxlive,'xpEnd':round(r['xp'],6),'levelEnd':r['level'],'comboEnd':r['combo'],'chargeEnd':r['charge'],'atkRank':atk}

def runcase(fx,cls,sv,on,byarch,kin,d,skilled,atkpath):
 r=newrun(cls,sv,on,skilled)
 for stage in range(1,51):
  row=simstage(r,fx,stage,byarch,kin,d,skilled,atkpath[stage] if on else 0);r['stageRows'].append(row)
  if r['level']>=31:break
 return r

def early(fxs,byarch,kin,d,skilled):
 fx=fxs['T1_CENTRAL'];rows=[]
 for cls in CLASSES:
  vals={1:[],6:[]}
  for lv in (1,6):
   for sv in (101,211,307):
    r=newrun(cls,sv,False,skilled,lv)
    for s in range(1,11):simstage(r,fx,s,byarch,kin,d,skilled,0)
    vals[lv].append(r['rootActions'])
  a=sum(vals[1])/3;b=sum(vals[6])/3;delta=(b/a-1)*100;exp='NEUTRAL' if cls in ('knight','tank') else 'REDUCED';ok=abs(delta)<=5 if exp=='NEUTRAL' else delta<-1
  rows.append({'class':cls,'lv1MeanRootActions':round(a,4),'lv6MeanRootActions':round(b,4),'deltaPct':round(delta,4),'expected':exp,'pass':ok})
 return rows
def isolated(fxs,byarch,kin,d,skilled,atkpath):
 rows=[];viol=[]
 for fxid in FXS:
  for cls in CLASSES:
   for stage,lv in ((10,6),(20,16),(30,21),(40,26)):
    pairs=[]
    for sv in (101,211,307):
     nums=[]
     for on in (False,True):
      r=newrun(cls,sv,on,skilled,lv);nums.append(simstage(r,fxs[fxid],stage,byarch,kin,d,skilled,atkpath[stage] if on else 0)['rootActions'])
     pairs.append({'seed':sv,'off':nums[0],'on':nums[1]})
     if nums[1]>nums[0]:viol.append({'fixture':fxid,'class':cls,'stage':stage,'level':lv,'seed':sv,'off':nums[0],'on':nums[1]})
    a=sum(x['off'] for x in pairs)/3;b=sum(x['on'] for x in pairs)/3;rows.append({'fixture':fxid,'class':cls,'stage':stage,'level':lv,'atkRank':atkpath[stage],'offMean':round(a,4),'onMean':round(b,4),'deltaPct':round((b/a-1)*100,4),'aggregateDirectionPass':b<=a+1e-12,'pairs':pairs})
 return rows,viol

def summarize(cases):
 g={}
 for c in cases:g.setdefault((c['fixture'],c['class'],c['shopOn']),[]).append(c)
 out=[]
 for (fx,cls,on),rows in sorted(g.items()):
  rr=[r['milestoneReach'].get('31') for r in rows];st=[x['stage'] for x in rr if x]
  out.append({'fixture':fx,'class':cls,'shopOn':on,'n':len(rows),'lv31ReachCount':len(st),'lv31ReachStageMean':round(sum(st)/len(st),4) if st else None,'lv31ReachStageMin':min(st) if st else None,'lv31ReachStageMax':max(st) if st else None,'rootActionsMean':round(sum(r['rootActions'] for r in rows)/len(rows),4),'xpMean':round(sum(r['xp'] for r in rows)/len(rows),4)})
 return out
def sha(paths):return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seeds',type=int,default=20);ap.add_argument('--output',type=Path);args=ap.parse_args();p4a,sm,fxs,byarch,kin,combat,skilled,shop,p4d2=load();d=defs(p4d2);atkpath,finalr=shop_path(shop);earlyrows=early(fxs,byarch,kin,d,skilled);isorows,isoviol=isolated(fxs,byarch,kin,d,skilled,atkpath);seedvals=[101+110*i for i in range(args.seeds)];cases=[]
 for fxid in FXS:
  for cls in CLASSES:
   for sv in seedvals:
    for on in (False,True):
     r=runcase(fxs[fxid],cls,sv,on,byarch,kin,d,skilled,atkpath);cases.append({'fixture':fxid,'class':cls,'seed':sv,'shopOn':on,'rootActions':r['rootActions'],'judgments':r['judgments'],'expAwards':r['expAwards'],'generatedHits':r['generatedHits'],'n3Triggers':r['n3Triggers'],'heavyActions':r['heavyActions'],'pxpHeavy':r['pxpHeavy'],'xp':round(r['xp'],6),'level':r['level'],'milestoneReach':r['milestoneReach'],'stageRows':r['stageRows']})
 inv=[]
 for c in cases:
  if c['expAwards']!=c['rootActions']:inv.append({'case':'EXP_AWARD_COUNT','key':[c['fixture'],c['class'],c['seed'],c['shopOn']]})
  if c['judgments']!=c['rootActions']+c['heavyActions']:inv.append({'case':'HEAVY_JUDGMENT_COUNT','key':[c['fixture'],c['class'],c['seed'],c['shopOn']]})
 idx={(c['fixture'],c['class'],c['seed'],c['shopOn']):c for c in cases};cum=[]
 for fxid in FXS:
  for cls in CLASSES:
   for sv in seedvals:
    a=idx[(fxid,cls,sv,False)];b=idx[(fxid,cls,sv,True)]
    for i in range(min(len(a['stageRows']),len(b['stageRows']))):
     if b['stageRows'][i]['rootActions']>a['stageRows'][i]['rootActions']:cum.append({'fixture':fxid,'class':cls,'seed':sv,'stage':i+1,'off':a['stageRows'][i]['rootActions'],'on':b['stageRows'][i]['rootActions']})
 result={'schemaVersion':'p6-b2-fresh-forward-progression-temp-v0.1','classification':'BOUNDED_DIAGNOSTIC_CONDITIONAL_ON_STAGE_ACCESS_NO_PRODUCTION_AUTHORITY','authority':{'contract':'154_P6_B2_FRESH_FORWARD_P6_AUTHORITY_AND_FIDELITY_CONTRACT_V0_1.md','survivalClaim':False,'shopTrajectoryStatus':'DIAGNOSTIC','expCreditsStatus':'PROVISIONAL','skillNumericStatus':'MIXED_STRUCTURAL_APPROVED_NUMERIC_PROVISIONAL'},'kernel':{'stageAccess':'FORCED_CONDITIONAL','wallArrival':'CLAMP_NOT_FAILURE','recipeBundleAssembly':'SERIAL_PACKETS_1500MS_GAP_DIAGNOSTIC','actionIntervalMs':ACTION_MS,'rogueLv16':'NEXT_ROOT_INTERVAL_X0.8_ON_PERFECT_CONTAINING_ROOT','archerLv11':'PROJECTILE_SPEED_ONLY_NO_ROOT_CADENCE_CHANGE','tankAftershockGeometry':'LEGACY_CONTINUOUS_Y_PROXY_DX0.16_DY0.10_NOT_AUTHORITY','levelUnlockChronology':'NEXT_ROOT_ACTION_ONLY','mageLv26Chronology':'IMMEDIATE_PACKAGE_THEN_DEATH_SPAWN_THEN_CHAIN_THEN_DELAYED_RESONANCE','stopAtLv31':True},'inputSha256':sha([P4A,P4AS,REC,KIN,COMBAT,SKILLED,SHOP,P4D2]),'inputs':{'fixtures':list(FXS),'seeds':seedvals,'classes':list(CLASSES),'shopLanes':['OFF','ATK_ON'],'atkPerRank':.08,'shopFinalRanks':finalr,'atkRankByEntryStage':atkpath,'milestoneThresholdCandidates':dict(MILESTONES),'markerOnlyCentralReachReference':sm['centralReachAtMidpointCandidates']},'checks':{'invariantFailures':inv,'earlyLv6Directional':earlyrows,'earlyLv6DirectionalPass':all(x['pass'] for x in earlyrows),'isolatedSameStageAtkDirection':isorows,'isolatedSameStageAtkAggregatePass':all(x['aggregateDirectionPass'] for x in isorows),'isolatedSameStageAtkPairViolations':isoviol,'isolatedSameStageAtkPairViolationCount':len(isoviol),'cumulativePathStageRootActionIncreases':cum,'cumulativePathStageRootActionIncreaseCount':len(cum),'productionValuesFrozen':False},'summary':summarize(cases),'cases':cases}
 text=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n';args.output.write_text(text,encoding='utf-8') if args.output else print(text,end='')
if __name__=='__main__':main()
