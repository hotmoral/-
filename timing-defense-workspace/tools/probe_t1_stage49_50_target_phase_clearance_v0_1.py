#!/usr/bin/env python3
"""Target-phase clearance attribution for T1 Stage49-50 distinct grammar v0.1.

Measures the full class package against the authored grammar that spawned each target,
not just Lv31 final damage. For every Stage49/50 phase and class/seed it records:
- authored targets;
- targets killed by player/effects, reconstructed from cumulative finalDamage vs target HP;
- targets that resolve by wall contact (authored minus reconstructed player kills at settled boundary);
- target-phase total / Lv31 damage;
- time from phase start until its last player-killed target.

The core damage ledger intentionally stores damage facts rather than a duplicated kill flag,
so this probe reconstructs target death from cumulative ledger damage and immutable monster HP.

The probe compares Lv31 OFF vs ON using identical deterministic lifecycle conditions.
Diagnostic only; no recipe or scalar adoption.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import probe_t1_stage49_50_distinct_grammar_cadence_v0_1 as distinct
import probe_t1_archer_lv31_continuous_corridor_bridge_v0_1 as widthbridge

r=distinct.r
WIDTH=0.20
OFF=[6,11,16,21,26]
ON=[6,11,16,21,26,31]


def phase_target_map(recipe:dict,gap_ms:int,names:list[str]):
    mapping={}
    starts={name:i*gap_ms for i,name in enumerate(names)}
    expected={name:[] for name in names}
    for idx,spawn in enumerate(recipe['spawns'],start=1):
        name=distinct.phase_for_ms(int(spawn['tMs']),gap_ms,names)
        mid=f"S{int(recipe['stage'])}_{idx}"
        mapping[mid]={'phase':name,'type':spawn['type'],'spawnMs':int(spawn['tMs'])}
        expected[name].append(mid)
    return mapping,expected,starts


def execute_with_ledger(runtime,by,cls,seed,active):
    level=31 if 31 in active else max(active)
    run=r.new_run(runtime,cls,seed,level,active)
    blocks=[]; continuity=[]; prev=None
    for stage in [46,47,48,49,50]:
        run['activeMilestones']=list(active); run['level']=level; before=len(run['ledger'])
        result=r.simulate_stage(run,by[stage],runtime); ledger=run['ledger'][before:]
        if prev is not None:
            for key in ('baseHp','baseMaxHp','wallDeficit','combo','charge','judgmentRng','combatProcRng'):
                if result['entryState'][key]!=prev[key]: continuity.append(f'{cls}/{seed}/stage{stage}:{key}')
        prev=result['exitState']; blocks.append({'result':result,'ledger':ledger})
        if run['status']=='FAILED': break
    return {'blocks':blocks,'continuityErrors':continuity,'status':run['status'],'baseHp':run['baseHp']}


def attribute_targets(block,recipe,gap_ms,names,runtime):
    mapping,expected,starts=phase_target_map(recipe,gap_ms,names)
    phases={name:{'authored':len(expected[name]),'killedIds':set(),'totalDamage':0.0,'lv31Damage':0.0,'hitEvents':0,'lv31HitEvents':0,'lastKillMs':None} for name in names}
    cumulative={tid:0.0 for tid in mapping}
    for e in block['ledger']:
        tid=e['targetId']
        meta=mapping.get(tid)
        if not meta:
            continue
        p=phases[meta['phase']]
        dmg=float(e['finalDamage']); p['totalDamage']+=dmg; p['hitEvents']+=1
        cumulative[tid]+=dmg
        if str(e['effectId']).startswith('LV31_'):
            p['lv31Damage']+=dmg; p['lv31HitEvents']+=1
        target_hp=float(runtime['monsters'][meta['type']]['hp'])
        if tid not in p['killedIds'] and cumulative[tid] >= target_hp - 1e-9:
            p['killedIds'].add(tid)
            t=int(e['atMs'])
            p['lastKillMs']=t if p['lastKillMs'] is None else max(p['lastKillMs'],t)
    out={}
    for name,p in phases.items():
        killed=len(p['killedIds']); escapes=p['authored']-killed
        out[name]={
            'authored':p['authored'],
            'playerKilled':killed,
            'wallResolvedOrUnkilled':escapes,
            'allPlayerKilled':escapes==0,
            'totalDamage':round(p['totalDamage'],6),
            'lv31Damage':round(p['lv31Damage'],6),
            'hitEvents':p['hitEvents'],
            'lv31HitEvents':p['lv31HitEvents'],
            'lastPlayerKillMs':p['lastKillMs'],
            'clearLatencyFromPhaseStartMs':None if p['lastKillMs'] is None or escapes else int(p['lastKillMs']-starts[name]),
        }
    return out


def run_side(runtime,by,cls,seed,active,gap_ms,order):
    case=widthbridge.with_archer_final_width(WIDTH,lambda:execute_with_ledger(runtime,by,cls,seed,active))
    stages={}
    for block in case['blocks']:
        stage=block['result']['stage']
        if stage in (49,50): stages[str(stage)]=attribute_targets(block,by[stage],gap_ms,order[stage],runtime)
    return {'continuityErrors':case['continuityErrors'],'status':case['status'],'baseHp':case['baseHp'],'stages':stages}


def aggregate(rows,order):
    out={}
    for cls in r.CLASSES:
        out[cls]={}; crows=[x for x in rows if x['class']==cls]
        for side in ('OFF','ON'):
            out[cls][side]={}
            for stage in (49,50):
                out[cls][side][str(stage)]={}
                for name in order[stage]:
                    vals=[x[side]['stages'][str(stage)][name] for x in crows]
                    complete=[v['clearLatencyFromPhaseStartMs'] for v in vals if v['clearLatencyFromPhaseStartMs'] is not None]
                    out[cls][side][str(stage)][name]={
                        'cases':len(vals),
                        'authoredTargets':sum(v['authored'] for v in vals),
                        'playerKilled':sum(v['playerKilled'] for v in vals),
                        'wallResolvedOrUnkilled':sum(v['wallResolvedOrUnkilled'] for v in vals),
                        'allPlayerKilledCases':sum(1 for v in vals if v['allPlayerKilled']),
                        'meanClearLatencyMs':None if not complete else round(sum(complete)/len(complete),3),
                        'totalDamage':round(sum(v['totalDamage'] for v in vals),6),
                        'lv31Damage':round(sum(v['lv31Damage'] for v in vals),6),
                    }
    return out


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
    specs=[('CAD_A_G5500','ORDER_A',5500),('CAD_B_G5500','ORDER_B',5500)]
    candidates={}; fidelity=[]
    for cid,order_key,gap in specs:
        doc=distinct.candidate(source,cid,order_key,gap); runtime=r.build_runtime(doc,p3,p4,temporal); by={int(x['stage']):x for x in doc['recipes']}; order=distinct.ORDERS[order_key]
        rows=[]
        for cls in r.CLASSES:
            for seed in seeds:
                off1=run_side(runtime,by,cls,seed,OFF,gap,order); off2=run_side(runtime,by,cls,seed,OFF,gap,order)
                on1=run_side(runtime,by,cls,seed,ON,gap,order); on2=run_side(runtime,by,cls,seed,ON,gap,order)
                if r.sha256_obj(off1)!=r.sha256_obj(off2): fidelity.append(f'{cid}/OFF/determinism/{cls}/{seed}')
                if r.sha256_obj(on1)!=r.sha256_obj(on2): fidelity.append(f'{cid}/ON/determinism/{cls}/{seed}')
                fidelity.extend(f'{cid}/OFF/{e}' for e in off1['continuityErrors']); fidelity.extend(f'{cid}/ON/{e}' for e in on1['continuityErrors'])
                rows.append({'class':cls,'seed':seed,'OFF':off1,'ON':on1})
        agg=aggregate(rows,order)
        total_killed=sum(v['playerKilled'] for cls in agg.values() for side in cls.values() for stage in side.values() for v in stage.values())
        if total_killed <= 0:
            fidelity.append(f'{cid}/NO_RECONSTRUCTED_PLAYER_KILLS')
        candidates[cid]={'recipeVersion':doc['version'],'order':order_key,'gapMs':gap,'aggregate':agg,'rows':rows,'reconstructedPlayerKills':total_killed}

    out={'version':'t1-stage49-50-target-phase-clearance-v0.1','status':'DIAGNOSTIC_FULL_PACKAGE_PHASE_ATTRIBUTION_NO_AUTHORING_ADOPTION','sourceRecipe':str(args.recipes),'sourceRecipeSha256':r.sha256_bytes(Path(args.recipes).read_bytes()),'killReconstructionRule':'cumulative ledger.finalDamage by targetId >= immutable target HP','archerWidthBridge':{'yTolerance':WIDTH,'status':'DIAGNOSTIC_ONLY'},'seeds':list(seeds),'fidelityErrors':fidelity,'candidates':candidates}
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')

    for cid,c in candidates.items():
        print('\n',cid,'reconstructedKills',c['reconstructedPlayerKills'])
        a=c['aggregate']
        for cls in r.CLASSES:
            print(' ',cls)
            for side in ('OFF','ON'):
                compact={}
                for stage in ('49','50'):
                    compact['S'+stage]={name:{'K':v['playerKilled'],'W':v['wallResolvedOrUnkilled'],'C':v['allPlayerKilledCases'],'ms':v['meanClearLatencyMs']} for name,v in a[cls][side][stage].items()}
                print('  ',side,json.dumps(compact,sort_keys=True))
    if fidelity:
        raise SystemExit('TARGET_PHASE_CLEARANCE_FIDELITY_FAIL')

if __name__=='__main__':
    main()
