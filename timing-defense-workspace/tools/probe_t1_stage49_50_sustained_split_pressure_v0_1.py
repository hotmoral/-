#!/usr/bin/env python3
"""Stage49-50 sustained split-pressure chronology probe v0.1.

Bounded third diagnostic after geometry-only and durable-pair candidates remained Tank-skewed.
Only Stage49/50 composition/geometry/chronology changes. Scalars and Stage46-48 stay fixed.
The search replaces burst/repeat structures with a continuous legal stream under max4s<=8.
Diagnostic only; no authoring adoption.
"""
from __future__ import annotations
import argparse, copy, json
from pathlib import Path
import probe_t1_stage49_50_class_rotation_shape_v0_1 as shape
r=shape.r


def make_stream(stage:int,count:int,interval:int,brute_mode:str):
    if stage==49:
        if brute_mode=='QUARTER': pattern=['RUNNER','RUNNER','BRUTE','RUNNER']
        else: pattern=['RUNNER','BRUTE','RUNNER']
        bands=[0.20,0.80]
    else:
        if brute_mode=='QUARTER': pattern=['RUNNER','GRUNT','BRUTE','RUNNER']
        else: pattern=['RUNNER','BRUTE','GRUNT']
        bands=[0.16,0.84,0.50]
    out=[]; brute_i=0; light_i=0
    for i in range(count):
        typ=pattern[i%len(pattern)]
        if typ=='BRUTE': idx=brute_i; brute_i+=1
        else: idx=light_i+1; light_i+=1
        out.append({'tMs':i*interval,'type':typ,'y':bands[idx%len(bands)]})
    return out


def candidate(source:dict,cid:str,interval:int,c49:int,c50:int,brute_mode:str):
    doc=copy.deepcopy(source); by={int(x['stage']):x for x in doc['recipes']}
    for stage,count in ((49,c49),(50,c50)):
        rec=by[stage]
        rec['spawns']=make_stream(stage,count,interval,brute_mode)
        rec['formation']='F08'; rec['formationSet']=sorted(set(rec.get('formationSet',[]))|{'F08'})
        rec['cadence']='CD05'
        rec['pressureTags']=sorted(set(rec.get('pressureTags',[]))|{'RUSH','BULWARK'})
    doc['version']=f"{source['version']}+{cid}"
    doc['status']='EPHEMERAL_STAGE49_50_SUSTAINED_SPLIT_DIAGNOSTIC_NOT_AUTHORING'
    return doc


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--recipes',required=True)
    ap.add_argument('--p3',default='legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json')
    ap.add_argument('--p4d2-base',default='legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json')
    ap.add_argument('--p4d2-temporal',default='legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json')
    ap.add_argument('--seeds',default='101,211,307'); ap.add_argument('--json-out',required=True); args=ap.parse_args()
    source=r.load_yaml(args.recipes); p3=r.load_json(args.p3); p4=r.load_json(args.p4d2_base); temporal=r.load_json(args.p4d2_temporal)
    seeds=tuple(int(x) for x in args.seeds.split(',') if x.strip()); source_by={int(x['stage']):x for x in source['recipes']}; cap=int(source['guards']['authored4sNormalMax'])
    specs=[
      ('SUSTAIN_650_Q',650,20,22,'QUARTER'),
      ('SUSTAIN_650_T',650,20,22,'THIRD'),
      ('SUSTAIN_600_Q',600,22,24,'QUARTER'),
      ('SUSTAIN_600_T',600,22,24,'THIRD'),
      ('SUSTAIN_550_Q',550,22,26,'QUARTER'),
      ('SUSTAIN_550_T',550,22,26,'THIRD'),
      ('SUSTAIN_500_Q',500,24,28,'QUARTER'),
      ('SUSTAIN_500_T',500,24,28,'THIRD'),
    ]
    candidates=[]; rejected=[]
    for cid,interval,c49,c50,mode in specs:
        doc=candidate(source,cid,interval,c49,c50,mode); by={int(x['stage']):x for x in doc['recipes']}; errors=r.static_recipe_gate(doc)
        for stage in source_by:
            if stage not in (49,50) and by[stage] != source_by[stage]: errors.append(f'scope-change-stage{stage}')
        static={str(s):shape.stage_static(by[s]) for s in (49,50)}
        if any(v['max4s']>cap for v in static.values()): errors.append('AUTHORED_4S_DENSITY_EXCEEDS_NORMAL_CAP')
        if errors: rejected.append({'id':cid,'staticErrors':errors,'stageStatic':static}); continue
        dyn=shape.execute_candidate(doc,p3,p4,temporal,seeds)
        candidates.append({'id':cid,'intervalMs':interval,'stage49Count':c49,'stage50Count':c50,'bruteMode':mode,'stageStatic':static,**dyn})
    out={'version':'t1-stage49-50-sustained-split-pressure-probe-v0.1','status':'DIAGNOSTIC_SEARCH_NO_AUTHORING_ADOPTION','sourceRecipe':str(args.recipes),'sourceRecipeSha256':r.sha256_bytes(Path(args.recipes).read_bytes()),'stageScope':[49,50],'normal4sCap':cap,'seeds':list(seeds),'candidates':candidates,'rejected':rejected}
    Path(args.json_out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('id offWall onWall offFail onFail offDamage onDamage offClasses onClasses offTop2 onTop2')
    for c in candidates:
        print(c['id'],c['OFF']['wallPositiveCases'],c['ON']['wallPositiveCases'],c['OFF']['failOrIncompleteCases'],c['ON']['failOrIncompleteCases'],c['OFF']['totalWallDamage'],c['ON']['totalWallDamage'],c['OFF']['classesWithWallPressure'],c['ON']['classesWithWallPressure'],c['OFF']['top2DamageShare'],c['ON']['top2DamageShare'])
        print('  OFF_BY_CLASS',json.dumps({k:v['totalWallDamage'] for k,v in c['OFF']['byClass'].items()},sort_keys=True))
        print('  ON_BY_CLASS ',json.dumps({k:v['totalWallDamage'] for k,v in c['ON']['byClass'].items()},sort_keys=True))
    if any(c['fidelityErrors'] for c in candidates): raise SystemExit('SUSTAINED_SPLIT_PROBE_FIDELITY_FAIL')
if __name__=='__main__': main()
