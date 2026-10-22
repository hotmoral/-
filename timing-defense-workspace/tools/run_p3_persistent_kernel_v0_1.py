#!/usr/bin/env python3
from __future__ import annotations
import argparse,copy,hashlib,heapq,json,math
from pathlib import Path
BASE={"NORMAL":100,"GOOD":140,"PERFECT":200,"HEAVY":180,"HEAVY+":230,"GREAT":300,"SUPER":400,"CRITICAL":600}
MASK=0xffffffff; FNV=2166136261; PRIME=16777619; ZERO=0x6D2B79F5
def seed(base,domain):
 h=FNV
 for b in f"{base}|{domain}".encode(): h=((h^b)*PRIME)&MASK
 return h or ZERO
class RNG:
 def __init__(self,s): self.state=s&MASK or ZERO
 def unit(self):
  x=self.state;x^=(x<<13)&MASK;x^=(x>>17)&MASK;x^=(x<<5)&MASK;self.state=x&MASK;return self.state/4294967296
def choose(d,u):
 a=0;last=None
 for k,v in d.items():
  last=k;a+=float(v)
  if u<a:return k
 return last
def hsh(o): return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def cb(c): return .15 if c>=30 else .12 if c>=20 else .08 if c>=10 else .05 if c>=5 else 0
def strong(x,y):
 if x==y=="PERFECT":return "CRITICAL"
 w=(2 if x=="PERFECT" else 1 if x=="GOOD" else 0)+(2 if y=="PERFECT" else 1 if y=="GOOD" else 0)
 return "SUPER" if w>=3 else "GREAT" if w==2 else "HEAVY+" if w==1 else "HEAVY"
def knock(t): return .047 if t=="CRITICAL" else .024 if t in ("PERFECT","SUPER") else .013 if t in ("GOOD","GREAT","HEAVY+") else .006
def mile(c): return c if c in (5,10,20,30) or (c>30 and c%10==0) else 0
def budget(m): return 210 if m>=30 else 150 if m>=20 else 90 if m>=10 else 60
def weights(c,m):
 if c=="rogue":
  n=5 if m>=30 else 4 if m>=20 else 3 if m>=10 else 2;return [1/n]*n
 return {"knight":[.67,.33],"tank":[.6,.2,.2],"archer":[.7,.3],"mage":[.55,.15,.15,.15]}[c]
def alloc(b,w):
 ex=[b*x for x in w];out=[math.floor(x) for x in ex];rem=b-sum(out);order=sorted(range(len(w)),key=lambda i:(-(ex[i]%1),i))
 for k in range(rem):out[order[k%len(order)]]+=1
 return out
def newrun(fx,cls,s,lane,account=None,hp=None):
 r=RNG(seed(s,"JUDGMENT"));st=choose(fx["centralModel"]["initialState"],r.unit());H=int(hp or fx["testControls"]["primaryBaseHpSentinel"])
 return {"runId":f"P3-{cls}-{s}-{lane}","classId":cls,"baseSeed":s,"lane":lane,"stage":1,"level":1,"exp":0,"expEligibleEvents":0,
 "runCoin":0,"shopRanks":{},"combo":0,"comboPeak":0,"charge":0,"baseMaxHp":H,"baseHp":H,"judgmentRng":r.state,"judgmentState":st,
 "combatProcRng":seed(s,"COMBAT_PROC"),"accountPermanent":copy.deepcopy(account or {"sentinelPermanent":17}),"temporaryEffects":{},"ledger":[],
 "stageSummaries":[],"n3Triggers":0,"lv6SkillHits":0,"status":"ACTIVE"}
def judge(run,fx):
 r=RNG(run["judgmentRng"]);s=fx["centralModel"]["states"][run["judgmentState"]];j=choose(s["judgmentDistribution"],r.unit())
 run["judgmentState"]=choose(s["transitionAfterJudgment"],r.unit());run["judgmentRng"]=r.state;run["expEligibleEvents"]+=1;return j
