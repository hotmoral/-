# Timing Defense — Headless Simulation Method

## Purpose
Use renderer-free models to validate numerical balance, progression, team-role value and encounter structure faster than manual play.

Simulation is diagnostic. It is not a replacement for feel/UX testing and never self-authorizes a numerical live balance patch.

## Governance
Required order:
1. model / simulate / observe,
2. identify intentional specialization vs abstraction/artifact vs implementation defect vs real balance defect,
3. report,
4. discuss,
5. make explicit decision,
6. only then patch numerical live gameplay.

Implementation-fidelity defects that violate an already frozen rule may be fixed without treating them as balance changes.

---

# Frozen semantic decisions

## Timing profiles
- Novice: N45 / G45 / P10.
- Average: N25 / G55 / P20.
- Skilled: N10 / G50 / P40.
- Expert: N3 / G32 / P65.

Average cadence reference:
- normal 1.14 s,
- heavy 1.68 s.

Skilled cadence reference:
- normal 1.04 s,
- heavy 1.54 s.

## Archer
Straight-line geometric penetration only.
- no homing,
- no automatic next-enemy chain,
- no post-launch off-line retargeting,
- trajectory is locked at launch,
- if the intended target disappears, only a hitbox intersecting the locked path can be hit.

## Tank
Team-specialist. Fresh-run solo Stage-10 parity is not required.

## Rogue / bosses
- no same-target dagger hit cap,
- boss dagger damage scalar = 0.70,
- boss knockback scalar = 0.40.

## EXP
EXP remains tied to timing attack results/events. Faster-clearing classes are allowed to level differently because they may perform fewer attack events.

---

# Current live prototype facts used when mirroring combat

Current exact implementation basis: **v0.16**, live source HEAD:
`b8b823742bd5fb16026090045cd347feb0f9275e`.

Important runtime facts:
- class-specific projectile lifetime remains part of combat timing,
- local base recovery is 390 ms after hit resolution,
- Rogue Lv16 PERFECT-containing attack changes that recovery to 312 ms,
- live AI attack intervals differ by class,
- live AI uses lower fixed timing-result probabilities than a real Skilled human,
- monsters move continuously toward the wall,
- current Stage 1–10 live spawner caps simultaneous active monsters at 10,
- current ordinary targeting starts from the nearest target,
- Archer is the exception after launch: its path is locked and no longer follows generic target retargeting.

When a simulation intentionally differs from current live behavior because it validates future multiplayer or future Lv26/Lv31 mechanics, that difference must be stated explicitly.

---

# Simulation history

## v1 — role separation
Validated basic class identities:
- Rogue vs durable normal,
- Archer vs line pack,
- Mage vs dense cluster,
- Tank vs wall pressure,
- Knight as stable generalist.

## v2 — Stage 1–10 + run shop
Added current campaign/shop economy and candidate Lv6–21 skills.

Deliberate volume: 39,600 core runs plus targeted diagnostics.

Key decisions:
- permissive Archer auto-chain was rejected as a model artifact,
- Tank solo weakness was accepted as specialization,
- EXP/attack-count coupling was retained.

Report: `BALANCE_SIM_REPORT_V2.md`.

## v3 — Average→Skilled mastery curve
Nine interpolation points plus accuracy-only diagnostics.

Deliberate volume: 27,500 runs.

Key result:
- mastery response is strong and desirable,
- cadence is a real skill axis in addition to judgment accuracy.

Report: `BALANCE_SIM_REPORT_V3_SKILL_CURVE.md`.

## v4 — team-composition / co-op role isolation
2/3/4-player compositions, identical seeded waves, duplicate-class checks and targeted Lv21 role diagnostics.

Deliberate volume: 13,780 runs.

Key result:
- Tank has real defensive team utility,
- Rogue has durable-normal team value,
- Archer and Mage remain line-vs-density distinct,
- Knight remains a stabilizing generalist,
- old unscaled Stage 1–10 waves saturate at 3–4 players.

Report: `BALANCE_SIM_REPORT_V4_TEAM.md`.

## v5 — Tier Pressure Grammar
Moved above exact combat to validate long-run encounter variety.

Pressure families:
- S Swarm,
- E Elite/Heavy,
- X Special/Mixed.

Five representative 50-stage prototypes were generated.
Across 250 stages:
- 1-pattern 40.8%,
- 2-pattern 43.6%,
- 3-pattern 15.6%.

Geometry, internal ratios and timing are authored as gameplay data.

Files:
- `TIER_PRESSURE_GRAMMAR_V1.md`
- `BALANCE_SIM_REPORT_V5_PRESSURE_GRAMMAR.md`
- `pressure_grammar_sim_v1.py`

## v6 — concrete current-roster recipes
v6 converted S/E/X into GRUNT/RUNNER/BRUTE/SHIELD/FLYER recipes.

Candidate Swarm counts:
- line = 8 / 11 / 14 for 2P/3P/4P,
- cluster = 7 / 10 / 13,
- scatter = 9 / 12 / 16.

X scaling primarily adds role-bearing anchors/disruption rather than blanket HP.

E is represented as an effective durability budget, not a literal single-monster HP instruction.

Candidate P95 four-second spawn burst:
- 2P = 11,
- 3P = 15,
- 4P = 18.

The approximate conservative one-human/current-AI-like bound produced:
- 2P Average/Skilled = 100 / 100%,
- 3P = 88.4 / 94.9%,
- 4P = 68.3 / 83.0%.

That model preceded exact playable Lv11–21 and contained approximations, so v7 supersedes it for formula-sensitive interpretation.

Files:
- `PRESSURE_RECIPES_V1.md`
- `BALANCE_SIM_REPORT_V6_CONCRETE_RECIPES.md`
- `pressure_recipe_sim_v1.py`

