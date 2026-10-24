#!/usr/bin/env python3
"""Parent-root phase attribution for T1 Stage49-50 distinct grammar v0.1.

Corrects a diagnostic attribution bug: delayed Lv31 effects (Mage staged blasts,
Rogue daggers, Knight second wave) must be attributed to the phase of the root timing
action that created them, not the later timestamp when the delayed hit lands.

This probe reuses the already-admitted distinct-grammar candidates unchanged and
recomputes phase attribution via ledger.parentActionId -> actionTrace.action.
No gameplay or candidate recipe semantics are changed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import probe_t1_stage49_50_distinct_grammar_cadence_v0_1 as distinct
import probe_t1_stage49_50_class_rotation_shape_v0_1 as shape
import probe_t1_archer_lv31_continuous_corridor_bridge_v0_1 as widthbridge

r=distinct.r
WIDTH=distinct.WIDTH
ACTIVE=distinct.ACTIVE


def attr_parent(block, recipe, gap_ms, names):
    out={name:{'rootActions':0,'lv31FinalRoots':0,'lv31Damage':0.0,'lv31Hits':0,'lv31BruteDamage':0.0,'lv31Knock':0.0} for name in names}
    action_phase={}
    for a in block['result']['actionTrace']:
        name=distinct.phase_for_ms(a['atMs'],gap_ms,names)
        action_phase[int(a['action'])]=name
        out[name]['rootActions']+=1
        if a.get('lv31Final'):
            out[name]['lv31FinalRoots']+=1

    for e in block['ledger']:
        if not str(e['effectId']).startswith('LV31_'):
            continue
        parent=e.get('parentActionId')
        if parent is None or int(parent) not in action_phase:
            raise RuntimeError(f"UNATTRIBUTED_LV31_EFFECT:{e}")
        name=action_phase[int(parent)]
        dmg=float(e['finalDamage'])
        out[name]['lv31Damage']+=dmg
        out[name]['lv31Hits']+=1
        out[name]['lv31Knock']+=float(e.get('knockDistance',0))
        if distinct.target_type(recipe,e['targetId'])=='BRUTE':
            out[name]['lv31BruteDamage']+=dmg

    for v in out.values():
        roots=v['lv31FinalRoots']
        for k in ('lv31Damage','lv31BruteDamage','lv31Knock'):
            v[k]=round(v[k],6)
        v['damagePerFinal']=None if roots==0 else round(v['lv31Damage']/roots,6)
        v['hitsPerFinal']=None if roots==0 else round(v['lv31Hits']/roots,6)
        v['bruteDamagePerFinal']=None if roots==0 else round(v['lv31BruteDamage']/roots,6)
        v['knockPerFinal']=None if roots==0 else round(v['lv31Knock']/roots,6)
    return out


def execute(doc,p3,p4,temporal,seeds,order_key,gap_ms):
    overall=widthbridge.with_archer_final_width(WIDTH,lambda:shape.execute_candidate(doc,p3,p4,temporal,seeds))
    runtime=r.build_runtime(doc,p3,p4,temporal)
    by={int(x['stage']):x for x in doc['recipes']}
    order=distinct.ORDERS[order_key]
    rows=[]; fidelity=[]
    for cls in r.CLASSES:
        for seed in seeds:
            case=widthbridge.with_archer_final_width(WIDTH,lambda cls=cls,seed=seed:distinct.execute_with_ledger(runtime,by,cls,seed))
            fidelity.extend(case['continuityErrors'])
            stages={}
            for block in case['blocks']:
                stage=block['result']['stage']
                if stage in (49,50):
                    stages[str(stage)]=attr_parent(block,by[stage],gap_ms,order[stage])
            rows.append({'class':cls,'seed':seed,'phaseAttribution':stages})

    aggregate={}
    for cls in r.CLASSES:
        aggregate[cls]={}; crows=[x for x in rows if x['class']==cls]
        for stage in (49,50):
            aggregate[cls][str(stage)]={}
            for name in order[stage]:
                vals=[x['phaseAttribution'][str(stage)][name] for x in crows]
                roots=sum(v['lv31FinalRoots'] for v in vals)
                dmg=sum(v['lv31Damage'] for v in vals)
                hits=sum(v['lv31Hits'] for v in vals)
                brute=sum(v['lv31BruteDamage'] for v in vals)
                knock=sum(v['lv31Knock'] for v in vals)
                aggregate[cls][str(stage)][name]={
                    'lv31FinalRoots':roots,
                    'lv31Damage':round(dmg,6),
                    'lv31Hits':hits,
                    'lv31BruteDamage':round(brute,6),
                    'lv31Knock':round(knock,6),
                    'damagePerFinal':None if roots==0 else round(dmg/roots,6),
                    'hitsPerFinal':None if roots==0 else round(hits/roots,6),
                    'bruteDamagePerFinal':None if roots==0 else round(brute/roots,6),
                    'knockPerFinal':None if roots==0 else round(knock/roots,6),
                }
    return {'overall':overall,'phaseFidelityErrors':fidelity,'phaseAggregate':aggregate,'phaseRows':rows}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--recipes',required=True)
    ap.add_argument('--p3',default='legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json')
    ap.add_argument('--p4d2-base',default='legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json')
    ap.add_argument('--p4d2-temporal',default='legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json')
    ap.add_argument('--seeds',default='101,211,307,409,503')
    ap.add_argument('--json-out',required=True)
    args=ap.parse_args()

    source=r.load_yaml(args.recipes); p3=r.load_json(args.p3); p4=r.load_json(args.p4d2_base); temporal=r.load_json(args.p4d2_temporal)
    seeds=tuple(int(x) for x in args.seeds.split(',') if x.strip())
    source_by={int(x['stage']):x for x in source['recipes']}
    specs=[('CAD_A_G5500','ORDER_A',5500),('CAD_A_G6000','ORDER_A',6000),('CAD_B_G5500','ORDER_B',5500),('CAD_B_G6000','ORDER_B',6000)]
    candidates=[]; rejected=[]; fidelity=[]
    for cid,order,gap in specs:
        doc=distinct.candidate(source,cid,order,gap)
        by={int(x['stage']):x for x in doc['recipes']}
        errors=r.static_recipe_gate(doc)
        for stage in source_by:
            if stage not in (49,50) and by[stage]!=source_by[stage]: errors.append(f'scope-change-stage{stage}')
        static={str(s):shape.stage_static(by[s]) for s in (49,50)}
        if any(v['max4s']>8 for v in static.values()): errors.append('AUTHORED_4S_DENSITY_EXCEEDS_NORMAL_CAP')
        if errors:
            rejected.append({'id':cid,'staticErrors':errors,'stageStatic':static}); continue
        dyn=execute(doc,p3,p4,temporal,seeds,order,gap)
        errs=[f'{cid}:overall:{e}' for e in dyn['overall']['fidelityErrors']]+[f'{cid}:phase:{e}' for e in dyn['phaseFidelityErrors']]
        fidelity.extend(errs)
        candidates.append({'id':cid,'order':order,'gapMs':gap,'archerDiagnosticWidth':WIDTH,'stageStatic':static,**dyn})

    out={
        'version':'t1-stage49-50-distinct-grammar-parent-attribution-v0.1',
        'status':'DIAGNOSTIC_PARENT_ROOT_ATTRIBUTION_NO_AUTHORING_ADOPTION',
        'sourceRecipe':str(args.recipes),
        'sourceRecipeSha256':r.sha256_bytes(Path(args.recipes).read_bytes()),
        'attributionRule':'LV31 effect -> ledger.parentActionId -> actionTrace.action root phase',
        'archerWidthBridge':{'yTolerance':WIDTH,'status':'DIAGNOSTIC_ONLY'},
        'grammarTemplates':distinct.GRAMMARS,
        'orders':distinct.ORDERS,
        'seeds':list(seeds),
        'fidelityErrors':fidelity,
        'candidates':candidates,
        'rejected':rejected,
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')

    for c in candidates:
        o=c['overall']
        print('\n',c['id'],'OFFwall',o['OFF']['totalWallDamage'],'ONwall',o['ON']['totalWallDamage'])
        for cls in r.CLASSES:
            print(' ',cls,'S49',json.dumps(c['phaseAggregate'][cls]['49'],sort_keys=True))
            print(' ',cls,'S50',json.dumps(c['phaseAggregate'][cls]['50'],sort_keys=True))
    if fidelity:
        raise SystemExit('DISTINCT_GRAMMAR_PARENT_ATTRIBUTION_FIDELITY_FAIL')

if __name__=='__main__':
    main()