def combo(run,j):
 if j=="PERFECT":run["combo"]+=1;run["comboPeak"]=max(run["comboPeak"],run["combo"]);return [mile(run["combo"])] if mile(run["combo"]) else []
 run["combo"]=0;return []
def eff(base,mods):
 flat=sum(m["value"] for m in mods if m["operation"]=="FLAT_ADD");pct=sum(m["value"] for m in mods if m["operation"]=="PCT_ADD")
 return (base+flat)*(1+pct),[{"sourceId":m["sourceId"],"scope":m["scope"],"statId":"attack","operation":m["operation"],"value":m["value"]} for m in mods]
def alive(st):return [m for m in st["monsters"] if m["alive"]]
def front(st):return min(alive(st),key=lambda m:(m["x"],m["id"])) if alive(st) else None
def nearby(st,p,dx,dy,n):
 q=[(math.hypot(m["x"]-p["x"],m["y"]-p["y"]),m["id"],m) for m in alive(st) if m["id"]!=p["id"] and abs(m["x"]-p["x"])<dx and abs(m["y"]-p["y"])<dy];q.sort();return [x[2] for x in q[:n]]
def behind(st,p,n):
 q=[(m["x"],m["id"],m) for m in alive(st) if m["id"]!=p["id"] and m["x"]>p["x"] and abs(m["y"]-p["y"])<=.06];q.sort();return [x[2] for x in q[:n]]
def dmg(run,st,fx,t,raw,at,tier,eid,contrib=None,parent=None,tank=False):
 if not t or not t["alive"]:return
 ms=fx["monsters"][t["type"]];actual=max(1,round(raw*ms["armor"]));t["hp"]-=actual;t["x"]=min(.985,t["x"]+knock(tier)*ms["knockResist"]*(1.3 if tank else 1))
 run["ledger"].append({"recordType":"PowerAttribution","stage":st["stage"],"atMs":at,"actionId":st["actionSeq"],"parentActionId":parent,"sourceClass":run["classId"],
 "effectId":eid,"targetId":t["id"],"baseAmount":raw,"statContributions":contrib or [],"actionTransforms":{"timingTier":tier,"combo":run["combo"],"level":run["level"]},
 "targetTransforms":{"armor":ms["armor"]},"preMitigationAmount":raw,"finalAmount":actual,"shieldAbsorbed":0,"hpDamage":0})
 if t["hp"]<=0:t["alive"]=False
def sched(st,due,kind,p):st["queueSeq"]+=1;heapq.heappush(st["queue"],(due,st["queueSeq"],kind,p))
def n3(run,st,fx,m,at):
 p=front(st)
 if not p:return
 run["n3Triggers"]+=1;parts=alloc(budget(m),weights(run["classId"],m));c=run["classId"]
 if c=="rogue":
  for i,raw in enumerate(parts):sched(st,at+i*55,"n3",{"raw":raw,"targetId":p["id"],"effectId":"N3_FIXED_BUDGET"})
  return
 dmg(run,st,fx,p,parts[0],at,"NORMAL","N3_FIXED_BUDGET",parent=st["actionSeq"],tank=(c=="tank" and run["level"]>=6))
 qs=behind(st,p,1) if c in ("knight","archer") else nearby(st,p,.13,.16,2) if c=="tank" else nearby(st,p,.12,.17,3)
 for q,raw in zip(qs,parts[1:]):dmg(run,st,fx,q,raw,at,"NORMAL","N3_FIXED_BUDGET",parent=st["actionSeq"],tank=(c=="tank" and run["level"]>=6))
