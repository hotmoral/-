#!/usr/bin/env python3
"""TEMP P5 Stage48 calculated escort-handoff ladder feasibility diagnostic.

Uses current provisional speeds only to derive late SHIELD spawn delays that should overtake a
SIEGER at selected elapsed times. This is a feasibility probe, not Stage48 authoring.
All physical spawns remain x=0.92. No monster/class/shop numerical changes.
"""
from __future__ import annotations
import copy, inspect, json
from pathlib import Path
import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_real_monster_frontline_search_temp_v2 as v2

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def row(typ,band,t,ref=0.0): return {'type':typ,'band':int(band),'referenceOffset':float(ref),'spawnLeadSeconds':float(12.0+ref-t)}
def now_from_stack():
    f=inspect.currentframe()
    try:
        f=f.f_back
        while f:
            v=f.f_locals.get('now')
            if isinstance(v,(int,float)): return round(float(v),4)
            f=f.f_back
    finally: del f
    return None

def make(direction,name,catch_targets):
    # Current anchors: SIEGER .045, SHIELD .057. For SHIELD spawned delta after SIEGER,
    # catch time from SIEGER spawn = delta * v_shield/(v_shield-v_sieger) = 4.75*delta.
    s_t=8.0
    screens=[row('BRUTE',-2,6.0),row('SHIELD',-1,6.5)]
    for i,target_t in enumerate(catch_targets):
        delay=float(target_t)/4.75
        screens.append(row('SHIELD',-2 if i%2==0 else -1,s_t+delay,2.5+i*0.2))
    d=copy.deepcopy(direction); s=d['stageDirection']['48']; s['pressureCycleSecondsCandidate']=999.0
    s['diagnosticPacket']=screens+[row('SIEGER',2,s_t,2.0)]
    s['note']=f'TEMP_CALCULATED_HANDOFF_LADDER:{name}'
    integ.validate_right_edge_contract(d)
    return d

def main():
    base=load('legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json')
    temporal=load('legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json')
    stage49=load('legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json')
    direction=load('legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json')
    shop=load('legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json')
    integration=load('legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json')
    integ.validate_right_edge_contract(direction); base=integ.inject_diagnostic_monsters(base,stage49); settled.install_fixed_schedule_hook()
    variants={
        'HANDOFF_3_SHIELDS_CATCH_4_8_11':make(direction,'HANDOFF_3_SHIELDS_CATCH_4_8_11',[4.0,8.0,11.0]),
        'HANDOFF_4_SHIELDS_CATCH_3_6_9_11':make(direction,'HANDOFF_4_SHIELDS_CATCH_3_6_9_11',[3.0,6.0,9.0,11.0]),
    }
    scale=float(integration['shopEffectScale']); profile='BALANCED'; starts=v2.pre_stage48_states(base,temporal,direction,shop,integration,[profile],scale)
    glb=integ.SIMULATE.__globals__; oh,on,om=glb['hit'],glb['nearest'],glb['make_mob']; trace=None
    def mw(mon,cfg,typ,band,idx):
        m=om(mon,cfg,typ,band,idx)
        if trace is not None and typ=='SIEGER': trace['s']={'spawnAt':now_from_stack(),'firstDamageAt':None,'firstPrimaryAt':None,'deathAt':None,'deathX':None}
        return m
    def nw(mobs):
        p=on(mobs)
        if trace is not None and p is not None and p.typ=='SIEGER' and trace.get('s') and trace['s']['firstPrimaryAt'] is None: trace['s']['firstPrimaryAt']=now_from_stack()
        return p
    def hw(mon,cfg,mobs,target,raw,stats,counter,armor_ignore=False):
        t=now_from_stack(); iss=target is not None and getattr(target,'typ',None)=='SIEGER'; alive=bool(getattr(target,'alive',False)) if target else False; bx=float(getattr(target,'x',0.0)) if target else None
        if iss and trace is not None and trace.get('s') and trace['s']['firstDamageAt'] is None: trace['s']['firstDamageAt']=t
        res=oh(mon,cfg,mobs,target,raw,stats,counter,armor_ignore=armor_ignore)
        if iss and trace is not None and trace.get('s') and alive and not bool(getattr(target,'alive',False)) and trace['s']['deathAt'] is None: trace['s']['deathAt']=t; trace['s']['deathX']=round(bx,4)
        return res
    glb['hit'],glb['nearest'],glb['make_mob']=hw,nw,mw
    out={'version':'p5-stage48-calculated-handoff-ladder-temp-v0.1','authority':'TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY','rows':[],'schedules':{}}
    try:
        for name,d in variants.items():
            cfg=integ.stage_temporal(temporal,d,integration,48,'Knight'); sched=integ.build_integrated_schedule(cfg)
            out['schedules'][name]=[{'t':round(t,3),'type':typ,'band':band} for t,typ,band in sched]
            for cls in integ.CLASSES:
                st=starts[(profile,cls)]; trace={}
                sim,_=settled.simulate_stage(base,temporal,d,integration,cls,st['profile'],scale,48,st['startStage48Wall'],0.25 if cls=='Tank' else None,120.0)
                s=trace.get('s') or {}; sp=s.get('spawnAt'); fd=s.get('firstDamageAt'); fp=s.get('firstPrimaryAt'); de=s.get('deathAt')
                out['rows'].append({'variant':name,'class':cls,'windups':int(sim.get('siegerWindups') or 0),'shots':int(sim.get('siegerShots') or 0),'repositions':int(sim.get('siegerRepositions') or 0),'wallHits':int(sim.get('wallHits') or 0),'endWall':sim.get('endWall'),'burialTime':sim.get('burialTime'),'firstDamageAfterSpawn':round(fd-sp,4) if fd is not None and sp is not None else None,'firstPrimaryAfterSpawn':round(fp-sp,4) if fp is not None and sp is not None else None,'deathAfterSpawn':round(de-sp,4) if de is not None and sp is not None else None,'deathX':s.get('deathX'),'diedBeforePrimary':bool(de is not None and (fp is None or de<fp-1e-9))})
                trace=None
    finally: glb['hit'],glb['nearest'],glb['make_mob']=oh,on,om
    text=json.dumps(out,indent=2,sort_keys=True); Path('p5_stage48_calculated_handoff_ladder_temp.json').write_text(text+'\n',encoding='utf-8'); print(text)
if __name__=='__main__': main()
