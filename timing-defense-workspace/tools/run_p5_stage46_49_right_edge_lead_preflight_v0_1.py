#!/usr/bin/env python3
import json, math, pathlib, sys
p=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else 'legacy-game-structure/data/p5_stage46_49_right_edge_lead_fixture_v0_1.json')
cfg=json.loads(p.read_text())
spawn=cfg['baseSpawnX']; wall=cfg['wallX']; trig=cfg['siegeTriggerX']; wind=cfg['siegeWindupSeconds']; root=cfg['rootAttackIntervalSeconds']
ss=cfg['monsterSpeeds']['SIEGER']; ds=cfg['monsterSpeeds']['ARMORED_DURABLE_PROXY']
shop=cfg['shopDiagnostic']; atk_mult=1+shop['balancedAtkRank']*shop['legacyAtkPctPerRank']*shop['effectScale']
res={'version':'p5-stage46-49-right-edge-lead-preflight-result-v0.1','rng':'NONE','shopAtkMultiplier':round(atk_mult,6),'stages':{},'nakedSiegerKillRoots':{}}
for cls,raw in cfg['ordinaryPerfectRawByClassBeforeShop'].items():
    dmg=raw*atk_mult
    res['nakedSiegerKillRoots'][cls]={'damagePerRootApprox':round(dmg,3),'rootsToKill520':math.ceil(cfg['nakedSiegerHp']/dmg)}
for st,v in cfg['stageLeadCandidates'].items():
    sl=float(v['siegerLeadSeconds']); dl=float(v['durableLeadSeconds'])
    sx=spawn-ss*sl; dx=spawn-ds*dl
    res['stages'][st]={
      'intent':v['intent'],
      'siegerLeadSeconds':sl,
      'siegerXAtPressureReferenceIfUntouched':round(sx,4),
      'siegerSecondsFromReferenceToFirstPossibleShotIfUntouched':round(max(0,(sx-trig)/ss)+wind,3),
      'durableLeadSeconds':dl,
      'durableXAtPressureReferenceIfUntouched':round(dx,4),
      'durableSecondsFromReferenceToWallIfUntouched':round(max(0,(dx-wall)/ds),3),
      'rootOpportunitiesDuringSiegerLeadApprox':math.floor(sl/root+1e-9)
    }
res['oldProxyConversion']={
  'siegerSpawnXCenter0.48EquivalentLeadSeconds':round((spawn-0.48)/ss,3),
  'siegerSpawnXRange0.45_0.55EquivalentLeadSeconds':[round((spawn-0.55)/ss,3),round((spawn-0.45)/ss,3)],
  'durableSpawnXCenter0.65EquivalentLeadSeconds':round((spawn-0.65)/ds,3),
  'durableSpawnXRange0.60_0.70EquivalentLeadSeconds':[round((spawn-0.70)/ds,3),round((spawn-0.60)/ds,3)]
}
res['classification']={
  'MIDFIELD_POP_IN_REQUIRED':False,
  'NAKED_EARLY_SIEGER_IS_SAFE_REPLACEMENT':False,
  'ESCORT_OR_FRONTMOST_PROTECTION_REQUIRED':True,
  'STAGE46_49_TRAVEL_LEAD_RAMP_IS_KINEMATICALLY_COHERENT':True,
  'FULL_COMBAT_RECONVERGENCE_REQUIRED':True
}
print(json.dumps(res,indent=2,sort_keys=True))
