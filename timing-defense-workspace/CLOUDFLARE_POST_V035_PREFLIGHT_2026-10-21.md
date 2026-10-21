# Timing Defense — Post-v0.35 Cloudflare Migration Preflight

Date: 2026-10-21 KST  
Status: **PREFLIGHT COMPLETE / IMPLEMENTATION NOT STARTED**

## 0. Baseline

Validated Cloudflare v0.35 baseline:
- deployment/checkpoint HEAD: `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- preserved branch: `timing-defense-cloudflare-v035-pass-20261021`
- health: `0.35-cf.7`

This preflight does not modify the validated deployment branch or combat coefficients.

Audited sources include:
- `timing-defense-v011/v013-1.js`
- `timing-defense-v011/v013-2.js`
- `timing-defense-v011/v016-core.js`
- `timing-defense-v011/v017-ux-ai.js`
- `timing-defense-v011/v018-auto-combo.js`
- `timing-defense-cloudflare-poc/src/index.js`
- `timing-defense-cloudflare-poc/src/v035-entry.js`
- `timing-defense-v011/v035-cloudflare-v2.js`
- `timing-defense-v011/v035-stage2-input-guard.js`
- `timing-defense-v011/v035-authoritative-results.js`
- `DESIGN_DECISIONS.md`
- `SKILL_PLAN_LV6_31.md`
- `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
- `TIER_PRESSURE_GRAMMAR_V1.md`
- `PRESSURE_RECIPES_V1.md`

---

# 1. Stage 3–10 legacy contract audit

The next Cloudflare expansion must use the existing 10-stage prototype contract first. The later S/E/X pressure grammar and concrete 2/3/4-player recipes are **candidate future encounter data**, not authorized production values and must not be substituted into this migration slice.

## 1.1 Exact legacy stage plan

| Stage | Count | Base gap | Composition rule | Special |
|---|---:|---:|---|---|
| 1 | 8 | 1120 ms | GRUNT 100% | already PASS |
| 2 | 10 | 1040 ms | GRUNT 62% / RUNNER 38% | already PASS |
| 3 | 12 | 980 ms | GRUNT 44% / RUNNER 34% / BRUTE 22% | first new monster type |
| 4 | 13 | 940 ms | GRUNT 36% / RUNNER 26% / SHIELD 20% / BRUTE 18% | armor enters |
| 5 | 10 | 1080 ms | non-final: G27/R21/S20/B18/F14; final forced BRUTE | checkpoint boss |
| 6 | 14 | 900 ms | G27/R21/S20/B18/F14 | FLYER active |
| 7 | 15 | 860 ms | G20/R22/S20/F18/B20 | mixed roster |
| 8 | 16 | 820 ms | G20/R22/S20/F18/B20 | mixed roster |
| 9 | 17 | 780 ms | G20/R22/S20/F18/B20 | mixed roster |
| 10 | 18 | 760 ms | non-final mixed; final forced BRUTE | final boss |

Abbreviations: G=GRUNT, R=RUNNER, S=SHIELD, B=BRUTE, F=FLYER.

## 1.2 Monster contracts not yet present in Cloudflare v0.35

Current Cloudflare `TYPES` contains only GRUNT and RUNNER. Legacy additional types:

- BRUTE: HP 900, speed .040, wall damage 180, knock resist .38, armor 1.00, reward 14.
- SHIELD: HP 540, speed .057, wall damage 120, knock resist .62, armor .72, reward 10.
- FLYER: HP 225, speed .100, wall damage 70, knock resist .90, armor 1.00, reward 7.

Legacy HP scaling:
- base stage multiplier: `1 + (stage-1)*0.13`.
- current ordinary non-boss experiment: additional `×1.10`.
- ordinary +10% does **not** apply to boss monsters.

Boss contract:
- Stage 5 final monster: forced BRUTE, visual scale 1.25, HP multiplier ×2.7.
- Stage 10 final monster: forced BRUTE, visual scale 1.42, HP multiplier ×4.0.
- boss wall damage multiplier: ×1.45.
- boss knockback scalar: ×0.40.
- Rogue dagger damage against bosses: ×0.70.

