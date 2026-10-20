# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.30**
- Public URL: `https://timing-defense-v011.onrender.com/v030.html`
- Live source HEAD: `a235bf2dc0bd5bb5138b4bd89d81512345ec6713`
- Render deploy: `dep-dbbhud8n74is73cp0rug` / LIVE

Workspace remains canonical for design decisions, simulation interpretation, and new-session recovery.

---

# Frozen combat / role decisions
- Knight: stable generalist / penetration / strong heavy.
- Rogue: multihit / crit / durable-normal execution; same-target dagger hits uncapped.
- Tank: team-specialist / knockback / wall protection.
- Archer: strict straight-line trajectory; no bending/seeking.
- Mage: density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP remains tied to valid timing events; passive attacks grant no EXP.
- Balance gaps must be reported/discussed before numerical patching.
- Current combo presentation is approved; do not change unless explicitly requested.

Experimental values remain not production-frozen:
- passive 40 raw / 2.0 s,
- ordinary non-boss HP +10%,
- combo persistent 5/8/12/15% candidate,
- combo milestone raw-equivalent 60/90/150/210 cap.

---

# Core combat state
- Rhythm `X → X → X → X+Y`.
- Skills implemented through Lv21; Lv26/Lv31 planned.
- New timing turn starts only with a visible target.
- Empty-target turns do not grant EXP.
- Already-started valid turns survive target disappearance.
- Heavy X→Y can finish after target disappearance.
- Target wait/stage downtime do not break combo.
- Stage intro: `STAGE N / READY → fade → START! + combat`.
- Passive auto-attack interval remains common across classes at 2.0 s.

---

# Approved class radar
Axes: `공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역`

Values:
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`

Five visual levels. Equal levels are allowed. Radar is class-identity presentation, not literal raw-stat output.

---

# Stable presentation foundation through v0.26
- Character select with nickname + five-class carousel.
- Left profile / center hero / right 3×2 skills.
- Animated class radar.
- Rich role/detail copy.
- `습득 LV N` skill card presentation.
- Rogue HUD charcoal/black + silver.
- Projectile visibility pass without travel-time change.
- BASE HP top-center gauge.
- Top-right STAGE → LV → KILLS.
- Combat title removed; combo untouched.
- Fortified home-base visual.
- Combat skill strip reuses lobby skill artwork.

---

# v0.27 intended features and regression
Read `V027_DEVICE_FIX_WAITING_UX_REPORT.md` and `V030_ROOT_CAUSE_RECOVERY_REPORT.md`.

Intended v0.27 features:
- one-line skill name and acquisition level,
- correct radar aspect ratio,
- Android horizontal swipe,
- fixed arrows,
- result PLAYER / CLASS collision fix,
- local TEAM waiting UX for FRIEND / LINK / RANDOM.

Critical regression found after device audit:

```js
function normalizeSkillLevels(){
  root?.querySelectorAll('.v024SkillLv').forEach(el=>{
    const n=(el.textContent||'').match(/\d+/)?.[0]||'';
    if(n) el.textContent=`습득 LV ${n}`;
  })
}
new MutationObserver(normalizeSkillLevels).observe(root,{childList:true,subtree:true});
```

Because the callback rewrites `textContent` even when it is already identical, the observer can retrigger itself indefinitely. v0.26 had an equality guard and did not have this defect.

This is the primary known root cause for the severe partial-render/freeze behavior introduced at v0.27.

---

# v0.28 / v0.29 superseded
The viewport/orientation recovery experiments were based on the half-width symptom before the observer loop was found.

Do not continue their strategy by default:
- no numeric viewport-meta width rewriting,
- no physical-screen-width forcing,
- no screen/outer/inner width heuristics unless clean v0.30 evidence later proves a separate viewport defect.

v0.30 does not load v0.28 or v0.29 scripts.

---

# Current implementation — v0.30
Files:
- `timing-defense-v011/v030-safety.js`
- `timing-defense-v011/v030.html`

Read first:
- `V030_ROOT_CAUSE_RECOVERY_REPORT.md`

Loader strategy:
1. load through the known v0.26 foundation,
2. run `v030-safety.js`,
3. run existing `v027-polish.js`.

`v030-safety.js` intercepts only the defective redundant `normalizeSkillLevels` MutationObserver. The safe v0.26 normalizer remains active and already provides `습득 LV N`.

Orientation:
- game is landscape-only,
- portrait is blocked with a simple max-z-index overlay,
- no viewport width/meta manipulation occurs.

Preserved v0.27 UX:
- skill one-line headers,
- radar aspect fix,
- swipe + arrows,
- result class badge layout,
- TEAM local waiting screens.

No combat, combo, balance, projectile timing, or multiplayer-authority behavior changed.

---

# Network truth boundary
Actual multiplayer is still **not implemented**.
Do not claim multiplayer is live until two independent clients join the same authoritative room and synchronize game state.

TEAM slot rule:
- SOLO: AI 0–3
- TEAM: AI FILL 0–2, leaving at least one human slot.

FRIEND/LINK/RANDOM are local waiting UX only.

---

# Exact next work boundary
1. Device-test public v0.30 on the same Samsung Browser device.
2. Confirm direct landscape load fills the full content width and remains responsive.
3. Confirm no gradual/partial render freeze.
4. Verify skill name + `습득 LV N`, radar shape, arrows, and swipe.
5. Rotate portrait and verify only the landscape-only gate.
6. Rotate back and verify the full-width lobby returns without width forcing.
7. Verify result board and TEAM waiting screens.
8. Fix only defects reproducible from the clean v0.30 chain.
9. Then design actual multiplayer architecture.
10. After network foundation, continue Lv26/Lv31 implementation and full-run balance simulation.

## Still unresolved
- actual room/network backend,
- invite/link security contract,
- matchmaking policy,
- reconnect/reconciliation,
- multiplayer economy/shop ownership,
- duplicate-class policy,
- DUO/TRIPLE/FULL synchronization,
- Lv26/Lv31 coefficients,
- final passive/HP/combo coefficients,
- final E/X/tier values,
- final result metric policy.

---

# New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `V030_ROOT_CAUSE_RECOVERY_REPORT.md`
4. `V027_DEVICE_FIX_WAITING_UX_REPORT.md`
5. `V026_HUD_LAYOUT_REPORT.md`
6. `V025_LAYOUT_POLISH_REPORT.md`
7. `V024_RADAR_READABILITY_REPORT.md`
8. `CHARACTER_PROFILE_RADAR_V1.md`
9. `DESIGN_DECISIONS.md`
10. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
11. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
12. `SKILL_PLAN_LV6_31.md`
13. `TIER_PRESSURE_GRAMMAR_V1.md`
14. `PRESSURE_RECIPES_V1.md`
15. `SIMULATION_METHOD.md`
16. `NEXT_WORK.md`
