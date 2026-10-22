#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_CORPUS=ROOT/'legacy-game-structure'/'data'/'p4a_marker_opportunity_corpus_v0_1.json'

WINDOWS={6:(5,7),11:(11,14),16:(18,21),21:(25,28),26:(32,36),31:(41,45)}
CENTERS={6:6,11:13,16:20,21:27,26:34,31:43}
TIERS=['T1','T2','T3','T4']; ENVS=['LOW','CENTRAL','HIGH']
CLASSES=['knight','rogue','tank','archer','mage']
PRANGES={
'T1':{'BASELINE':(19,30),'FLOOD':(5,11),'RUSH':(9,17),'BULWARK':(9,17)},
'T2':{'BASELINE':(14,22),'FLOOD':(5,11),'RUSH':(9,17),'BULWARK':(19,30),'AERIAL':(14,22)},
'T3':{'BASELINE':(9,17),'FLOOD':(14,22),'RUSH':(14,22),'BULWARK':(9,17),'BREACH':(19,30),'AERIAL':(9,17),'REPLICATE':(19,30)},
'T4':{'BASELINE':(5,11),'FLOOD':(5,11),'RUSH':(9,17),'BULWARK':(14,22),'BREACH':(9,17),'AERIAL':(9,17),'REPLICATE':(9,17),'SUPPORT':(19,30),'SIEGE':(19,30)}}
CRANGES={'T1':{0:(8,14),1:(22,30),2:(8,15),3:(0,4),4:(0,0)},'T2':{0:(4,8),1:(15,22),2:(18,25),3:(4,8),4:(0,2)},'T3':{0:(2,5),1:(10,16),2:(19,26),3:(8,14),4:(0,3)},'T4':{0:(2,4),1:(8,14),2:(16,22),3:(14,20),4:(1,4)}}
LEGAL={'T1':set(['E01','E02','E03']),'T2':set(['E01','E02','E03','E04','E05','E06','E14']),'T3':set(['E01','E02','E03','E04','E05','E06','E07','E08','E13','E14','E15','E17','E20']),'T4':set(f'E{i:02d}' for i in range(1,21))}
EARLIEST={t:{r:1 for r in LEGAL[t]} for t in LEGAL}
EARLIEST['T1'].update({'E02':5,'E03':15}); EARLIEST['T2'].update({'E04':5,'E05':8,'E06':15,'E14':18})
EARLIEST['T3'].update({'E07':5,'E13':8,'E17':10,'E08':15,'E15':18,'E20':23}); EARLIEST['T4'].update({'E09':11,'E12':14,'E16':14,'E10':22,'E11':25,'E18':25,'E19':31})
TEACH={'T1':{5:'E02',15:'E03'},'T2':{5:'E04',15:'E06'},'T3':{5:'E07',15:'E08'},'T4':{11:'E09',22:'E10'}}
OPP={'E01':{'knight','archer','mage'},'E02':{'rogue','tank'},'E03':{'rogue','knight'},'E04':{'rogue','archer'},'E05':{'rogue','knight','archer'},'E06':{'archer','mage'},'E07':{'tank','rogue'},'E08':{'mage','tank'},'E09':{'mage','rogue'},'E10':{'tank','archer'},'E11':{'archer','knight','tank'},'E12':{'rogue','mage','knight'},'E13':{'tank','rogue'},'E14':{'archer','tank'},'E15':{'mage','rogue'},'E16':{'mage','knight'},'E17':{'tank','archer','knight'},'E18':{'archer','tank','mage'},'E19':set(CLASSES),'E20':{'tank','mage','rogue'}}
FORM={'T1':set(['F01','F02','F03','F04','F08']),'T2':set(['F01','F02','F03','F04','F05','F08']),'T3':set(['F01','F02','F03','F04','F05','F08','F09']),'T4':set(f'F{i:02d}' for i in range(1,10))}
CAD={'T1':set(['CD01','CD02','CD03','CD04','CD05']),'T2':set(['CD01','CD02','CD03','CD04','CD05','CD07']),'T3':set(['CD01','CD02','CD03','CD04','CD05','CD07','CD08']),'T4':set(f'CD{i:02d}' for i in range(1,9))}

def normalize_corpus(corpus):
    schema=corpus.get('stageRowSchema')
    if not schema:return corpus
    for fx in corpus.get('fixtures',[]):
        if fx.get('stages') and isinstance(fx['stages'][0],list):
            rows=[]
            for row in fx['stages']:
                d=dict(zip(schema,row))
                d['recipeBundle']=str(d['recipeBundle']).split('+') if d['recipeBundle'] else []
                d['pressureFamilies']=str(d['pressureFamilies']).split(',') if d['pressureFamilies'] else []
                rows.append(d)
            fx['stages']=rows
    return corpus