## v7 — exact v0.16 formula re-run
v7 exists because the playable Lv6–21 implementation is now concrete enough to mirror rather than approximate.

Reproducible model:
`combat_exact_v016.py`.

### Modeling boundary
The campaign-bound matrix remains a conservative diagnostic:
- one local human uses Average or Skilled,
- remaining slots use current live AI cadence/result quality,
- AI teammates do not receive the local human Lv6–21 skill block,
- fixed-level snapshots Lv6/Lv11/Lv16/Lv21 are used instead of pretending a future 50-stage multiplayer economy is already frozen,
- S/E/X recipes come from `PRESSURE_RECIPES_V1.md`.

Therefore v7 is a **pressure / skill-step bound**, not a final all-human co-op clear-rate target.

### Exact local formulas mirrored
- Knight: +12%; Lv11 85% penetration; Lv16 +18% PERFECT damage/+20% knockback; Lv21 +20% heavy and up to 3 extra penetrations.
- Rogue: 55% second dagger; +6%p native crit; exact 390→312 ms recovery; Lv21 four 45% follow-ups.
- Tank: Lv6 knockback; Lv11 -10% wall damage; true 80 shield / 3 s expiry-refresh; Lv21 full-damage Ground Impact and ×2 heavy knockback.
- Archer: +10%; life ÷1.25; locked straight-line collision; pre-Lv16 52% secondary penetration; Lv16 armor-ignore/100% preserved penetration on PERFECT; Lv21 100/65/65 triple shot.
- Mage: 50→60% splash; +35% radius; 55% outer-ring center-excluding Resonance; Lv21 +20% heavy / ×1.6 radius / slower orb.

### Implementation artifact discovered during extraction
Initial v0.16 still inherited generic `nearestMonster()` retargeting if an Archer target died before impact. This could bend side arrows off-line.

That contradicted an already frozen semantic rule, so it was classified as an **implementation defect**, fixed first, and only the corrected formula was used for final v7 interpretation.

Fix commit:
`b8b823742bd5fb16026090045cd347feb0f9275e`.

### Run volume
Campaign-bound:
- Lv6 snapshot: 2,100 runs,
- Lv11: 2,100,
- Lv16: 2,100,
- Lv21 stable snapshot: 3,500,
- independent Lv21 local-class matrix: 2,500,
- total = **12,300**.

Additional targeted validation:
- durable-normal duels = **50,000**,
- static line/cluster geometry trials = **20,000**.

### Main fixed-level result
3P Average / Skilled:
- Lv6 36.2 / 50.7%,
- Lv11 49.6 / 68.0%,
- Lv16 55.6 / 77.8%,
- Lv21 81.6 / 96.4%.

4P:
- Lv6 22.7 / 33.0%,
- Lv11 33.3 / 42.7%,
- Lv16 33.7 / 49.3%,
- Lv21 52.8 / 73.6%.

2P is near saturation in this pressure/AI-bound model.

T4 Crossfire remains the strongest current stress identity:
- 3P Lv21 = 63.3 / 89.3%,
- 4P Lv21 = 33.0 / 59.0%.

### Role checks
Durable-normal Lv21 mean TTK Average / Skilled:
- Rogue 20.54 / 15.92 s,
- Archer 25.44 / 19.76,
- Knight 33.45 / 25.14,
- Mage 39.98 / 31.31,
- Tank 42.67 / 33.47.

Rogue therefore retains its intended specialist niche despite lower broad wave-clear results.

Archer/Mage geometry after trajectory locking:
- Average line: Archer 16.53 vs Mage 21.40 s,
- Average dense cluster: Archer 20.03 vs Mage 19.71,
- Skilled line: Archer 12.16 vs Mage 15.53,
- Skilled dense cluster: Archer 15.08 vs Mage 15.59.

The line identity is strong. Dense-pack separation is close and requires real rendered play evidence before any balance conclusion.

### v7 balance interpretation
No numerical class rebalance is authorized.

Watch items only:
- Archer broad Lv21 campaign throughput,
- 2P saturation,
- Mage/Archer dense-pack separation on the real battlefield,
- future true-human teammate cadence.

Report: `BALANCE_SIM_REPORT_V7_V016_EXACT.md`.

---

# Deterministic comparison principle
When comparing classes, compositions or pressure candidates, reuse the same seeds / authored stage grammar so only the tested variable changes.

## Metrics by layer

### Combat/campaign
- clear/fail,
- wall HP / wall hits,
- clear time,
- target-type TTK / kill share,
- total/skill damage,
- shield generation/absorption,
- level/EXP timing,
- attack count/cadence,
- shop ranks where applicable.

### Encounter grammar / recipe
- 1/2/3-pattern stage counts,
- S/E/X occurrence and pressure shares,
- pair/triple internal ratios,
- early/mid/late/final placement,
- formation geometry,
- repeated signatures,
- short-window spawn density,
- total stage population,
- threat-index envelope,
- role-opportunity distribution.

---

# Current next extension
Formula extraction/re-simulation is no longer the blocker; v7 completed it.

The current blocker is **rendered/device behavior validation** of v0.16:
- six-slot HUD fit,
- visually straight Archer paths,
- Tank shield lifecycle,
- Rogue barrage readability,
- Mage Resonance center exclusion,
- Lv21 VFX readability under dense pressure.

Fix implementation/readability defects if found. Do not numerically rebalance from first impressions.

After that closes:
1. use exact v7 formulas for further 2/3/4-player pressure calibration,
2. combine simulation with targeted real-play evidence,
3. report/discuss before changing class or encounter numbers,
4. then choose the next major block: Lv26/Lv31, wider tier authoring, multiplayer sync/economy, or permanent/meta progression.