def action(run,st,fx,at,mods=None):
 p=front(st)
 if not p:st["nextAction"]=at+50;return
 st["actionSeq"]+=1;st["actions"]+=1;heavy=run["charge"]>=3;x=judge(run,fx);y=judge(run,fx) if heavy else None;mil=[]
 if heavy:mil+=combo(run,x);pred=run["combo"]+1 if y=="PERFECT" else 0;tier=strong(x,y or "NORMAL");mil+=combo(run,y or "NORMAL")
 else:pred=run["combo"]+1 if x=="PERFECT" else 0;tier=x;mil+=combo(run,x)
 raw,contrib=eff(BASE[tier]*(1+cb(pred)),mods or []);c=run["classId"];lv=run["level"]>=6
 if lv and c=="knight":raw*=1.12;contrib+=[{"sourceId":"LV6_KNIGHT_BLADE_WAVE","scope":"LEVEL","statId":"attack","operation":"PCT_MULT_EXPLICIT","value":.12}]
 pid=p["id"];dmg(run,st,fx,p,raw,at,tier,"PLAYER_BASE_ATTACK",contrib,tank=(lv and c=="tank"))
 if lv:
  pref=next((m for m in st["monsters"] if m["id"]==pid),p)
  if c=="rogue":sched(st,at+55,"lv6",{"targetId":pid,"raw":raw*.55,"effectId":"LV6_ROGUE_SECOND_HIT"})
  elif c=="archer":
   for q in behind(st,pref,2):dmg(run,st,fx,q,raw*.52,at,tier,"LV6_ARCHER_PENETRATION",parent=st["actionSeq"]);run["lv6SkillHits"]+=1
  elif c=="mage":
   for q in nearby(st,pref,.105,.16,3):dmg(run,st,fx,q,raw*.5,at,"SKILL","LV6_MAGE_SPLASH",parent=st["actionSeq"]);run["lv6SkillHits"]+=1
  elif c=="tank":run["ledger"].append({"recordType":"EffectAttribution","stage":st["stage"],"atMs":at,"actionId":st["actionSeq"],"sourceClass":c,"effectId":"LV6_TANK_KNOCKBACK_X1_30","finalAmount":0})
 for m in mil:n3(run,st,fx,m,at)
 run["charge"]=0 if heavy else min(3,run["charge"]+1);st["nextAction"]=at+fx["testControls"]["actionIntervalMs"]
def specs(fx,cfg):
 out=[]
 for ph in cfg["phases"]:
  for s in fx["recipes"][ph["recipeId"]]["spawns"]:x=dict(s);x["tMs"]+=ph["offsetMs"];out.append(x)
 return sorted(out,key=lambda x:(x["tMs"],x["type"],x["y"]))
