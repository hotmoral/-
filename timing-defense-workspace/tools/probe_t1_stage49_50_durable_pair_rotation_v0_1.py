#!/usr/bin/env python3
"""Stage49-50 distributed durable-pair rotation probe v0.1.

Second bounded diagnostic after geometry-only search showed pressure remained Tank-only.
This probe keeps Stage46-48 and all combat scalars fixed, keeps Stage49/50 body counts
for base candidates, and changes only Stage49/50 type chronology + wide-axis placement.
Optional tail variants add a small late four-body learned-vocabulary pulse to test duration
without repeating the whole encounter.

Diagnostic only. No authoring adoption or numerical freeze.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import probe_t1_stage49_50_class_rotation_shape_v0_1 as shape

r = shape.r

S49_TYPES = {
    6: ["BRUTE","BRUTE","RUNNER","RUNNER","RUNNER","BRUTE","BRUTE","RUNNER","RUNNER","RUNNER","BRUTE","BRUTE","RUNNER","RUNNER","RUNNER"],
    8: ["BRUTE","BRUTE","RUNNER","RUNNER","BRUTE","BRUTE","RUNNER","RUNNER","BRUTE","BRUTE","RUNNER","RUNNER","BRUTE","BRUTE","RUNNER"],
}
S50_TYPES = {
    6: ["BRUTE","BRUTE","RUNNER","GRUNT","RUNNER","GRUNT","BRUTE","BRUTE","RUNNER","GRUNT","RUNNER","GRUNT","BRUTE","BRUTE","RUNNER","GRUNT","RUNNER","GRUNT"],
    8: ["BRUTE","BRUTE","RUNNER","GRUNT","BRUTE","BRUTE","RUNNER","GRUNT","BRUTE","BRUTE","RUNNER","GRUNT","BRUTE","BRUTE","RUNNER","GRUNT","RUNNER","GRUNT"],
}


def assign_pair_geometry(stage: int, types: list[str]):
    if stage == 49:
        bands = [0.20, 0.80]
    else:
        bands = [0.16, 0.84, 0.50]
    out=[]
    brute_i=0
    light_i=0
    for typ in types:
        if typ == "BRUTE":
            idx=brute_i
            brute_i += 1
        else:
            idx=light_i + 1
            light_i += 1
        out.append(bands[idx % len(bands)])
    return out


def pairwave_candidate(source: dict, brute_level: int, tail_copies: int):
    doc=copy.deepcopy(source)
    by={int(x['stage']):x for x in doc['recipes']}
    for stage, pattern in ((49,S49_TYPES[brute_level]),(50,S50_TYPES[brute_level])):
        recipe=by[stage]
        times=[int(x['tMs']) for x in recipe['spawns']]
        if len(times) != len(pattern):
            raise RuntimeError(f'stage{stage} count mismatch {len(times)} != {len(pattern)}')
        ys=assign_pair_geometry(stage, pattern)
        recipe['spawns']=[{'tMs':t,'type':typ,'y':y} for t,typ,y in zip(times,pattern,ys)]
        recipe['formation']='F08'
        recipe['formationSet']=sorted(set(recipe.get('formationSet',[]))|{'F08'})
        recipe['pressureTags']=sorted(set(recipe.get('pressureTags',[]))|{'BULWARK','RUSH'})
        if tail_copies:
            if stage == 49:
                tail_types=['BRUTE','BRUTE','RUNNER','RUNNER']
                tail_ys=[0.20,0.80,0.20,0.80]
            else:
                tail_types=['BRUTE','BRUTE','GRUNT','RUNNER']
                tail_ys=[0.16,0.84,0.50,0.16]
            tail_offsets=[0,250,500,750]
            start0=14000 + (1000 if stage==50 else 0)
            for copy_i in range(tail_copies):
                start=start0 + copy_i*14000
                for off,typ,y in zip(tail_offsets,tail_types,tail_ys):
                    recipe['spawns'].append({'tMs':start+off,'type':typ,'y':y})
            recipe['spawns'].sort(key=lambda x:(int(x['tMs']),str(x['type']),float(x['y'])))
    doc['version']=f"{source['version']}+durable-pair-b{brute_level}-tail{tail_copies}"
    doc['status']='EPHEMERAL_STAGE49_50_DURABLE_PAIR_DIAGNOSTIC_NOT_AUTHORING'
    return doc


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--recipes',required=True)
    ap.add_argument('--p3',default='legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json')
    ap.add_argument('--p4d2-base',default='legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json')
    ap.add_argument('--p4d2-temporal',default='legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json')
    ap.add_argument('--seeds',default='101,211,307')
    ap.add_argument('--json-out',required=True)
    args=ap.parse_args()

    source=r.load_yaml(args.recipes)
    p3=r.load_json(args.p3)
    p4=r.load_json(args.p4d2_base)
    temporal=r.load_json(args.p4d2_temporal)
    seeds=tuple(int(x) for x in args.seeds.split(',') if x.strip())
    source_by={int(x['stage']):x for x in source['recipes']}
    cap=int(source['guards']['authored4sNormalMax'])

    specs=[
        ('PAIR_B6',6,0),
        ('PAIR_B8',8,0),
        ('PAIR_B6_TAIL4_X1',6,1),
        ('PAIR_B8_TAIL4_X1',8,1),
        ('PAIR_B6_TAIL4_X2',6,2),
        ('PAIR_B8_TAIL4_X2',8,2),
    ]
    candidates=[]; rejected=[]
    for cid,brutes,tails in specs:
        doc=pairwave_candidate(source,brutes,tails)
        by={int(x['stage']):x for x in doc['recipes']}
        errors=r.static_recipe_gate(doc)
        for stage in source_by:
            if stage not in (49,50) and by[stage] != source_by[stage]:
                errors.append(f'scope-change-stage{stage}')
        static={str(s):shape.stage_static(by[s]) for s in (49,50)}
        if any(v['max4s']>cap for v in static.values()):
            errors.append('AUTHORED_4S_DENSITY_EXCEEDS_NORMAL_CAP')
        if errors:
            rejected.append({'id':cid,'staticErrors':errors,'stageStatic':static}); continue
        dyn=shape.execute_candidate(doc,p3,p4,temporal,seeds)
        candidates.append({'id':cid,'targetBrutesPerStage':brutes,'tailCopies':tails,'stageStatic':static,**dyn})

    out={
        'version':'t1-stage49-50-durable-pair-rotation-probe-v0.1',
        'status':'DIAGNOSTIC_SEARCH_NO_AUTHORING_ADOPTION',
        'sourceRecipe':str(args.recipes),
        'sourceRecipeSha256':r.sha256_bytes(Path(args.recipes).read_bytes()),
        'stageScope':[49,50],
        'seeds':list(seeds),
        'normal4sCap':cap,
        'candidates':candidates,
        'rejected':rejected,
    }
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')

    print('id offWall onWall offFail onFail offDamage onDamage offClasses onClasses offTop2 onTop2')
    for c in candidates:
        print(c['id'],c['OFF']['wallPositiveCases'],c['ON']['wallPositiveCases'],c['OFF']['failOrIncompleteCases'],c['ON']['failOrIncompleteCases'],c['OFF']['totalWallDamage'],c['ON']['totalWallDamage'],c['OFF']['classesWithWallPressure'],c['ON']['classesWithWallPressure'],c['OFF']['top2DamageShare'],c['ON']['top2DamageShare'])
        print('  OFF_BY_CLASS',json.dumps({k:v['totalWallDamage'] for k,v in c['OFF']['byClass'].items()},sort_keys=True))
        print('  ON_BY_CLASS ',json.dumps({k:v['totalWallDamage'] for k,v in c['ON']['byClass'].items()},sort_keys=True))
    if any(c['fidelityErrors'] for c in candidates):
        raise SystemExit('DURABLE_PAIR_PROBE_FIDELITY_FAIL')

if __name__=='__main__':
    main()
