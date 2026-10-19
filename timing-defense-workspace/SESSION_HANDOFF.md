# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations

- Public repository: `hotmoral/-`
- Persistent planning/balance branch: `timing-defense-workspace`
- Live playable branch: `timing-defense-live-v011`
- Live prototype: `v0.15`
- Play URL: https://timing-defense-v011.onrender.com/v015.html

The workspace branch is the source of truth for design decisions, balance interpretation, simulation reports and session handoff. The live branch is separate so analysis/documentation changes do not deploy automatically.

## Current playable state

Five classes are playable: Knight / Rogue / Tank / Archer / Mage.
Current live growth implementation contains the Lv6 skill layer only.
Planned unlock levels are:

`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`

Stage prototype is 1–10. Run EXP, coins and shop upgrades reset each run.

## Frozen class-role decisions

- Knight: generalist / stable frontline / penetration / strong heavy.
- Rogue: fast multihit / crit / high-HP normal target execution.
- Tank: team-specialist / knockback / wall protection / battlefield control. Fresh-run solo Stage-10 parity is NOT required.
- Archer: straight-line geometric penetration only. No retargeting, homing or automatic next-enemy chaining.
- Mage: density specialist / area burst / chained explosions.

## Frozen boss interaction rules

- Rogue dagger hits have no same-target hit cap.
- Boss dagger damage scalar: `0.70` starting value.
- Boss knockback scalar: `0.40` starting value.
- These are tuning values, but they are NOT to be changed automatically from simulation output.

## Frozen progression philosophy

- EXP stays tied to timing attack results/events.
- Faster-killing classes are not compensated merely because they perform fewer attacks and therefore may gain EXP more slowly.
- `Skilled` simulation profile means approximately `NORMAL 10% / GOOD 50% / PERFECT 40%`, plus modestly faster attack commitment than Average.
- Strong Skilled performance is acceptable because player mastery is intended to materially reduce difficulty.
- The user expects players to reach Skilled consistency relatively quickly; preserve room for that mastery progression.

## Balance governance

**Never patch solely because a simulation exposes a large performance gap.**

Required order:

`simulate → identify cause/model artifact/intentional specialization → report → discuss with user → explicit decision → only then patch live gameplay`

## Simulation status

### v1
Role-scenario validation established the intended identity split:
- Rogue strongest vs durable normal targets.
- Archer strongest in aligned line packs.
- Mage strongest in dense clusters.
- Tank strongest in wall preservation/control.
- Knight stable generalist.

### v2
Added Stage 1–10 + shop simulation. Important discoveries:
- permissive Archer auto-chain penetration badly overestimated Archer, so penetration semantics were explicitly frozen to straight-line geometry.
- Tank's poor solo result was discussed and accepted as team specialization.
- EXP/attack-count coupling was discussed and intentionally retained.

Report: `BALANCE_SIM_REPORT_V2.md`

### v3
Average→Skilled mastery curve confirmed a strong but plausible player-skill progression.

Main endpoint:
- Skilled = N10 / G50 / P40 with modestly faster cadence.
- Knight / Archer / Mage become highly reliable Stage-10 solo performers.
- Rogue remains a specialist rather than a general solo clearer.
- Tank solo result remains non-normative.
- No live change was applied.

Report: `BALANCE_SIM_REPORT_V3_SKILL_CURVE.md`

### v4 — latest completed validation
Team-composition / co-op role validation was run as a report-only role-isolation model.

Important modeling boundary:
- primary Stage 1–10 comparisons use current unscaled wave counts/gaps.
- all human teammates use the same named proficiency in a comparison.
- sync bonuses are not modeled yet.
- multiplayer shop/economy ownership is not frozen, so v4 intentionally excludes run-shop upgrades and should not be compared 1:1 to v2/v3 absolute clear rates.

Deliberate v4 volume: **13,780 runs**.

Key results:
- **Tank team utility is real under meaningful wall pressure.** In hard Lv21 diagnostics it reduced net wall HP loss through mitigation, shield refresh and knockback even while killing fewer enemies.
- **Rogue team niche is real.** In several 3-player mixes Rogue took about 39–42% of BRUTE/SHIELD kills while representing only one third of the team.
- **Archer and Mage remain geometrically distinct.** In long-line packs Archer produced about 66.8% of pair damage; in dense clusters Mage produced about 58.4%.
- **Knight remains a strong generalist/stabilizer** and is often the safest third member.
- **Current Stage 1–10 waves saturate at 3–4 players.** At Average, 9/10 unique 3-player teams were already 100% clear; all unique 4-player teams were 100%. At Skilled all 3-player and 4-player unique compositions were 100% clear.
- Therefore current waves cannot be treated as final 3–4 player balance targets. Co-op pressure scaling must eventually be designed explicitly.
- Duplicate diagnostic flagged **Knight + Knight** as unusually strong at Average (~93% clear versus ~51–57% for mixed Knight pairs), but this is NOT a balance verdict because the headless Knight Lv11 penetration geometry is still approximate. Re-test after exact playable collision implementation.

No live balance value was changed from v4.

Report: `BALANCE_SIM_REPORT_V4_TEAM.md`

## Current skill-design candidate through Lv21

See `SKILL_PLAN_LV6_31.md` for complete Lv6–31 plan.

Through Lv21:
- Knight: Lv6 +12% blade-wave damage; Lv11 penetration; Lv16 PERFECT enhancement; Lv21 large heavy blade wave.
- Rogue: Lv6 second dagger 55%; Lv11 +6%p class crit; Lv16 PERFECT cycle reduction; Lv21 five-dagger heavy.
- Tank: Lv6 width/knockback enhancement; Lv11 wall incoming damage -10%; Lv16 80 shield / 3 s refresh non-stack; Lv21 broad heavy shockwave.
- Archer: Lv6 straight-line penetration; Lv11 speed +25% and damage +10%; Lv16 PERFECT armor-ignoring preserved penetration; Lv21 triple shot.
- Mage: Lv6 burst; Lv11 larger/stronger burst; Lv16 outer-ring resonance excluding original center target; Lv21 greater arcane orb.

These remain candidate implementation values, not authority to deploy without the normal discussion/implementation boundary.

## Exact next work boundary

Do NOT immediately alter live numerical balance.

The next design question is now **co-op team-size pressure philosophy**, because current Stage 1–10 waves are saturated by 3–4 players.

Before building a v5 pressure model, discuss and choose whether additional human players should primarily create:
1. more enemies,
2. tougher enemies,
3. a mix of count + HP,
4. or additional elite/special threats while keeping ordinary enemies readable.

Also still unresolved:
- multiplayer shop/economy ownership and timing,
- duplicated-class policy,
- exact network/sync attack bonus implementation.

After co-op pressure philosophy is agreed, build v5 simulation first. Report → discuss → decide before any live difficulty patch.

## New-session read order

1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `DESIGN_DECISIONS.md`
4. `SKILL_PLAN_LV6_31.md`
5. `BALANCE_SIM_REPORT_V2.md`
6. `BALANCE_SIM_REPORT_V3_SKILL_CURVE.md`
7. `BALANCE_SIM_REPORT_V4_TEAM.md`
8. `SIMULATION_METHOD.md`
9. `NEXT_WORK.md`