def newstage(fx,cfg):return {"stage":cfg["stage"],"at":0,"idx":0,"nextId":1,"monsters":[],"queue":[],"queueSeq":0,"nextAction":0,"actionSeq":0,"actions":0,"wallDamage":0,"baseHpStart":None,"jrStart":None,"jeStart":None,"specs":specs(fx,cfg),"temporaryObjects":{}}
def simstage(run,fx,cfg,st=None,stop=None,mods=None):
 st=copy.deepcopy(st) if st else newstage(fx,cfg)
 if st["baseHpStart"] is None:st["baseHpStart"]=run["baseHp"];st["jrStart"]=run["judgmentRng"];st["jeStart"]=run["expEligibleEvents"]
 dt=fx["testControls"]["timeStepMs"]
 while st["at"]<=60000:
  at=st["at"]
  while st["idx"]<len(st["specs"]) and st["specs"][st["idx"]]["tMs"]<=at:
   s=st["specs"][st["idx"]];ms=fx["monsters"][s["type"]];st["monsters"].append({"id":st["nextId"],"type":s["type"],"x":fx["world"]["spawnX"],"y":s["y"],"hp":ms["hp"],"alive":True});st["nextId"]+=1;st["idx"]+=1
  while st["queue"] and st["queue"][0][0]<=at:
   due,_,kind,p=heapq.heappop(st["queue"]);t=next((m for m in st["monsters"] if m["id"]==p["targetId"] and m["alive"]),None) or front(st)
   if t:dmg(run,st,fx,t,p["raw"],due,"SKILL" if kind=="lv6" else "NORMAL",p["effectId"],parent=st["actionSeq"]);run["lv6SkillHits"]+=1 if kind=="lv6" else 0
  if at>=st["nextAction"]:action(run,st,fx,at,mods)
  for m in alive(st):m["x"]-=fx["monsters"][m["type"]]["speed"]*(dt/1000)
  for m in list(alive(st)):
   if m["x"]<=fx["world"]["wallX"]:
    m["alive"]=False;wd=fx["monsters"][m["type"]]["wallDamage"];run["baseHp"]-=wd;st["wallDamage"]+=wd
    run["ledger"].append({"recordType":"PowerAttribution","stage":st["stage"],"atMs":at,"actionId":None,"parentActionId":None,"sourceClass":"system","effectId":m["type"]+"_WALL_HIT","targetId":"BASE","baseAmount":wd,"statContributions":[],"actionTransforms":{},"targetTransforms":{},"preMitigationAmount":wd,"finalAmount":wd,"shieldAbsorbed":0,"hpDamage":wd})
    if run["baseHp"]<=0:run["status"]="FAILED";return {"status":"FAILED","run":run,"stage":st}
  if stop is not None and at>=stop:return {"status":"SNAPSHOT","snapshot":{"run":copy.deepcopy(run),"stage":copy.deepcopy(st)}}
  if st["idx"]>=len(st["specs"]) and not alive(st) and not st["queue"]:
   run["temporaryEffects"].clear();st["temporaryObjects"].clear();delta=st["baseHpStart"]-run["baseHp"];lh=sum(x.get("hpDamage",0) for x in run["ledger"] if x.get("stage")==st["stage"])
   sm={"stage":st["stage"],"actions":st["actions"],"wallDamage":st["wallDamage"],"baseHpStart":st["baseHpStart"],"baseHpEnd":run["baseHp"],"hpDelta":delta,"ledgerHpDamage":lh,"comboEnd":run["combo"],"chargeEnd":run["charge"],"levelEnd":run["level"],"settled":True,"judgmentRngStart":st["jrStart"],"judgmentRngEnd":run["judgmentRng"],"expEligibleEventsStart":st["jeStart"],"expEligibleEventsEnd":run["expEligibleEvents"]}
   run["stageSummaries"].append(sm)
   if delta!=lh:raise AssertionError("base HP ledger mismatch")
   return {"status":"STAGE_SETTLED","run":run,"summary":sm}
  st["at"]+=dt
 raise RuntimeError("stage horizon")
def primary(fx,cls,s,lane,start=1,run=None):
 run=copy.deepcopy(run) if run else newrun(fx,cls,s,lane)
 for sn in range(start,11):
  if lane=="FORCED_LV6_TRANSITION" and sn==6 and run["level"]<6:run["level"]=6;run["ledger"].append({"recordType":"StateTransition","stage":sn,"effectId":"TEST_HOOK_FORCED_LV6","fromLevel":1,"toLevel":6})
  o=simstage(run,fx,fx["stages"][sn-1]);run=o["run"]
  if o["status"]=="FAILED":break
  run["stage"]=sn+1
 v={k:x for k,x in run.items() if k!="ledger"};v["ledgerHash"]=hsh(run["ledger"]);v["finalHash"]=hsh(v);return run,v