## 1.3 Movement/geometry consequence

Cloudflare v0.35 currently models monster X as time-derived and Y as effectively fixed.

That is sufficient for GRUNT/RUNNER Stage 1–2 presentation, but not sufficient for the full future authority model:
- RUNNER has a small vertical oscillation locally.
- FLYER has meaningful time-derived vertical oscillation.
- Archer line collision and Mage radius/outer-ring selection depend on authoritative X/Y geometry.

Therefore FLYER must not be added as a cosmetic-only moving object while server skill targeting still uses a fixed Y. Before Stage 5/6, introduce a deterministic `yAt(monster, at)` or equivalent authoritative geometry function.

## 1.4 Stage flow hardcoding that must be generalized

Current Cloudflare v0.35 has explicit Stage-2 assumptions in multiple layers:
- server `STAGES` supports only 1 and 2,
- server `spawn()` only knows Stage-2 composition beyond GRUNT,
- `checkEnd()` ends the run at Stage 2,
- client `enterStagePresentation()` ignores stages other than 2,
- `v035-stage2-input-guard.js` is hardcoded to Stage 2,
- authoritative result board captures `stage2-clear`,
- final result semantics are coupled to `stage2-clear`.

Required generalized state grammar:
- Stages 1–9 clear -> authoritative Team Shop.
- shop READY/NEXT -> future `stage-starting` -> `intro` -> `combat` for `stage+1`.
- Stage 10 clear -> final run clear/result state.
- Game over remains terminal at any stage.

Do not duplicate Stage-specific client guards for Stage 3, 4, etc. Replace Stage-2-only transition logic with one `stage N` invariant path.

---

# 2. Larger-party audit

## 2.1 What already generalizes correctly

Existing room authority already has useful four-slot foundations:
- `MAX_SLOTS = 4`,
- fixed slot IDs P1–P4,
- one host session,
- same-session reconnect returns the same slot,
- READY is per human,
- `canStart()` requires at least 2 humans and every human READY,
- shop READY is checked across all humans,
- host-only START/NEXT,
- run players are built from authoritative human participants,
- result rows are slot ordered and support up to four total participants,
- render party stores local + up to three remote/AI visual actors.

Supported intended TEAM combinations remain bounded by the frozen TEAM rule:
- 2 humans + 0–2 AI,
- 3 humans + 0–1 AI,
- 4 humans + 0 AI.

## 2.2 AI FILL semantic watch item

Current server treats configured `aiFill` positions as occupied slots before human join. Humans do not dynamically displace an AI filler.

This is structurally valid for fixed-position AI selection, but it is weaker than the design phrase “human slots take conceptual priority over AI filler.”

Do not silently change this behavior in the first larger-party patch. Treat dynamic AI displacement as a separate product decision.

## 2.3 Event-volume risk

Current Durable Object stores at most 48 events and public snapshots expose only the last 24.

That was sufficient for the validated 2-human Stage 1–2 slice, but 3–4 participants plus:
- human timing hits,
- passive hits,
- AI hits,
- penetration/splash/multi-dagger secondary hits,
- delayed skill effects,

can produce substantially more visual events per snapshot window.

Before 4-player Lv6+ validation, event delivery must be made loss-resistant. Preferred direction:
- keep monotonic event IDs,
- add action/cast identity (`actionId`, source slot, hit index),
- expose enough events since the client event floor rather than relying only on a small fixed tail,
- preserve reconnect historical-event suppression.

Do not solve this by giving clients damage authority.

---

# 3. Lv6+ multiplayer authority audit

## 3.1 Implementation truth

`SKILL_PLAN_LV6_31.md` defines Lv6/11/16/21/26/31 design contracts.

The actual legacy playable implementation audited in `v016-core.js` explicitly implements the **Lv6/Lv11/Lv16/Lv21 block**. Lv26/Lv31 names are present in the roadmap/unlock list, but their final playable combat consequences are not implemented in that v0.16 authority baseline.

