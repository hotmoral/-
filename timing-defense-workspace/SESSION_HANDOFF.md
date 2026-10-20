# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.22**
- Public URL: `https://timing-defense-v011.onrender.com/v022.html`
- Live source HEAD: `7a321d021cafbfc32749b4e8b9421b2bf908826a`
- Render deploy: `dep-dbbef5s9v7es73eupvlg` / LIVE

Workspace is canonical for design decisions, simulation interpretation and new-session recovery. Live branch is kept separate.

---

# Frozen combat / role decisions
- Knight: stable generalist / penetration / strong heavy.
- Rogue: multihit / crit / durable-normal execution; same-target dagger hits uncapped.
- Tank: team-specialist / knockback / wall protection; fresh-run solo parity not required.
- Archer: true straight-line trajectory; no off-line retarget/bending.
- Mage: density/AoE specialist.
- Boss dagger scalar = `0.70`.
- Boss knockback scalar = `0.40`.
- EXP remains tied to valid timing results/events.
- Passive basic attacks grant no EXP.

Mastery references:
- Average = N25 / G55 / P20.
- Skilled = N10 / G50 / P40 plus modestly faster commitment.

Balance governance:
`measure/model → classify intent/artifact/defect → report → discuss → explicit decision → numerical patch`

Do not rebalance automatically from a large simulation gap.

---

# Core combat state retained

## Skills
Implemented automatic milestones:
`Lv6 / Lv11 / Lv16 / Lv21`.

Reserved:
`Lv26 / Lv31`.

## Target / turn rule
- New Timing Square turn starts only with a visible target.
- If none exists at the next-turn boundary, Timing Square enters target-wait.
- AI/passive attacks wait too.
- No empty-turn EXP farming.
- Off-screen targets cannot be damaged/rewarded.

Once a valid local timing turn has begun, it is never cancelled merely because teammates/passive damage remove the last target:
- normal X remains tappable,
- heavy X→Y can finish,
- normal judgment/EXP for that already-started turn remains valid,
- only the next turn waits.

Target-wait and stage downtime do not break combo.

## Stage intro
Current flow:
`STAGE N / READY → fade → combat becomes active + START!`

During the intro there is no enemy progression, AI/passive attack or Timing Square input/sweep.

---

# Current experimental combat coefficients — still NOT production-frozen

Passive basic attack:
- `40 raw / 2.0 s`
- no EXP / charge / crit / skill / combo
- knockback suppressed
- non-boss HP +10%

PERFECT combo:
- PERFECT only
- GOOD/NORMAL/MISS reset
- heavy X/Y count separately
- count unbounded
- no hidden timing difficulty escalation

Persistent bonus:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap

Milestone budgets:
- 5 = 60
- 10 = 90
- 20 = 150
- 30+ = 210 cap
- 40/50/60… repeat 30-tier power.

User device testing has confirmed the conceptual value of passive breathing-room and combo tension, but not frozen these coefficients.

---

# v0.21 — presentation polish

Historical public page: `https://timing-defense-v011.onrender.com/v021.html`
HEAD `5a1c7fbfb575e805ce65eb238157abd2136ba3fa`
Render `dep-dbbec549v7es73euenkg`

See `V021_IMPLEMENTATION_REPORT.md`.

Changes:
- remove lower-left EXP float,
- show `+EXP N` beside EXP gauge,
- timing judgments pop quickly **inside** Timing Square with tier-specific size/color/glow,
- natural geometric scenery replaces black grid,
- centered result panel,
- centered `START!` at combat activation,
- debug N/G/P/C/AVG and hint hidden.

No numerical balance changes.

---

# Current playable implementation — v0.22 pre-game lobby

Files:
- `timing-defense-v011/v022-lobby.js`
- `timing-defense-v011/v022.html`

See `V022_LOBBY_IMPLEMENTATION_REPORT.md`.

## Production-direction entry flow
`nickname + class carousel → play settings → run / future team waiting → stage intro → combat`

The old in-combat class selector and bottom TEAM/SPEED/RESET test controls are hidden.

## Nickname
- required to continue,
- remembered locally in the browser.

## Character carousel
- five classes,
- smooth horizontal slide,
- arrow buttons + swipe,
- one large class presentation at a time,
- geometric but deliberately differentiated clothing/weapon silhouette,
- role summary,
- six skill cards with unlock level and descriptions.

