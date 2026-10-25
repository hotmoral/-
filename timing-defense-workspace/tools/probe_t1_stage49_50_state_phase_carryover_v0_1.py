#!/usr/bin/env python3
"""Targeted Stage49->50 persistent-state / P×P phase trace v0.1.

Compare transition-aware integration v0.1 vs v0.2 using the same
DURABLE_CORE_3 Stage50 CLUSTER morphology. This is attribution only:
no recipe adoption, no scalar change, no state reset.

Records Stage49 exit == Stage50 entry for combo/charge/RNG plus P×P root
locations. Mage is traced across all five seeds; Archer seed503 is traced OFF
and ON because v0.1 isolated its whole-window chronology reversal there.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import probe_t1_stage49_50_transition_aware_integration_v0_1 as v1
import probe_t1_stage49_50_transition_aware_integration_v0_2 as v2
import probe_t1_stage49_50_target_phase_clearance_v0_1 as target
import probe_t1_archer_lv31_continuous_corridor_bridge_v0_1 as widthbridge
import t1_transition_microsim_mage_lv31_fidelity_bridge_v0_1 as magebridge

r=v1.r
ACTIVE_OFF=v1.OFF
ACTIVE_ON=v1.ON
GAP=v1.GAP_MS


def build(source, version):
    if version=='V01':
        order=v1.ORDER
        doc=v1.build_candidate(source,'DURABLE_CORE_3')
    else:
        old=v1.ORDER
        try:
            v1.ORDER=v2.ORDER_V02
            order=v2.ORDER_V02
            doc=v1.build_candidate(source,'DURABLE_CORE_3')
        finally:
            v1.ORDER=old
    return doc,order


def phase_for(at_ms,order50):
    return target.distinct.phase_for_ms(int(at_ms),GAP,order50)


def run_case(runtime,by,cls,seed,active,order):
    case=magebridge.with_mage_lv31_fidelity(
        lambda: widthbridge.with_archer_final_width(
            v1.WIDTH,
            lambda: target.execute_with_ledger(runtime,by,cls,seed,active),
        )
    )
    blocks={int(x['result']['stage']):x for x in case['blocks']}
    s49=blocks[49]['result']; s50=blocks[50]['result']
    keys=('baseHp','baseMaxHp','wallDeficit','combo','charge','judgmentRng','combatProcRng')
    continuity={k:(s49['exitState'][k]==s50['entryState'][k]) for k in keys}
    pxp=[]
    for a in s50['actionTrace']:
        if a.get('heavy') and a.get('x')=='PERFECT' and a.get('y')=='PERFECT':
            pxp.append({
                'action':a['action'],'atMs':a['atMs'],'phase':phase_for(a['atMs'],order[50]),
                'lv31Final':a['lv31Final'],'chargeBefore':a['chargeBefore'],
                'comboAfter':a['comboAfter'],'primaryTargetId':a['primaryTargetId'],
                'primaryTargetType':a['primaryTargetType'],'primaryTargetY':a['primaryTargetY'],
            })
    return {
        'status':case['status'],'continuityErrors':case['continuityErrors'],
        'stage49Settled':s49['stageSettledTime'],'stage50Settled':s50['stageSettledTime'],
        'stage49RootActions':s49['rootTimingActionCount'],'stage50RootActions':s50['rootTimingActionCount'],
        'stage49ExitState':s49['exitState'],'stage50EntryState':s50['entryState'],
        'continuityEqual':continuity,'stage50PxP':pxp,
    }


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
    out={'version':'t1-stage49-50-state-phase-carryover-trace-v0.1','status':'DIAGNOSTIC_ATTRIBUTION_ONLY','sourceRecipeSha256':r.sha256_bytes(Path(args.recipes).read_bytes()),'fidelityErrors':[],'versions':{}}
    for vid in ('V01','V02'):
        doc,order=build(source,vid); runtime=r.build_runtime(doc,p3,p4,temporal); by={int(x['stage']):x for x in doc['recipes']}
        block={'order':order,'mageON':{},'archer503':{}}
        for seed in seeds:
            a=run_case(runtime,by,'mage',seed,ACTIVE_ON,order); b=run_case(runtime,by,'mage',seed,ACTIVE_ON,order)
            if r.sha256_obj(a)!=r.sha256_obj(b): out['fidelityErrors'].append(f'{vid}/mage/{seed}/determinism')
            out['fidelityErrors'].extend(f'{vid}/mage/{seed}/{e}' for e in a['continuityErrors'])
            if not all(a['continuityEqual'].values()): out['fidelityErrors'].append(f'{vid}/mage/{seed}/state-continuity')
            block['mageON'][str(seed)]=a
        for side,active in (('OFF',ACTIVE_OFF),('ON',ACTIVE_ON)):
            a=run_case(runtime,by,'archer',503,active,order); b=run_case(runtime,by,'archer',503,active,order)
            if r.sha256_obj(a)!=r.sha256_obj(b): out['fidelityErrors'].append(f'{vid}/archer503/{side}/determinism')
            out['fidelityErrors'].extend(f'{vid}/archer503/{side}/{e}' for e in a['continuityErrors'])
            if not all(a['continuityEqual'].values()): out['fidelityErrors'].append(f'{vid}/archer503/{side}/state-continuity')
            block['archer503'][side]=a
        out['versions'][vid]=block
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    for vid,b in out['versions'].items():
        print('\n',vid,'ORDER49',b['order'][49],'ORDER50',b['order'][50])
        for seed,x in b['mageON'].items():
            print(' MAGE',seed,'S49roots',x['stage49RootActions'],'exitCharge',x['stage49ExitState']['charge'],'exitCombo',x['stage49ExitState']['combo'],'S50PxP',json.dumps(x['stage50PxP'],sort_keys=True))
        for side,x in b['archer503'].items():
            print(' ARCHER503',side,'S49',x['stage49Settled'],'S50',x['stage50Settled'],'exitCharge',x['stage49ExitState']['charge'],'S50PxP',json.dumps(x['stage50PxP'],sort_keys=True))
    if out['fidelityErrors']:
        raise SystemExit('STATE_PHASE_CARRYOVER_FIDELITY_FAIL')

if __name__=='__main__': main()
