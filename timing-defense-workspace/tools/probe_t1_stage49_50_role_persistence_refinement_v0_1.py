#!/usr/bin/env python3
"""T1 Stage49-50 role-persistence refinement probe v0.1.

Refines only the surviving ROT5_G3500 rotating-grammar direction after phase attribution:
- Stage49 LINE was landing in a low-Lv31-opportunity time window;
- LINE/CLUSTER light bodies were often gone before Lv31 finals arrived.

Refinement:
1) Stage49 phase order becomes DURABLE_SCATTER -> FRONTLINE -> LINE -> CLUSTER,
   moving LINE into the observed later final-opportunity window.
2) Body counts/timing remain unchanged; one light body in LINE and one in CLUSTER are
   replaced by BRUTE so aligned/clustered pressure persists long enough to be read.
3) Stage50 keeps LINE -> CLUSTER -> FRONTLINE -> DURABLE_SCATTER -> LINE reprise.
4) Archer uses diagnostic continuous bridge yTol=0.20 only; no width freeze.

No scalar, body-count, Stage46-48, shop, EXP, or production change.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import probe_t1_stage49_50_class_rotation_shape_v0_1 as shape
import probe_t1_stage49_50_rotating_grammar_v0_1 as rotating
import probe_t1_stage49_50_rotating_grammar_phase_attribution_v0_1 as phaseprobe
import probe_t1_archer_lv31_continuous_corridor_bridge_v0_1 as widthbridge

r=shape.r
WIDTH=0.20
GAP=3500

REFINED_PHASES={
 'LINE':[('BRUTE',0.46),('RUNNER',0.48),('BRUTE',0.50),('GRUNT',0.44),('RUNNER',0.52),('BRUTE',0.46)],
 'CLUSTER':[('GRUNT',0.42),('BRUTE',0.46),('GRUNT',0.50),('RUNNER',0.44),('BRUTE',0.48),('GRUNT',0.43)],
 'FRONTLINE':rotating.PHASES['FRONTLINE'],
 'DURABLE_SCATTER':rotating.PHASES['DURABLE_SCATTER'],
}


def build(rows_names):
    offsets=[0,400,800,1200,1600,2000]; rows=[]
    for i,name in enumerate(rows_names):
        base=i*GAP
        for off,(typ,y) in zip(offsets,REFINED_PHASES[name]):
            rows.append({'tMs':base+off,'type':typ,'y':y})
    return rows


def refined_candidate(source):
    doc=copy.deepcopy(source); by={int(x['stage']):x for x in doc['recipes']}
    orders={49:['DURABLE_SCATTER','FRONTLINE','LINE','CLUSTER'],50:['LINE','CLUSTER','FRONTLINE','DURABLE_SCATTER','LINE']}
    for stage,names in orders.items():
        by[stage]['spawns']=build(names)
        by[stage]['formation']='F08' if stage==49 else 'F01'
        by[stage]['formationSet']=['F01','F02','F03','F08']
        by[stage]['cadence']='CD05'
        by[stage]['pressureTags']=['BASELINE','FLOOD','RUSH','BULWARK']
    doc['version']=f"{source['version']}+ROT5_ROLE_PERSIST_G3500"
    doc['status']='EPHEMERAL_STAGE49_50_ROLE_PERSISTENCE_REFINEMENT_NOT_AUTHORING'
    return doc


def overall(doc,p3,p4,temporal,seeds):
    return widthbridge.with_archer_final_width(WIDTH,lambda:shape.execute_candidate(doc,p3,p4,temporal,seeds))


def phase_attr(doc,p3,p4,temporal,seeds,orders):
    runtime=r.build_runtime(doc,p3,p4,temporal); by={int(x['stage']):x for x in doc['recipes']}; rows=[]; fidelity=[]
    for cls in r.CLASSES:
        for seed in seeds:
            case=widthbridge.with_archer_final_width(WIDTH,lambda cls=cls,seed=seed:phaseprobe.execute_with_ledger(runtime,by,cls,seed))
            if case['continuityErrors']: fidelity.extend(case['continuityErrors'])
            attrs={}
            for block in case['stages']:
                stage=block['result']['stage']
                if stage in (49,50): attrs[str(stage)]=phaseprobe.attribute_stage(block,by[stage],GAP,orders[stage])
            rows.append({'class':cls,'seed':seed,'phaseAttribution':attrs})
    aggregate={}
    for cls in r.CLASSES:
        aggregate[cls]={}
        crows=[x for x in rows if x['class']==cls]
        for stage in (49,50):
            aggregate[cls][str(stage)]={}
            for name in orders[stage]:
                # LINE occurs twice in Stage50; phaseprobe dict collapses same name. Use LINE_REPRISE externally.
                if stage==50 and name=='LINE' and name in aggregate[cls][str(stage)]: continue
                vals=[x['phaseAttribution'][str(stage)][name] for x in crows]
                roots=sum(v['lv31FinalRoots'] for v in vals); dmg=sum(v['lv31Damage'] for v in vals); hits=sum(v['lv31Hits'] for v in vals); brute=sum(v['lv31BruteDamage'] for v in vals); knock=sum(v['lv31KnockDistance'] for v in vals)
                aggregate[cls][str(stage)][name]={'lv31FinalRoots':roots,'lv31Damage':round(dmg,6),'lv31Hits':hits,'lv31BruteDamage':round(brute,6),'lv31KnockDistance':round(knock,6),'damagePerFinal':None if roots==0 else round(dmg/roots,6),'hitsPerFinal':None if roots==0 else round(hits/roots,6),'bruteDamagePerFinal':None if roots==0 else round(brute/roots,6)}
    return {'fidelityErrors':fidelity,'aggregate':aggregate,'rows':rows}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--recipes',required=True); ap.add_argument('--p3',default='legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json'); ap.add_argument('--p4d2-base',default='legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json'); ap.add_argument('--p4d2-temporal',default='legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json'); ap.add_argument('--seeds',default='101,211,307,409,503'); ap.add_argument('--json-out',required=True); args=ap.parse_args()
    source=r.load_yaml(args.recipes); p3=r.load_json(args.p3); p4=r.load_json(args.p4d2_base); temporal=r.load_json(args.p4d2_temporal); seeds=tuple(int(x) for x in args.seeds.split(',') if x.strip())
    control=rotating.candidate(source,'ROT5_G3500',3500,True,False); refined=refined_candidate(source)
    orders_control={49:['DURABLE_SCATTER','LINE','FRONTLINE','CLUSTER'],50:['LINE','CLUSTER','FRONTLINE','DURABLE_SCATTER','LINE_REPRISE']}
    orders_refined={49:['DURABLE_SCATTER','FRONTLINE','LINE','CLUSTER'],50:['LINE','CLUSTER','FRONTLINE','DURABLE_SCATTER','LINE_REPRISE']}
    # Convert the repeated final LINE in refined Stage50 to a unique attribution label without changing recipe bytes.
    # phaseprobe classification uses names only; provide LINE_REPRISE for the final time window.
    refined_orders_for_attr=orders_refined
    candidates={}
    for cid,doc,orders in [('CONTROL_ROT5_G3500',control,orders_control),('REFINED_ROLE_PERSIST',refined,refined_orders_for_attr)]:
        errors=r.static_recipe_gate(doc); by={int(x['stage']):x for x in doc['recipes']}; static={str(s):shape.stage_static(by[s]) for s in (49,50)}
        if any(v['max4s']>8 for v in static.values()): errors.append('AUTHORED_4S_DENSITY_EXCEEDS_NORMAL_CAP')
        if errors: raise SystemExit(f'{cid}:STATIC_FAIL:{errors}')
        ov=overall(doc,p3,p4,temporal,seeds)
        pa=phase_attr(doc,p3,p4,temporal,seeds,orders)
        candidates[cid]={'recipeVersion':doc['version'],'stageStatic':static,'overall':ov,'phase':pa}
    fidelity=[f'{cid}:overall:{e}' for cid,c in candidates.items() for e in c['overall']['fidelityErrors']] + [f'{cid}:phase:{e}' for cid,c in candidates.items() for e in c['phase']['fidelityErrors']]
    out={'version':'t1-stage49-50-role-persistence-refinement-probe-v0.1','status':'DIAGNOSTIC_REFINEMENT_NO_AUTHORING_ADOPTION','sourceRecipe':str(args.recipes),'sourceRecipeSha256':r.sha256_bytes(Path(args.recipes).read_bytes()),'archerWidthBridge':{'yTolerance':WIDTH,'status':'DIAGNOSTIC_ONLY'},'gapMs':GAP,'seeds':list(seeds),'fidelityErrors':fidelity,'candidates':candidates}
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    for cid,c in candidates.items():
        o=c['overall']; print('\n',cid,'OFF',o['OFF']['totalWallDamage'],o['OFF']['wallPositiveCases'],'ON',o['ON']['totalWallDamage'],o['ON']['wallPositiveCases'])
        print(' OFF_SEC',json.dumps({k:v['meanLateSettledSeconds'] for k,v in o['OFF']['byClass'].items()},sort_keys=True)); print(' ON_SEC ',json.dumps({k:v['meanLateSettledSeconds'] for k,v in o['ON']['byClass'].items()},sort_keys=True))
        for cls in r.CLASSES:
            print(' ',cls,'S49',json.dumps(c['phase']['aggregate'][cls]['49'],sort_keys=True))
            print(' ',cls,'S50',json.dumps(c['phase']['aggregate'][cls]['50'],sort_keys=True))
    if fidelity: raise SystemExit('ROLE_PERSISTENCE_REFINEMENT_FIDELITY_FAIL')
if __name__=='__main__': main()
