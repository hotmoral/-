#!/usr/bin/env python3
"""T1 Stage49-50 rotating grammar diagnostic v0.1.

This probe follows the existing P4-D2 grammar-first direction rather than making both
late stages one wide split-axis encounter. It rotates learned T1 vocabulary through:
LINE -> CLUSTER -> FRONTLINE -> DURABLE_SCATTER, with an optional final LINE reprise.

Boundaries:
- Stage46-48 unchanged from exact v0.2 source;
- only GRUNT/RUNNER/BRUTE;
- all monster/class/shop/EXP/PxP scalars unchanged;
- authored 4s density <= 8;
- skilled central deterministic model;
- Archer Lv31 uses the conservative diagnostic continuous bridge yTol=0.20,
  corresponding to immediately-adjacent five-band centres; this is NOT a width freeze;
- no production authoring adoption.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import probe_t1_stage49_50_class_rotation_shape_v0_1 as shape
import probe_t1_archer_lv31_continuous_corridor_bridge_v0_1 as widthbridge

r = shape.r
ARCHER_DIAGNOSTIC_WIDTH = 0.20

PHASES = {
    "LINE": [
        ("GRUNT", 0.46), ("RUNNER", 0.48), ("BRUTE", 0.50),
        ("GRUNT", 0.44), ("RUNNER", 0.52), ("BRUTE", 0.46),
    ],
    "CLUSTER": [
        ("GRUNT", 0.42), ("RUNNER", 0.46), ("GRUNT", 0.50),
        ("RUNNER", 0.44), ("BRUTE", 0.48), ("GRUNT", 0.43),
    ],
    "FRONTLINE": [
        ("BRUTE", 0.44), ("BRUTE", 0.48), ("GRUNT", 0.46),
        ("RUNNER", 0.42), ("BRUTE", 0.50), ("RUNNER", 0.54),
    ],
    "DURABLE_SCATTER": [
        ("BRUTE", 0.18), ("RUNNER", 0.82), ("BRUTE", 0.78),
        ("RUNNER", 0.22), ("GRUNT", 0.50), ("BRUTE", 0.54),
    ],
}


def build_stage(stage: int, phase_names: list[str], phase_gap_ms: int, durable_extra: bool):
    offsets = [0, 400, 800, 1200, 1600, 2000]
    rows=[]
    for phase_i, name in enumerate(phase_names):
        phase = list(PHASES[name])
        if durable_extra and name in ("FRONTLINE", "DURABLE_SCATTER"):
            # Composition-only sensitivity: replace one light body, never add a body.
            typ, y = phase[-1]
            phase[-1] = ("BRUTE", y)
        base = phase_i * phase_gap_ms
        for off, (typ, y) in zip(offsets, phase):
            rows.append({"tMs": base + off, "type": typ, "y": y})
    return rows


def candidate(source: dict, cid: str, gap_ms: int, final_line_reprise: bool, durable_extra: bool):
    doc=copy.deepcopy(source)
    by={int(x['stage']):x for x in doc['recipes']}
    s49_phases=["DURABLE_SCATTER","LINE","FRONTLINE","CLUSTER"]
    s50_phases=["LINE","CLUSTER","FRONTLINE","DURABLE_SCATTER"]
    if final_line_reprise:
        s50_phases.append("LINE")

    by[49]['spawns']=build_stage(49,s49_phases,gap_ms,durable_extra)
    by[49]['formation']='F08'
    by[49]['formationSet']=['F01','F02','F03','F08']
    by[49]['cadence']='CD05'
    by[49]['pressureTags']=['RUSH','BULWARK','BASELINE','FLOOD']

    by[50]['spawns']=build_stage(50,s50_phases,gap_ms,durable_extra)
    by[50]['formation']='F01'
    by[50]['formationSet']=['F01','F02','F03','F08']
    by[50]['cadence']='CD05'
    by[50]['pressureTags']=['BASELINE','FLOOD','RUSH','BULWARK']

    doc['version']=f"{source['version']}+{cid}"
    doc['status']='EPHEMERAL_STAGE49_50_ROTATING_GRAMMAR_DIAGNOSTIC_NOT_AUTHORING'
    return doc


def execute(recipe_doc,p3,p4,temporal,seeds):
    return widthbridge.with_archer_final_width(
        ARCHER_DIAGNOSTIC_WIDTH,
        lambda: shape.execute_candidate(recipe_doc,p3,p4,temporal,seeds),
    )


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--recipes',required=True)
    ap.add_argument('--p3',default='legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json')
    ap.add_argument('--p4d2-base',default='legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json')
    ap.add_argument('--p4d2-temporal',default='legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json')
    ap.add_argument('--seeds',default='101,211,307')
    ap.add_argument('--json-out',required=True)
    args=ap.parse_args()

    source=r.load_yaml(args.recipes); p3=r.load_json(args.p3); p4=r.load_json(args.p4d2_base); temporal=r.load_json(args.p4d2_temporal)
    seeds=tuple(int(x) for x in args.seeds.split(',') if x.strip())
    source_by={int(x['stage']):x for x in source['recipes']}; cap=int(source['guards']['authored4sNormalMax'])

    specs=[
        ('ROT4_G4000',4000,False,False),
        ('ROT5_G4000',4000,True,False),
        ('ROT4_G3500',3500,False,False),
        ('ROT5_G3500',3500,True,False),
        ('ROT4_G4000_DUR',4000,False,True),
        ('ROT5_G4000_DUR',4000,True,True),
    ]
    candidates=[]; rejected=[]
    for cid,gap,reprise,durable in specs:
        doc=candidate(source,cid,gap,reprise,durable); by={int(x['stage']):x for x in doc['recipes']}
        errors=r.static_recipe_gate(doc)
        for stage in source_by:
            if stage not in (49,50) and by[stage] != source_by[stage]: errors.append(f'scope-change-stage{stage}')
        static={str(s):shape.stage_static(by[s]) for s in (49,50)}
        if any(v['max4s']>cap for v in static.values()): errors.append('AUTHORED_4S_DENSITY_EXCEEDS_NORMAL_CAP')
        if errors:
            rejected.append({'id':cid,'staticErrors':errors,'stageStatic':static}); continue
        dyn=execute(doc,p3,p4,temporal,seeds)
        candidates.append({'id':cid,'gapMs':gap,'finalLineReprise':reprise,'durableExtra':durable,'archerDiagnosticWidth':ARCHER_DIAGNOSTIC_WIDTH,'stageStatic':static,**dyn})

    out={
      'version':'t1-stage49-50-rotating-grammar-probe-v0.1',
      'status':'DIAGNOSTIC_SEARCH_NO_AUTHORING_ADOPTION',
      'sourceRecipe':str(args.recipes),
      'sourceRecipeSha256':r.sha256_bytes(Path(args.recipes).read_bytes()),
      'stageScope':[49,50],
      'grammarOrder':{
        'stage49':['DURABLE_SCATTER','LINE','FRONTLINE','CLUSTER'],
        'stage50':['LINE','CLUSTER','FRONTLINE','DURABLE_SCATTER','optional_LINE_reprise']
      },
      'archerWidthBridge':{'yTolerance':ARCHER_DIAGNOSTIC_WIDTH,'status':'DIAGNOSTIC_ONLY_NOT_NUMERICAL_FREEZE'},
      'normal4sCap':cap,'seeds':list(seeds),'candidates':candidates,'rejected':rejected
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('id offWall onWall offFail onFail offDamage onDamage offClasses onClasses offTop2 onTop2')
    for c in candidates:
        print(c['id'],c['OFF']['wallPositiveCases'],c['ON']['wallPositiveCases'],c['OFF']['failOrIncompleteCases'],c['ON']['failOrIncompleteCases'],c['OFF']['totalWallDamage'],c['ON']['totalWallDamage'],c['OFF']['classesWithWallPressure'],c['ON']['classesWithWallPressure'],c['OFF']['top2DamageShare'],c['ON']['top2DamageShare'])
        print('  OFF_BY_CLASS',json.dumps({k:v['totalWallDamage'] for k,v in c['OFF']['byClass'].items()},sort_keys=True))
        print('  ON_BY_CLASS ',json.dumps({k:v['totalWallDamage'] for k,v in c['ON']['byClass'].items()},sort_keys=True))
    if any(c['fidelityErrors'] for c in candidates): raise SystemExit('ROTATING_GRAMMAR_FIDELITY_FAIL')

if __name__=='__main__': main()
