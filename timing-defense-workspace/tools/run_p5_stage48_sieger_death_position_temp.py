#!/usr/bin/env python3
"""TEMP: compare SIEGER death position under current proxy packet vs real-monster screens."""
from __future__ import annotations

import copy
import json
from collections import defaultdict
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_real_monster_frontline_search_temp_v2 as v2


def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    base=load('legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json')
    temporal=load('legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json')
    stage49=load('legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json')
    direction=load('legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json')
    shop=load('legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json')
    refinement=load('legacy-game-structure/data/p5_class_identity_refinement_fixture_v0_1.json')
    integration=load('legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json')
    integ.validate_right_edge_contract(direction)
    base=integ.inject_diagnostic_monsters(base,stage49)
    if 'ARMORED_DURABLE_PROXY' not in base['monsterAnchors']:
        base['monsterAnchors']['ARMORED_DURABLE_PROXY']=dict(refinement['knightRobustPair']['anchor'])
    settled.install_fixed_schedule_hook()
    scale=float(integration['shopEffectScale']); profiles=list(integration['representativeShopProfiles'])
    starts=v2.pre_stage48_states(base,temporal,direction,shop,integration,profiles,scale)

    candidates={'CURRENT_PROXY_PACKET':direction}
    vv=v2.variants(direction)
    for name in ('BRUTE_PAIR_LONG_LEAD','BRUTE_TRAIN_FOUR','BRUTE_SPLITTER_LAYER'):
        candidates[name]=vv[name]

    glb=integ.SIMULATE.__globals__
    original_hit=glb['hit']
    collector=[]
    context={'variant':None,'class':None,'profile':None}

    def wrapped_hit(mon,cfg,mobs,target,raw,stats,counter,armor_ignore=False):
        before_alive=bool(getattr(target,'alive',False))
        before_hp=float(getattr(target,'hp',0.0))
        before_x=float(getattr(target,'x',0.0))
        before_state=str(getattr(target,'state',''))
        result=original_hit(mon,cfg,mobs,target,raw,stats,counter,armor_ignore=armor_ignore)
        if getattr(target,'typ',None)=='SIEGER':
            after_alive=bool(getattr(target,'alive',False))
            collector.append({
                **context,
                'id':str(getattr(target,'id','UNKNOWN')),
                'x':round(before_x,4),
                'state':before_state,
                'hpBefore':round(before_hp,3),
                'raw':round(float(raw),3),
                'armorIgnore':bool(armor_ignore),
                'killedThisHit':bool(before_alive and not after_alive),
            })
        return result

    glb['hit']=wrapped_hit
    out={'variants':{}}
    try:
        for name,d in candidates.items():
            rows=[]
            for cls in integ.CLASSES:
                profile_name='BALANCED'; st=starts[(profile_name,cls)]
                context.update({'variant':name,'class':cls,'profile':profile_name})
                before=len(collector)
                row,_=settled.simulate_stage(base,temporal,d,integration,cls,st['profile'],scale,48,st['startStage48Wall'],0.25 if cls=='Tank' else None,120.0)
                ev=collector[before:]
                deaths=[x for x in ev if x['killedThisHit']]
                rows.append({
                    'class':cls,
                    'siegerWindups':int(row.get('siegerWindups') or 0),
                    'siegerShots':int(row.get('siegerShots') or 0),
                    'siegerRepositions':int(row.get('siegerRepositions') or 0),
                    'siegerHitEvents':len(ev),
                    'siegerDeathsByHit':len(deaths),
                    'deathX':[x['x'] for x in deaths],
                    'minDeathX':min((x['x'] for x in deaths),default=None),
                    'maxDeathX':max((x['x'] for x in deaths),default=None),
                    'firstFiveDeathEvents':deaths[:5],
                    'wallHits':int(row.get('wallHits') or 0),
                    'endWall':row.get('endWall'),
                })
            out['variants'][name]=rows
    finally:
        glb['hit']=original_hit

    text=json.dumps(out,indent=2,sort_keys=True)
    Path('p5_stage48_sieger_death_position_temp.json').write_text(text+'\n',encoding='utf-8')
    print(text)

if __name__=='__main__': main()
