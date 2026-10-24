#!/usr/bin/env python3
"""T1 Stage49-50 rotating grammar phase-attribution probe v0.1.

Validates whether the two surviving rotating-grammar candidates create actual class-role
windows rather than merely carrying grammar labels. Diagnostic only.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import probe_t1_stage49_50_rotating_grammar_v0_1 as rotating
import probe_t1_archer_lv31_continuous_corridor_bridge_v0_1 as widthbridge

r = rotating.r
WIDTH = 0.20
ACTIVE = [6,11,16,21,26,31]


def phase_names(stage:int,reprise:bool):
    if stage==49:
        return ['DURABLE_SCATTER','LINE','FRONTLINE','CLUSTER']
    names=['LINE','CLUSTER','FRONTLINE','DURABLE_SCATTER']
    if reprise: names.append('LINE_REPRISE')
    return names


def phase_for_ms(at_ms:int,gap_ms:int,names:list[str]):
    idx=min(max(0,int(at_ms)//gap_ms),len(names)-1)
    return names[idx]


def target_type_from_id(recipe:dict,target_id:str):
    try:
        idx=int(str(target_id).rsplit('_',1)[1])-1
        return recipe['spawns'][idx]['type']
    except Exception:
        return 'UNKNOWN'


def execute_with_ledger(runtime,by_stage,cls,seed):
    run=r.new_run(runtime,cls,seed,31,ACTIVE)
    out=[]
    prev=None
    continuity=[]
    for stage in [46,47,48,49,50]:
        run['activeMilestones']=list(ACTIVE); run['level']=31
        before=len(run['ledger'])
        result=r.simulate_stage(run,by_stage[stage],runtime)
        ledger=run['ledger'][before:]
        if prev is not None:
            for key in ('baseHp','baseMaxHp','wallDeficit','combo','charge','judgmentRng','combatProcRng'):
                if result['entryState'][key] != prev[key]:
                    continuity.append(f'{cls}/{seed}/stage{stage}:{key}')
        prev=result['exitState']
        out.append({'result':result,'ledger':ledger})
        if run['status']=='FAILED': break
    return {'class':cls,'seed':seed,'stages':out,'continuityErrors':continuity,'finalStatus':run['status'],'finalBaseHp':run['baseHp']}


def attribute_stage(stage_block,recipe,gap_ms,names):
    result=stage_block['result']; ledger=stage_block['ledger']
    phases={name:{'rootActions':0,'lv31FinalRoots':0,'totalDamage':0.0,'lv31Damage':0.0,'lv31Hits':0,'lv31BruteDamage':0.0,'lv31KnockDistance':0.0} for name in names}
    for a in result['actionTrace']:
        phase=phase_for_ms(int(a['atMs']),gap_ms,names)
        phases[phase]['rootActions'] += 1
        if a.get('lv31Final'):
            phases[phase]['lv31FinalRoots'] += 1
    for e in ledger:
        phase=phase_for_ms(int(e['atMs']),gap_ms,names)
        dmg=float(e['finalDamage']); phases[phase]['totalDamage'] += dmg
        if str(e['effectId']).startswith('LV31_'):
            phases[phase]['lv31Damage'] += dmg
            phases[phase]['lv31Hits'] += 1
            phases[phase]['lv31KnockDistance'] += float(e.get('knockDistance',0.0))
            if target_type_from_id(recipe,e['targetId'])=='BRUTE':
                phases[phase]['lv31BruteDamage'] += dmg
    for row in phases.values():
        for k in ('totalDamage','lv31Damage','lv31BruteDamage','lv31KnockDistance'):
            row[k]=round(row[k],6)
        row['lv31DamagePerFinal']=None if row['lv31FinalRoots']==0 else round(row['lv31Damage']/row['lv31FinalRoots'],6)
        row['lv31HitsPerFinal']=None if row['lv31FinalRoots']==0 else round(row['lv31Hits']/row['lv31FinalRoots'],6)
    return phases


def run_candidate(source,p3,p4,temporal,cid,gap,reprise,seeds):
    doc=rotating.candidate(source,cid,gap,reprise,False)
    runtime=r.build_runtime(doc,p3,p4,temporal); by={int(x['stage']):x for x in doc['recipes']}
    rows=[]; fidelity=[]
    for cls in r.CLASSES:
        for seed in seeds:
            case=widthbridge.with_archer_final_width(WIDTH,lambda cls=cls,seed=seed: execute_with_ledger(runtime,by,cls,seed))
            if case['continuityErrors']: fidelity.extend(case['continuityErrors'])
            stage_attr={}
            for block in case['stages']:
                stage=block['result']['stage']
                if stage in (49,50):
                    names=phase_names(stage,reprise)
                    stage_attr[str(stage)]=attribute_stage(block,by[stage],gap,names)
            rows.append({'class':cls,'seed':seed,'finalStatus':case['finalStatus'],'finalBaseHp':case['finalBaseHp'],'phaseAttribution':stage_attr})

    aggregate={}
    for cls in r.CLASSES:
        aggregate[cls]={}
        crows=[x for x in rows if x['class']==cls]
        for stage in (49,50):
            names=phase_names(stage,reprise)
            aggregate[cls][str(stage)]={}
            for name in names:
                vals=[x['phaseAttribution'][str(stage)][name] for x in crows if str(stage) in x['phaseAttribution']]
                roots=sum(v['lv31FinalRoots'] for v in vals); dmg=sum(v['lv31Damage'] for v in vals); hits=sum(v['lv31Hits'] for v in vals); brute=sum(v['lv31BruteDamage'] for v in vals); knock=sum(v['lv31KnockDistance'] for v in vals)
                aggregate[cls][str(stage)][name]={
                    'cases':len(vals),'lv31FinalRoots':roots,'lv31Damage':round(dmg,6),'lv31Hits':hits,'lv31BruteDamage':round(brute,6),'lv31KnockDistance':round(knock,6),
                    'damagePerFinal':None if roots==0 else round(dmg/roots,6),
                    'hitsPerFinal':None if roots==0 else round(hits/roots,6),
                    'bruteDamagePerFinal':None if roots==0 else round(brute/roots,6),
                    'knockPerFinal':None if roots==0 else round(knock/roots,6),
                }
    return {'recipeVersion':doc['version'],'fidelityErrors':fidelity,'aggregate':aggregate,'rows':rows}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--recipes',required=True)
    ap.add_argument('--p3',default='legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json'); ap.add_argument('--p4d2-base',default='legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json'); ap.add_argument('--p4d2-temporal',default='legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json')
    ap.add_argument('--seeds',default='101,211,307,409,503'); ap.add_argument('--json-out',required=True); args=ap.parse_args()
    source=r.load_yaml(args.recipes); p3=r.load_json(args.p3); p4=r.load_json(args.p4d2_base); temporal=r.load_json(args.p4d2_temporal); seeds=tuple(int(x) for x in args.seeds.split(',') if x.strip())
    candidates={
      'ROT4_G3500':run_candidate(source,p3,p4,temporal,'ROT4_G3500',3500,False,seeds),
      'ROT5_G3500':run_candidate(source,p3,p4,temporal,'ROT5_G3500',3500,True,seeds),
    }
    fidelity=[f'{cid}:{e}' for cid,c in candidates.items() for e in c['fidelityErrors']]
    out={'version':'t1-stage49-50-rotating-grammar-phase-attribution-v0.1','status':'DIAGNOSTIC_ROLE_ATTRIBUTION_NO_AUTHORING_ADOPTION','sourceRecipe':str(args.recipes),'sourceRecipeSha256':r.sha256_bytes(Path(args.recipes).read_bytes()),'archerWidthBridge':{'yTolerance':WIDTH,'status':'DIAGNOSTIC_ONLY'},'seeds':list(seeds),'fidelityErrors':fidelity,'candidates':candidates}
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    for cid,c in candidates.items():
        print('\n',cid)
        for cls in r.CLASSES:
            print(' ',cls)
            for stage in ('49','50'):
                compact={name:{'F':v['lv31FinalRoots'],'D/F':v['damagePerFinal'],'H/F':v['hitsPerFinal'],'B/F':v['bruteDamagePerFinal'],'K/F':v['knockPerFinal']} for name,v in c['aggregate'][cls][stage].items()}
                print('   S'+stage,json.dumps(compact,sort_keys=True))
    if fidelity: raise SystemExit('ROTATING_GRAMMAR_PHASE_ATTRIBUTION_FIDELITY_FAIL')
if __name__=='__main__': main()