def retry(fx,r):return newrun(fx,r["classId"],r["baseSeed"],r["lane"],r["accountPermanent"])
def fixtures(fx):
 rows=[];empty={"stage":99,"phases":[]};ms=fx["monsters"]["GRUNT"]
 r=newrun(fx,"knight",101,"LV1_CONTINUITY");r["charge"]=3;o=simstage(r,fx,empty);r=o["run"];s=newstage(fx,{"stage":100,"phases":[]});s["monsters"]=[{"id":1,"type":"GRUNT","x":1.0,"y":.46,"hp":ms["hp"],"alive":True}];before=r["judgmentRng"];action(r,s,fx,0);rows.append({"fixture":"F1_CHARGE_CONTINUITY","pass":o["status"]=="STAGE_SETTLED" and r["charge"]==0 and r["judgmentRng"]!=before})
 r=newrun(fx,"knight",101,"LV1_CONTINUITY");r["combo"]=4;r["judgmentState"]="FOCUS";o=simstage(r,fx,empty);r=o["run"];s=newstage(fx,{"stage":100,"phases":[]});s["monsters"]=[{"id":1,"type":"GRUNT","x":1.0,"y":.46,"hp":9999,"alive":True}];action(r,s,fx,0);rows.append({"fixture":"F2_COMBO_N3_BOUNDARY","pass":r["combo"]>=5 and r["n3Triggers"]>=1})
 weak=[{"sourceId":"P3_FAILURE_TEST","scope":"RUN","operation":"PCT_ADD","value":-.99}];r=newrun(fx,"mage",211,"LV1_CONTINUITY",hp=50);r.update({"level":6,"exp":99,"runCoin":7,"shopRanks":{"ATK":2},"combo":12,"charge":2});o=simstage(r,fx,fx["stages"][4],mods=weak);fr=o["run"];rr=retry(fx,fr);ok=o["status"]=="FAILED" and rr["stage"]==1 and rr["level"]==1 and rr["exp"]==0 and rr["runCoin"]==0 and rr["shopRanks"]=={} and rr["combo"]==rr["charge"]==0 and rr["baseHp"]==rr["baseMaxHp"] and rr["accountPermanent"]==fr["accountPermanent"];rows.append({"fixture":"F3_FAILURE_RETRY_RESET","pass":ok})
 u,uv=primary(fx,"archer",307,"FORCED_LV6_TRANSITION");p=newrun(fx,"archer",307,"FORCED_LV6_TRANSITION")
 for sn in range(1,6):p=simstage(p,fx,fx["stages"][sn-1])["run"];p["stage"]=sn+1
 rv=primary(fx,"archer",307,"FORCED_LV6_TRANSITION",6,json.loads(json.dumps(p)))[1];r=newrun(fx,"rogue",211,"LV1_CONTINUITY");cfg=fx["stages"][4];full=simstage(copy.deepcopy(r),fx,cfg);snap=simstage(copy.deepcopy(r),fx,cfg,stop=2500)["snapshot"];res=simstage(json.loads(json.dumps(snap["run"])),fx,cfg,json.loads(json.dumps(snap["stage"])));mid=hsh({k:v for k,v in full["run"].items() if k!="ledger"}|{"ledgerHash":hsh(full["run"]["ledger"])})==hsh({k:v for k,v in res["run"].items() if k!="ledger"}|{"ledgerHash":hsh(res["run"]["ledger"])});rows.append({"fixture":"F4_SNAPSHOT_RESUME_EQUIVALENCE","pass":uv["finalHash"]==rv["finalHash"] and mid})
 mods=[{"sourceId":"STAR_TEST","scope":"ACCOUNT","operation":"PCT_ADD","value":.1},{"sourceId":"ACH_TEST","scope":"CLASS_PERMANENT","operation":"PCT_ADD","value":.2},{"sourceId":"SHOP_TEST","scope":"RUN","operation":"PCT_ADD","value":.3}];e,c=eff(100,mods);r=newrun(fx,"knight",307,"LV1_CONTINUITY");r["judgmentState"]="FOCUS";s=newstage(fx,{"stage":101,"phases":[]});s["monsters"]=[{"id":1,"type":"GRUNT","x":1.0,"y":.46,"hp":9999,"alive":True}];action(r,s,fx,0,mods);src={x["sourceId"] for x in [z for z in r["ledger"] if z.get("effectId")=="PLAYER_BASE_ATTACK"][-1]["statContributions"]};rows.append({"fixture":"F5_MODIFIER_AGGREGATION_ATTRIBUTION","pass":abs(e-160)<1e-9 and src=={"STAR_TEST","ACH_TEST","SHOP_TEST"}})
 r=newrun(fx,"tank",101,"LV1_CONTINUITY");r["temporaryEffects"]={"TEST":1};o=simstage(r,fx,fx["stages"][0]);rows.append({"fixture":"F6_TEMPORARY_EFFECT_BOUNDARY","pass":o["run"]["temporaryEffects"]=={}})
 ns=newstage(fx,fx["stages"][1]);rows.append({"fixture":"F7_NO_TRANSIENT_LEAKAGE","pass":ns["monsters"]==[] and ns["queue"]==[] and ns["temporaryObjects"]=={} and ns["at"]==ns["idx"]==0})
 weak=[{"sourceId":"P3_ATTRITION_TEST","scope":"RUN","operation":"PCT_ADD","value":-.99}];r=newrun(fx,"knight",307,"LV1_CONTINUITY",hp=5000);o1=simstage(r,fx,fx["stages"][4],mods=weak);h1=o1["run"]["baseHp"];o2=simstage(o1["run"],fx,fx["stages"][5],mods=weak);h2=o2["run"]["baseHp"];rows.append({"fixture":"F8_BASE_HP_ATTRITION_CONTINUITY","pass":h1<5000 and o2["summary"]["baseHpStart"]==h1 and h2<=h1,"startHp":5000,"afterStage1":h1,"afterStage2":h2});return rows