class XS:
    def __init__(self,s:int): self.x=(s&0xffffffff) or 0x6D2B79F5
    def unit(self):
        x=self.x; x^=(x<<13)&0xffffffff; x^=x>>17; x^=(x<<5)&0xffffffff; self.x=x&0xffffffff; return self.x/2**32
class Central:
    def __init__(self,s:int): self.r=XS(s); self.focus=self.r.unit()<.4
    def judge(self):
        if self.focus:
            self.focus=self.r.unit()<.98; return 'P'
        u=self.r.unit(); q='P' if u<.5 else 'G' if u<.5+1/3 else 'N'
        if self.r.unit()<1/75:self.focus=True
        return q

def derived_seed(t,e,i): return int.from_bytes(hashlib.sha256(f'P4A|{t}|{e}|{i}'.encode()).digest()[:4],'little') or 1
def quant(v,p):
    a=sorted(v); pos=(len(a)-1)*p; lo=math.floor(pos); hi=math.ceil(pos); f=pos-lo
    return a[lo]*(1-f)+a[hi]*f

def heavy_tier(a,b):
    if a=='P' and b=='P': return 'CRITICAL'
    z=(2 if a=='P' else 1 if a=='G' else 0)+(2 if b=='P' else 1 if b=='G' else 0)
    return 'SUPER' if z>=3 else 'GREAT' if z==2 else 'HEAVY+' if z==1 else 'HEAVY'

def simulate(stages,t,e,seed_i,credit):
    p=Central(derived_seed(t,e,seed_i)); action_no=1; cum=0.; rows=[]
    dmg_n={'N':100,'G':140,'P':200}; dmg_h={'HEAVY':180,'HEAVY+':230,'GREAT':300,'SUPER':400,'CRITICAL':600}
    c_n={'N':credit['NORMAL'],'G':credit['GOOD'],'P':credit['PERFECT']}
    c_h={k:credit[k] for k in ['HEAVY','HEAVY+','GREAT','SUPER','CRITICAL']}
    for st in stages:
        workload=float(st['workloadEhp']); turns=0; stage_credit=0.
        while workload>0:
            if action_no%4==0:
                a=p.judge(); b=p.judge(); q=heavy_tier(a,b); damage=dmg_h[q]; gain=c_h[q]
            else:
                q=p.judge(); damage=dmg_n[q]; gain=c_n[q]
            workload-=damage; cum+=gain; stage_credit+=gain; turns+=1; action_no+=1
        rows.append({'stage':int(st['stage']),'turns':turns,'stageCredit':stage_credit,'cumCredit':cum})
    return rows

def unlock_stage(rows,thr):
    for r in rows:
        if r['cumCredit']>=thr:return r['stage']
    return 51

def validate_static(corpus):
    flags={'fixtureCount':len(corpus['fixtures'])==12,'pressureRange':True,'complexityRange':True,'classOpportunity10Stage':True,'c4Guards':True,'vocabulary':True,'exactSignatureTriple':True,'availabilityAndTeach':True}
    for fx in corpus['fixtures']:
        t=fx['tier']; stages=fx['stages']; flags['fixtureCount'] &= len(stages)==50
        pc=Counter(p for s in stages for p in s['pressureFamilies']); cc=Counter(int(s['dominantComplexity']) for s in stages)
        for p,(lo,hi) in PRANGES[t].items(): flags['pressureRange'] &= lo<=pc[p]<=hi
        for c,(lo,hi) in CRANGES[t].items(): flags['complexityRange'] &= lo<=cc[c]<=hi
        for s in stages:
            sn=int(s['stage']); bundle=s['recipeBundle']
            flags['availabilityAndTeach'] &= all(r in LEGAL[t] and sn>=EARLIEST[t].get(r,1) for r in bundle)
            flags['vocabulary'] &= s['formationId'] in FORM[t] and s['cadenceId'] in CAD[t]
        for sn,r in TEACH[t].items(): flags['availabilityAndTeach'] &= stages[sn-1]['recipeBundle']==[r]
        for start in range(0,41):
            os=set()
            for s in stages[start:start+10]:
                for r in s['recipeBundle']: os |= OPP[r]
            flags['classOpportunity10Stage'] &= set(CLASSES)<=os
        cs=[int(s['dominantComplexity']) for s in stages]
        flags['c4Guards'] &= all(not(cs[i]==4 and cs[i+1]==4) for i in range(49))
        flags['c4Guards'] &= all(sum(c==4 for c in cs[i:i+5])<=2 for i in range(46))
        flags['c4Guards'] &= sum(c==4 for c in cs[40:45])<=1
        sig=[(tuple(s['recipeBundle']),tuple(s['pressureFamilies']),s['dominantComplexity'],s['formationId'],s['cadenceId']) for s in stages]
        flags['exactSignatureTriple'] &= all(not(sig[i]==sig[i+1]==sig[i+2]) for i in range(48))
    return flags

