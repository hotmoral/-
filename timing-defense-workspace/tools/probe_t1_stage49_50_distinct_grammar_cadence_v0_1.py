#!/usr/bin/env python3
"""T1 Stage49-50 distinct-grammar-cadence probe v0.1.

The prior rotating-grammar candidate used the same 400ms spawn rhythm for every grammar.
That made LINE/CLUSTER/FRONTLINE/SCATTER differ mostly by labels and y/type placement,
not by actual x-depth/temporal density. This probe gives each grammar its own chronology:

LINE             = narrow y corridor + long temporal depth (Archer line-depth opportunity)
CLUSTER          = compact burst in x/y (Mage fixed-area opportunity)
FRONTLINE        = early durable front + delayed light rear (Knight/Tank disruption opportunity)
DURABLE_SCATTER  = distributed durable anchors + fast bodies (Rogue focus/retarget opportunity)

Only Stage49-50 composition/geometry/chronology changes. Stage46-48 and all combat scalars
remain exact v0.2. Archer Lv31 uses yTol=0.20 only as the existing diagnostic continuous
MID_ADJACENT bridge; no collision-width freeze is made.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import probe_t1_stage49_50_class_rotation_shape_v0_1 as shape
import probe_t1_archer_lv31_continuous_corridor_bridge_v0_1 as widthbridge
import probe_t1_stage49_50_rotating_grammar_phase_attribution_v0_1 as phaseprobe

r=shape.r
WIDTH=0.20
ACTIVE=[6,11,16,21,26,31]

GRAMMARS={
    'LINE': {
        'offsets':[0,650,1300,1950,2600,3250],
        'bodies':[('GRUNT',0.46),('RUNNER',0.48),('BRUTE',0.46),('GRUNT',0.44),('RUNNER',0.50),('BRUTE',0.46)],
    },
    'CLUSTER': {
        'offsets':[0,120,240,360,480,600],
        'bodies':[('GRUNT',0.42),('RUNNER',0.46),('GRUNT',0.50),('RUNNER',0.44),('BRUTE',0.48),('GRUNT',0.43)],
    },
    'FRONTLINE': {
        'offsets':[0,200,400,1000,1400,1800],
        'bodies':[('BRUTE',0.44),('BRUTE',0.48),('BRUTE',0.50),('GRUNT',0.46),('RUNNER',0.42),('RUNNER',0.54)],
    },
    'DURABLE_SCATTER': {
        'offsets':[0,300,600,900,1200,1500],
        'bodies':[('BRUTE',0.18),('RUNNER',0.82),('BRUTE',0.78),('RUNNER',0.22),('GRUNT',0.50),('BRUTE',0.54)],
    },
}

ORDERS={
    'ORDER_A': {
        49:['DURABLE_SCATTER','LINE','FRONTLINE','CLUSTER'],
        50:['LINE','CLUSTER','FRONTLINE','DURABLE_SCATTER','LINE_REPRISE'],
    },
    'ORDER_B': {
        49:['LINE','DURABLE_SCATTER','CLUSTER','FRONTLINE'],
        50:['FRONTLINE','LINE','CLUSTER','DURABLE_SCATTER','LINE_REPRISE'],
    },
}


def base_name(name:str):
    return 'LINE' if name=='LINE_REPRISE' else name


def build_stage(names:list[str],gap_ms:int):
    rows=[]
    for i,name in enumerate(names):
        g=GRAMMARS[base_name(name)]; base=i*gap_ms
        for off,(typ,y) in zip(g['offsets'],g['bodies']):
            rows.append({'tMs':base+off,'type':typ,'y':y})
    return rows


def candidate(source:dict,cid:str,order_key:str,gap_ms:int):
    doc=copy.deepcopy(source); by={int(x['stage']):x for x in doc['recipes']}; order=ORDERS[order_key]
    for stage in (49,50):
        by[stage]['spawns']=build_stage(order[stage],gap_ms)
        by[stage]['formation']='F08' if stage==49 else 'F01'
        by[stage]['formationSet']=['F01','F02','F03','F08']
        by[stage]['cadence']='CD05'
        by[stage]['pressureTags']=['BASELINE','FLOOD','RUSH','BULWARK']
    doc['version']=f"{source['version']}+{cid}"
    doc['status']='EPHEMERAL_STAGE49_50_DISTINCT_GRAMMAR_CADENCE_NOT_AUTHORING'
    return doc


def execute_with_ledger(runtime,by,cls,seed):
    run=r.new_run(runtime,cls,seed,31,ACTIVE); blocks=[]; continuity=[]; prev=None
    for stage in [46,47,48,49,50]:
        run['activeMilestones']=list(ACTIVE); run['level']=31; before=len(run['ledger'])
        result=r.simulate_stage(run,by[stage],runtime); ledger=run['ledger'][before:]
        if prev is not None:
            for key in ('baseHp','baseMaxHp','wallDeficit','combo','charge','judgmentRng','combatProcRng'):
                if result['entryState'][key]!=prev[key]: continuity.append(f'{cls}/{seed}/stage{stage}:{key}')
        prev=result['exitState']; blocks.append({'result':result,'ledger':ledger})
        if run['status']=='FAILED': break
    return {'blocks':blocks,'continuityErrors':continuity,'status':run['status'],'baseHp':run['baseHp']}


def phase_for_ms(at_ms:int,gap_ms:int,names:list[str]):
    return names[min(max(0,int(at_ms)//gap_ms),len(names)-1)]


def target_type(recipe:dict,target_id:str):
    try:
        idx=int(str(target_id).rsplit('_',1)[1])-1
        return recipe['spawns'][idx]['type']
    except Exception:
        return 'UNKNOWN'


def attr(block,recipe,gap_ms,names):
    out={name:{'rootActions':0,'lv31FinalRoots':0,'lv31Damage':0.0,'lv31Hits':0,'lv31BruteDamage':0.0,'lv31Knock':0.0} for name in names}
    for a in block['result']['actionTrace']:
        name=phase_for_ms(a['atMs'],gap_ms,names); out[name]['rootActions']+=1
        if a.get('lv31Final'): out[name]['lv31FinalRoots']+=1
    for e in block['ledger']:
        name=phase_for_ms(e['atMs'],gap_ms,names)
        if str(e['effectId']).startswith('LV31_'):
            dmg=float(e['finalDamage']); out[name]['lv31Damage']+=dmg; out[name]['lv31Hits']+=1; out[name]['lv31Knock']+=float(e.get('knockDistance',0))
            if target_type(recipe,e['targetId'])=='BRUTE': out[name]['lv31BruteDamage']+=dmg
    for v in out.values():
        roots=v['lv31FinalRoots']
        for k in ('lv31Damage','lv31BruteDamage','lv31Knock'): v[k]=round(v[k],6)
        v['damagePerFinal']=None if roots==0 else round(v['lv31Damage']/roots,6)
        v['hitsPerFinal']=None if roots==0 else round(v['lv31Hits']/roots,6)
        v['bruteDamagePerFinal']=None if roots==0 else round(v['lv31BruteDamage']/roots,6)
        v['knockPerFinal']=None if roots==0 else round(v['lv31Knock']/roots,6)
    return out


def execute(doc,p3,p4,temporal,seeds,order_key,gap_ms):
    overall=widthbridge.with_archer_final_width(WIDTH,lambda:shape.execute_candidate(doc,p3,p4,temporal,seeds))
    runtime=r.build_runtime(doc,p3,p4,temporal); by={int(x['stage']):x for x in doc['recipes']}; rows=[]; fidelity=[]
    order=ORDERS[order_key]
    for cls in r.CLASSES:
        for seed in seeds:
            case=widthbridge.with_archer_final_width(WIDTH,lambda cls=cls,seed=seed:execute_with_ledger(runtime,by,cls,seed))
            fidelity.extend(case['continuityErrors'])
            stages={}
            for block in case['blocks']:
                stage=block['result']['stage']
                if stage in (49,50): stages[str(stage)]=attr(block,by[stage],gap_ms,order[stage])
            rows.append({'class':cls,'seed':seed,'phaseAttribution':stages})
    aggregate={}
    for cls in r.CLASSES:
        aggregate[cls]={}; crows=[x for x in rows if x['class']==cls]
        for stage in (49,50):
            aggregate[cls][str(stage)]={}
            for name in order[stage]:
                vals=[x['phaseAttribution'][str(stage)][name] for x in crows]
                roots=sum(v['lv31FinalRoots'] for v in vals); dmg=sum(v['lv31Damage'] for v in vals); hits=sum(v['lv31Hits'] for v in vals); brute=sum(v['lv31BruteDamage'] for v in vals); knock=sum(v['lv31Knock'] for v in vals)
                aggregate[cls][str(stage)][name]={'lv31FinalRoots':roots,'lv31Damage':round(dmg,6),'lv31Hits':hits,'lv31BruteDamage':round(brute,6),'lv31Knock':round(knock,6),'damagePerFinal':None if roots==0 else round(dmg/roots,6),'hitsPerFinal':None if roots==0 else round(hits/roots,6),'bruteDamagePerFinal':None if roots==0 else round(brute/roots,6),'knockPerFinal':None if roots==0 else round(knock/roots,6)}
    return {'overall':overall,'phaseFidelityErrors':fidelity,'phaseAggregate':aggregate,'phaseRows':rows}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--recipes',required=True); ap.add_argument('--p3',default='legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json'); ap.add_argument('--p4d2-base',default='legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json'); ap.add_argument('--p4d2-temporal',default='legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json'); ap.add_argument('--seeds',default='101,211,307,409,503'); ap.add_argument('--json-out',required=True); args=ap.parse_args()
    source=r.load_yaml(args.recipes); p3=r.load_json(args.p3); p4=r.load_json(args.p4d2_base); temporal=r.load_json(args.p4d2_temporal); seeds=tuple(int(x) for x in args.seeds.split(',') if x.strip()); source_by={int(x['stage']):x for x in source['recipes']}
    # 4.5/5.0s were statically rejected because Stage50 reprise overlap produced max4=9-10.
    # 5.5s is the minimum calculated legal phase gap for this exact template family.
    specs=[('CAD_A_G5500','ORDER_A',5500),('CAD_A_G6000','ORDER_A',6000),('CAD_B_G5500','ORDER_B',5500),('CAD_B_G6000','ORDER_B',6000)]
    candidates=[]; rejected=[]; fidelity=[]
    for cid,order,gap in specs:
        doc=candidate(source,cid,order,gap); by={int(x['stage']):x for x in doc['recipes']}; errors=r.static_recipe_gate(doc)
        for stage in source_by:
            if stage not in (49,50) and by[stage]!=source_by[stage]: errors.append(f'scope-change-stage{stage}')
        static={str(s):shape.stage_static(by[s]) for s in (49,50)}
        if any(v['max4s']>8 for v in static.values()): errors.append('AUTHORED_4S_DENSITY_EXCEEDS_NORMAL_CAP')
        if errors: rejected.append({'id':cid,'staticErrors':errors,'stageStatic':static}); continue
        dyn=execute(doc,p3,p4,temporal,seeds,order,gap)
        errs=[f'{cid}:overall:{e}' for e in dyn['overall']['fidelityErrors']]+[f'{cid}:phase:{e}' for e in dyn['phaseFidelityErrors']]; fidelity.extend(errs)
        candidates.append({'id':cid,'order':order,'gapMs':gap,'archerDiagnosticWidth':WIDTH,'stageStatic':static,**dyn})
    out={'version':'t1-stage49-50-distinct-grammar-cadence-probe-v0.1','status':'DIAGNOSTIC_SEARCH_NO_AUTHORING_ADOPTION','sourceRecipe':str(args.recipes),'sourceRecipeSha256':r.sha256_bytes(Path(args.recipes).read_bytes()),'archerWidthBridge':{'yTolerance':WIDTH,'status':'DIAGNOSTIC_ONLY'},'grammarTemplates':GRAMMARS,'orders':ORDERS,'seeds':list(seeds),'fidelityErrors':fidelity,'candidates':candidates,'rejected':rejected}
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('id offDamage onDamage offWall onWall offFail onFail')
    for c in candidates:
        o=c['overall']; print(c['id'],o['OFF']['totalWallDamage'],o['ON']['totalWallDamage'],o['OFF']['wallPositiveCases'],o['ON']['wallPositiveCases'],o['OFF']['failOrIncompleteCases'],o['ON']['failOrIncompleteCases'])
        print(' ON_SEC',json.dumps({k:v['meanLateSettledSeconds'] for k,v in o['ON']['byClass'].items()},sort_keys=True))
        for cls in r.CLASSES:
            print(' ',cls,'S49',json.dumps(c['phaseAggregate'][cls]['49'],sort_keys=True))
            print(' ',cls,'S50',json.dumps(c['phaseAggregate'][cls]['50'],sort_keys=True))
    if fidelity: raise SystemExit('DISTINCT_GRAMMAR_CADENCE_FIDELITY_FAIL')
if __name__=='__main__': main()