## Skill-icon design rule
Icons must be **mechanically legible**, not merely class-colored.
Use different silhouettes/colors for different effects.
Examples already implemented:
- Knight double slash visually uses multiple blade shapes.
- Rogue dual/barrage/rain skills show multiple daggers.
- Tank skills show shield/shockwave/crack/rings.
- Archer Triple Shot shows three arrows; pierce skills show line penetration.
- Mage skills show blast, expansion, resonance, chain and collapse forms.

This rule applies to both lobby roadmap icons and eventual production HUD assets.

## Play settings interaction
For small fixed choice sets, prefer visible **buttons/segmented controls** over dropdowns when this is faster on mobile.

Current v0.22 settings:
- SOLO / TEAM
- AI NONE / +1 / +2 / +3
- AI P2/P3/P4 position
- AI class per enabled slot
- TEAM method FRIEND / LINK / RANDOM
- Tier1 only for now

Defaults:
- SOLO
- AI NONE
- highest available tier (currently Tier1)

Solo+AI applies the selected AI classes/positions and starts the actual run immediately.

## Network truth boundary
FRIEND / LINK / RANDOM are only the front-end selection surface in v0.22.
**There is no real room, invite, link join or random matchmaking backend yet.**
The UI must not claim that a remote player connected.

Next UX slice: v0.23 waiting-room flows.
After that: actual multiplayer room/match networking.

## End-run
Explicit `RETRY` and `LOBBY` buttons replace reliance on hidden prototype controls.

---

# End-run team board
Current metrics:
- KILLS
- DMG
- COIN
- LV
- MAX COMBO

Rows follow actual character slot order.
Each metric has rank styling: gold / silver / bronze / muted.
No forced global MVP.

---

# Encounter framework retained
Pressure families:
- S = Swarm
- E = Elite/Heavy
- X = Special/Mixed

1/2/3-pattern stages all valid. All three are not forced into every stage.

Candidate Swarm bursts:
- line 2P/3P/4P = 8 / 11 / 14
- cluster = 7 / 10 / 13
- scatter = 9 / 12 / 16

---

# Simulation state retained

## v7 exact-formula rerun
- Lv21 3P Average/Skilled = 81.6 / 96.4%
- Lv21 4P = 52.8 / 73.6%
- Rogue remains best durable-normal killer
- Archer remains strongest on line geometry
- no numerical class rebalance authorized.

## v8 passive/combo calibration
Around 150 judgments:
- Skilled P40: 5 combo ~61%, 10 ~0.87%, 20 ~0
- Expert P65: 10 ~50.6%, 20 ~0.83%, 30 ~0.014%
- master-test P80: 20 ~27.8%, 30 ~3.23%, 40 ~0.30%

Forced battlefield-reading pause indicated passive40/2s + HP10% recovers most attention cost without making passive-only play viable in normal 3P/4P pressure samples.

---

# Exact next work boundary
1. Device test public `v022.html`.
2. Verify nickname and class carousel on Android landscape.
3. Verify swipe does not accidentally trigger combat or page scroll.
4. Inspect geometric character proportions/weapon readability for all 5 classes.
5. Inspect all 30 skill icons; icons should communicate actual mechanic at a glance.
6. Check six skill cards fit/read well on short landscape screens.
7. Check button-based play settings usability.
8. Configure +1/+2/+3 AI with custom classes/positions and verify actual combat lineup.
9. Verify battle screen has no old class selector or bottom prototype settings box.
10. Implement v0.23 waiting-room UX for FRIEND / LINK / RANDOM.
11. Do not fake remote connectivity; actual networking follows as a separate implementation boundary.
12. Continue full-run progression simulation before freezing passive/HP/combo coefficients.

## Still unresolved / not production-frozen
- passive/HP/combo final coefficients,
- result-board final metrics,
- final E/X values and tier structure,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- DUO/TRIPLE/FULL sync implementation,
- Lv26/Lv31 coefficients,
- server authority model,
- room lifecycle / invite link contract / random matchmaking queue,
- disconnect/rejoin/state reconciliation.

---

# New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `V022_LOBBY_IMPLEMENTATION_REPORT.md`
4. `V021_IMPLEMENTATION_REPORT.md`
5. `V020_IMPLEMENTATION_REPORT.md`
6. `DESIGN_DECISIONS.md`
7. `V019_IMPLEMENTATION_REPORT.md`
8. `V018_IMPLEMENTATION_REPORT.md`
9. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
10. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
11. `SKILL_PLAN_LV6_31.md`
12. `TIER_PRESSURE_GRAMMAR_V1.md`
13. `PRESSURE_RECIPES_V1.md`
14. `SIMULATION_METHOD.md`
15. `NEXT_WORK.md`