def compute(corpus,seeds=100):
    credit=corpus['qualityCredit']; by={(fx['tier'],fx['envelope']):fx for fx in corpus['fixtures']}
    runs={(t,e):[simulate(by[(t,e)]['stages'],t,e,i,credit) for i in range(1,seeds+1)] for t in TIERS for e in ENVS}
    intervals={}; anchors={}; central_reach={}; env_p50={}
    for lv,(lo,hi) in WINDOWS.items():
        lower=max(quant([r[lo-2]['cumCredit'] if lo>1 else 0 for r in runs[(t,'CENTRAL')]],.5) for t in TIERS)
        upper=min(quant([r[hi-1]['cumCredit'] for r in runs[(t,'CENTRAL')]],.5) for t in TIERS)
        intervals[str(lv)]={'lowerExclusive':lower,'upperInclusive':upper,'nonEmpty':lower<upper}
        thr=(lower+upper)/2; anchors[str(lv)]=thr
        central_reach[str(lv)]={}; env_p50[str(lv)]={}
        for t in TIERS:
            us=[unlock_stage(r,thr) for r in runs[(t,'CENTRAL')]]
            central_reach[str(lv)][t]={k:quant(us,p) for k,p in [('P25',.25),('P50',.5),('P75',.75),('P90',.9)]}
            for e in ENVS:
                us2=[unlock_stage(r,thr) for r in runs[(t,e)]]
                env_p50[str(lv)][f'{t}_{e}']=quant(us2,.5)
    metrics={}
    for t in TIERS:
        for e in ENVS:
            fx=by[(t,e)]; rs=runs[(t,e)]; key=f'{t}_{e}'
            pc=Counter(p for s in fx['stages'] for p in s['pressureFamilies']); cc=Counter(str(s['dominantComplexity']) for s in fx['stages'])
            metrics[key]={'workloadEhp':sum(float(s['workloadEhp']) for s in fx['stages']),'twoPackageStages':sum(len(s['recipeBundle'])==2 for s in fx['stages']),'turnsP50':quant([sum(x['turns'] for x in r) for r in rs],.5),'creditP50Stage50':quant([r[-1]['cumCredit'] for r in rs],.5),'pressureCounts':dict(sorted(pc.items())),'complexityCounts':dict(sorted(cc.items()))}
    return {
      'version':'p4a-marker-inverse-design-summary-v0.1',
      'status':'P4A_MARKER_ONLY_DIAGNOSTIC_PASS_CANDIDATE_THRESHOLDS_NOT_FROZEN',
      'simulationSeedsPerFixture':seeds,
      'validation':validate_static(corpus),
      'centralP50FeasibleThresholdIntervals':intervals,
      'firstPassMidpointAnchorCandidates':anchors,
      'centralReachAtMidpointCandidates':central_reach,
      'allEnvelopeP50ReachAtMidpointCandidates':env_p50,
      'fixtureMetrics':metrics,
      'initialDiagnostic':{
        'finding':'Before bounded T2/T4 central workload redistribution, universal central P50 threshold intervals were empty at Lv16 and Lv21 while Lv6/Lv11/Lv26/Lv31 were feasible.',
        'action':'Small synthetic workload redistribution within existing Tier identity/ranges: T2 mid-band workload shifted later; T4 support/siege-compatible workload shifted earlier.',
        'result':'All six CENTRAL T1-T4 P50 threshold intervals became non-empty without Tier-specific XP multipliers.'},
      'watches':[
        'LOW/HIGH opportunity envelopes are stress envelopes and are not required to hit every candidate milestone window.',
        'P4-B skill power can materially change event opportunity and must rerun reach.',
        'workloadEhp is a relative marker-only opportunity proxy, not production difficulty or Stage HP authority.',
        'exact anchors, quality vector and percentile tail acceptance gates remain unfrozen.']}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--corpus',type=Path,default=DEFAULT_CORPUS); ap.add_argument('--seeds',type=int,default=100); ap.add_argument('--output',type=Path)
    a=ap.parse_args(); corpus=normalize_corpus(json.loads(a.corpus.read_text(encoding='utf-8'))); out=compute(corpus,a.seeds); text=json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)
    if a.output:a.output.write_text(text+'\n',encoding='utf-8')
    else:print(text)
if __name__=='__main__':main()