def execute(fx):
 rows=[]
 for c in fx["testControls"]["classes"]:
  for s in fx["testControls"]["baseSeeds"]:
   for lane in fx["testControls"]["lanes"]:
    r,v=primary(fx,c,s,lane);r2,v2=primary(fx,c,s,lane);lv=sum(1 for e in r["ledger"] if str(e.get("effectId","")).startswith("LV6_") or any(str(x.get("sourceId","")).startswith("LV6_") for x in e.get("statContributions",[])));cont=all(r["stageSummaries"][i+1]["judgmentRngStart"]==r["stageSummaries"][i]["judgmentRngEnd"] and r["stageSummaries"][i+1]["expEligibleEventsStart"]==r["stageSummaries"][i]["expEligibleEventsEnd"] for i in range(9));rows.append({"classId":c,"seed":s,"lane":lane,"stagesCompleted":len(r["stageSummaries"]),"status":r["status"],"finalHash":v["finalHash"],"replayHash":v2["finalHash"],"deterministic":v["finalHash"]==v2["finalHash"],"baseHpEnd":r["baseHp"],"comboPeak":r["comboPeak"],"lv6AttributionEntries":lv,"playerStreamContinuous":cont})
 fs=fixtures(fx);ok=all(r["deterministic"] and r["stagesCompleted"]==10 and r["status"]=="ACTIVE" and r["playerStreamContinuous"] and ((r["lane"]=="FORCED_LV6_TRANSITION" and r["lv6AttributionEntries"]>0) or (r["lane"]=="LV1_CONTINUITY" and r["lv6AttributionEntries"]==0)) for r in rows) and all(x["pass"] for x in fs);return rows,fs,{"recordType":"P3_AUDIT_SUMMARY","classification":"P3_STRUCTURAL_PASS" if ok else "P3_STRUCTURAL_FAIL","primaryRuns":len(rows),"fixtureCount":len(fs),"combo40ObservedRuns":sum(r["comboPeak"]>=40 for r in rows),"warning":"Structural integration only; no balance number frozen."}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--fixture",type=Path,default=Path(__file__).resolve().parents[1]/"legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json");a=ap.parse_args();fx=json.loads(a.fixture.read_text());r,f,s=execute(fx);print(json.dumps(s,separators=(",",":")));return 0 if s["classification"]=="P3_STRUCTURAL_PASS" else 2
if __name__=="__main__":raise SystemExit(main())