Therefore:
- Lv6–21 = migration/parity candidates.
- Lv26/Lv31 = **design-only for this migration preflight; do not invent implementation**.

## 3.2 Ownership classification

Legend:
- `P` = presentation-only.
- `C+S` = client may predict presentation/input, but server must confirm/own combat consequence.
- `S` = server-authoritative consequence.

### Knight

| Level | Effect | Ownership |
|---|---|---|
| 6 | +12% blade-wave damage | S |
| 6 | projectile size +25% | P |
| 11 | extra penetrations / 85% secondary damage | C+S target selection + damage |
| 16 | PERFECT-containing attack +18% damage | S |
| 16 | +20% knockback | S |
| 21 | heavy +20% damage / up to 3 extra penetrations | C+S |
| 21 | giant crescent presentation | P |
| 26 | no penetration decay / escalating knockback | S, design-only now |
| 31 | double broad blade wave / major knockback | C+S, design-only now |

### Rogue

| Level | Effect | Ownership |
|---|---|---|
| 6 | second dagger 55% | C+S multi-hit |
| 11 | +6 percentage-point class crit | S RNG |
| 16 | PERFECT recovery 390 -> 312 ms | client predicts cadence, server must validate attack eligibility |
| 21 | heavy = center + four 45% follow-ups | C+S multi-hit |
| 26 | PERFECT secondary tracking dagger 45% | S target selection/damage, design-only now |
| 31 | 8 rapid tracking daggers | S scheduled multi-hit, design-only now |

No same-target dagger cap. Boss dagger scalar remains 0.70.

### Tank

| Level | Effect | Ownership |
|---|---|---|
| 6 | shockwave visual width +30% | P in current legacy implementation |
| 6 | knockback +30% | S |
| 11 | wall incoming damage -10%, non-stacking across tanks | S shared-wall rule |
| 16 | PERFECT gives 80 shield / 3 s refresh | S timed shared-wall state |
| 21 | broad heavy multi-target impact / ~×2 knockback | C+S |
| 26 | 1.5 s, -25% movement zone | S timed monster movement modifier, design-only now |
| 31 | battlefield shockwave + 250 shield / 6 s | S, design-only now |

### Archer

| Level | Effect | Ownership |
|---|---|---|
| 6 | up to 2 additional straight-line penetrations | S geometric target selection |
| 11 | projectile speed +25% | P under current event-at-action server model |
| 11 | base damage +10% | S |
| 16 | PERFECT armor ignore / no penetration decay | S |
| 21 | heavy 100% + 65% + 65% triple shot | C+S |
| 26 | +2 penetration / preserve rear damage | S, design-only now |
| 31 | unlimited line penetration / armor ignore | S, design-only now |

Frozen rule: Archer must remain strict straight-line; no bending, seeking, or off-line retarget.

### Mage

| Level | Effect | Ownership |
|---|---|---|
| 6 | 50% splash | S radius target selection/damage |
| 11 | radius +35%, splash 60% | S |
| 16 | delayed 55% outer-ring resonance, center excluded | S scheduled delayed effect |
| 21 | heavy +20% damage / ×1.6 radius | S |
| 21 | slower/larger orb visual | P under current server model |
| 26 | chain explosions to up to 2 targets | S, design-only now |
| 31 | three-stage collapse / chained secondary explosions | S scheduled effects, design-only now |

## 3.3 Required server primitives before full Lv6–21 port

1. authoritative player class available in run combat logic,
2. skill milestone lookup derived from authoritative level,
3. one action/cast identity across primary and secondary hits,
4. deterministic geometric target helpers (line, radius, ring),
5. scheduled-effect queue included in Durable Object `nextDueAt()`,
6. authoritative wall-shield state + expiry,
7. server-side action cadence validation for Rogue Lv16,
8. skill event metadata sufficient for client VFX without client damage authority.

---

# 4. Pre-existing numerical parity findings — explicit decision gate

These were discovered while auditing the next slice. They are not automatically patched because numerical changes follow the project's explicit-decision governance.

## N1. Heavy-tier EXP mismatch

Legacy exact EXP table:
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 10
- HEAVY+ 14
- GREAT 18
- SUPER 23
- CRITICAL 28

Current Cloudflare server effectively uses:
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 8
- HEAVY+ 8
- GREAT 12
- SUPER 18
- CRITICAL 28

This was not obvious in the Stage 1–2 device gate, but it changes level timing and therefore becomes a direct skill-unlock dependency from Stage 3 onward.

**Recommendation:** classify as a parity defect and restore the exact legacy EXP table before enabling Lv6+ authority. Requires explicit approval because it changes deployed numerical behavior.

## N2. AI stage damage scaling missing in Cloudflare

Legacy AI launch behavior scales AI damage by:
`1 + (stage-1)*0.035`.

Current Cloudflare AI authority applies `baseDamage(tier)` without this stage multiplier.

Difference is small at Stage 2 but grows through Stage 10.

**Recommendation:** restore exact legacy AI stage scaling before Stage 3–10 expansion. Requires explicit approval because it changes deployed numerical behavior.

## N3. Combo milestone attack rewards are not server-authoritative in Cloudflare

Legacy experimental v0.18 includes extra milestone attack budgets at PERFECT combo milestones (60 / 90 / 150 / 210 raw-equivalent tiers, with recurring max-tier milestones after 30).

Cloudflare currently implements the persistent combo damage percentage but not those extra milestone attack consequences.

This feature is explicitly experimental/not production-frozen and can materially increase 3–4-player event volume.

**Recommendation:** do not silently port it inside the Stage 3 patch. Keep it as a separate explicit decision after the event-delivery kernel is generalized.

---

# 5. Reuse / adapter / replace classification

## REUSE AS IS
- Durable Object room ownership and persistence,
- WebSocket hibernation transport,
- session/slot reconnect identity,
- host identity,
- human READY gates,
- server-owned coin/ranks/purchases,
- v0.35 purchase pending UX,
- v0.34 monster smoothing baseline,
- authoritative result-row source,
- event-floor reconnect suppression,
- frozen class identity and existing approved presentation.

## REUSE WITH ADAPTER
- `beginStage(stage, at)` -> data-driven Stage N,
- `processAt(at)` -> all stage plans + scheduled skill effects,
- `checkEnd(at)` -> stages 1–9 shop / stage 10 final clear,
- monster serialization -> all five monster types + boss metadata,
- client Stage-2 intro/input guard -> generic Stage N invariant,
- result capture -> generic final-clear status,
- shop UI -> repeated stages without Stage-2 assumptions,
- remote projectile events -> action/cast grouping for multi-hit skills.

## REPLACE / GENERALIZE REQUIRED
- two-entry `STAGES` map,
- GRUNT/RUNNER-only server `TYPES`,
- Stage-2-only spawn selection,
- fixed-Y assumption before FLYER/geometry-sensitive skills,
- Stage-2-only client transition guard,
- Stage-2-only final result status,
- fixed short event tail as the only multi-client VFX delivery mechanism,
- generic class-agnostic human damage authority once Lv6+ unlocks.

## DEFER / NOT IN FIRST IMPLEMENTATION SLICE
- S/E/X 50-stage pressure grammar as live data,
- literal `PRESSURE_RECIPES_V1` team scaling,
- Lv26/Lv31 combat implementation,
- dynamic AI displacement by joining humans,
- production persistence/security/anti-cheat redesign,
- responsive phone/aspect-ratio safety layer,
- any new numerical balance tuning.

---

# 6. Recommended bounded implementation order

Do not attempt Stage 3–10 + 4-player + all skills in one patch.

## Slice A — parity/authority foundation (next implementation, after explicit N1/N2 decision)

Scope:
- no new stage,
- preserve validated Stage 1–2 flow,
- establish generic class/skill authority primitives,
- implement and API-test the existing **Lv6** consequences for all five human classes,
- add action/cast IDs and multi-hit event metadata,
- preserve current client prediction as presentation only,
- no Lv11+ yet,
- no 3–4-player expansion test yet.

Why first:
- Stage 3 is where natural progression begins to make Lv6 materially relevant,
- this isolates skill-authority defects from encounter-generalization defects,
- rollback is exact v0.35 PASS.

Acceptance:
- forced/server test states at Lv5 vs Lv6 prove only the intended effect changes,
- HP/death/knockback/wall state comes only from server,
- remote client sees identical authoritative result,
- no duplicate skill damage from local prediction,
- v0.35 Stage 1–2 device regression remains clean.

## Slice B — Stage 3 only, two-human first

After Slice A PASS:
- Stage 2 clear enters normal Team Shop instead of terminating,
- NEXT launches Stage 3,
- Stage 3 exact legacy count/gap/composition,
- add BRUTE server authority,
- Stage 3 clear returns to Team Shop,
- Stage 4 remains blocked/not-supported in this slice,
- two-human device test first; AI/larger-party validation separate.

This is the cheapest proof that Stage N generalization is real rather than another Stage-specific patch.

## Slice C — larger-party baseline on already-supported stages

Before combining full skills and later stages:
- 3 humans,
- 4 humans,
- 2 humans + 2 AI,
- 3 humans + 1 AI,
- READY/host/reconnect/shop/result consistency,
- event-volume instrumentation.

No balance tuning from this test.

## Slice D — Lv11–21 authority and Stage 4–10 in bounded groups

Suggested grouping after earlier gates:
- Stage 4: SHIELD + armor path,
- Stage 5–6: boss + FLYER + authoritative Y geometry,
- Stage 7–9: mixed roster stress,
- Stage 10: final boss + final clear/result,
- Lv11/16/21 authority introduced before natural progression reaches each milestone, with forced-level API tests independent of stage progression.

Lv26/Lv31 remain out of scope until a separate implementation contract is approved.

---

# 7. Device-validation matrix

| Gate | 2H | 3H | 4H | 2H+2AI | 3H+1AI |
|---|---:|---:|---:|---:|---:|
| waiting/READY/host | regression | required | required | required | required |
| reconnect same slot | regression | required | required | required | required |
| Team Shop all-human READY | regression | required | required | required | required |
| Stage N synchronized intro | required | later | later | later | later |
| same monster HP/deaths/base | required | later | later | later | later |
| remote timing projectile | regression | required | required | required | required |
| multi-hit skill authority | required by class | required after event-kernel PASS | required after event-kernel PASS | required with AI skills later | required with AI skills later |
| final result rows | regression | required | required | required | required |
| historical event replay after reconnect | regression | required | required | required | required |

Class skill observation matrix for Lv6 authority Slice A:
- Knight: +12% server damage; visual enlargement only presentation.
- Rogue: exact 55% second dagger, same target allowed.
- Tank: +30% server knockback.
- Archer: strict-line additional penetrations only; no off-line retarget.
- Mage: 50% server splash with authoritative target set.

---

# 8. Rollback / checkpoint plan

- Never move the preserved `timing-defense-cloudflare-v035-pass-20261021` branch.
- Start next implementation from exact PASS HEAD `b8cb477...`.
- Use a new implementation branch; do not develop directly on the watched deployment branch.
- Before each device candidate, preserve the previous PASS checkpoint.
- Move `timing-defense-cloudflare-do-poc` only to an audited candidate HEAD.
- Any regression in Stage 1–2 authority, reconnect, shop, result, CHARGE or projectile parity -> immediately classify and rollback to v0.35 PASS while fixing off-line.

---

# 9. Preflight conclusion

The architecture is viable for the next migration, but broad Stage 3–10 implementation is **not yet authorized by this preflight**.

The next implementation dependency order is:

1. explicit decision on numerical parity findings N1/N2,
2. Slice A — generic skill-authority foundation + Lv6 on validated Stage 1–2,
3. Slice B — Stage 3 only,
4. larger-party baseline,
5. Lv11–21 + Stage 4–10 in bounded groups,
6. separate later decision for Lv26/Lv31 and experimental combo milestone attacks.

No balance recommendation is made by this preflight.