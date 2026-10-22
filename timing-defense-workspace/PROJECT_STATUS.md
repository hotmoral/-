# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Current validated deployment
Primary architecture: **Cloudflare Workers + Durable Objects event-driven multiplayer**.

- public: `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- validated HEAD: `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health: `0.45-cf.1`
- last executable checkpoint: **v0.45 SIEGER FULL PASS**
- checkpoint: `timing-defense-cloudflare-v045-sieger-pass-20261022`
- live run/job: `39725993894` / `119649887564`

Read first:
1. `NEXT_WORK.md`
2. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
3. `MONSTER_CAPABILITY_CONTRACT_V1.md`
4. `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
5. `CLOUDFLARE_V045_SIEGER_CAPABILITY_PASS_2026-10-22.md`
6. `SKILL_PLAN_LV6_31.md`
7. `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`
8. `V016_IMPLEMENTATION_REPORT.md`
9. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
10. `DESIGN_DECISIONS.md`

---

# Closed combat/network foundations
- v0.36: exact EXP table, AI stage multiplier, Lv6 class skill authority.
- v0.38: 512-event cursor kernel, reconnect, 3H/4H/mixed-party flow.
- v0.39: N3 product contract frozen and authoritative.
- Stage1–3 are regression fixtures only, not final campaign recipes.

## Lv6 authoritative summary
- Knight +12% damage.
- Rogue second dagger +55ms at 55%.
- Tank +30% knockback.
- Archer up to 2 strict-line additional hits at 52%.
- Mage up to 3 nearby splash hits at 50%.

## N3 frozen summary
- milestones 5 / 10 / 20 / 30 / every +10 thereafter.
- budgets 60 / 90 / 150 / 210.
- no generated EXP / charge / combo / ordinary crit / recursive skill / recursive N3.
- normal armor / kill / kill coin / contribution and frozen boss scalars retained.

---

# Campaign direction
Do **not** reconstruct legacy Stage4→10 as production content.

Production direction remains approximately 50 stages with:
- tier identities,
- S/E/X pressure grammar,
- 2/3/4-player composition scaling,
- re-authored monster combinations,
- deterministic simulation/calibration,
- explicit production-number freeze only after report/discussion/decision.

---

# Monster Capability V1 — MECHANICAL FOUNDATION COMPLETE
All nine ordinary archetypes now have server-authoritative mechanical foundations:
GRUNT / RUNNER / BRUTE / SHIELD / FLYER / CHARGER / SPLITTER / SUPPORTER / SIEGER.

Checkpoint chain:
- Foundation `68882c2013d1d35aaedbf12e5725fde377795044` — 22/22 PASS.
- v0.40 SHIELD `7a3bdf0134e38f36383b52d4bc69b40147b0e5ad` — FULL PASS.
- v0.41 FLYER `7a68ba6d78b3ac8611c815f582e24e871a947f03` — FULL PASS.
- v0.42 CHARGER `57e6fc1bb4ef388b1d1de5403b60866c48b5c07a` — FULL PASS.
- v0.43 SPLITTER `d1bac2effbd866aa221d55829678f959bc099b82` — FULL PASS.
- v0.44 SUPPORTER `b2dc0269e144d9fa13ee490bba36ae93839f6a20` — FULL PASS.
- v0.45 SIEGER `ea22cc279603394dc4b439b6fdbb0c83aff4299a` — FULL PASS.

Current monster capability coefficients remain **PROVISIONAL — NOT PRODUCTION BALANCE FROZEN** unless separately approved.

Bosses remain a separate capability-composition layer.

## v0.45 SIEGER closure
- authoritative standoff arrival.
- persistent ADVANCE/WINDUP/COOLDOWN; FIRE is instantaneous.
- repeated ranged wall shots keep SIEGER alive.
- team DEF applies.
- knockback can force reposition/fresh windup.
- SUPPORTER affects approach only.
- reconnect, late replay and monotonic events validated.
- SIEGER selftest **20/20 PASS**.
- prior complete browser/WebSocket regression PASS.

The first live gate failure was only a stale workflow expectation of 18 checks while the final suite contained 20. No gameplay/numerical change was required.

---

# Player Skill Authority Review — COMPLETE
Canonical review:
`PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`

Recovered six-milestone roadmap:
`Lv6 / Lv11 / Lv16 / Lv21 / Lv26 / Lv31`.

## Classification
### Lv6
**FROZEN+AUTHORITATIVE** in current Cloudflare.

### Lv11 / Lv16 / Lv21
**LEGACY-REFERENCE / exact parity candidates.**

Evidence:
- actually implemented/deployed in legacy v0.16,
- exact formulas mirrored by v7 simulation,
- old Cloudflare preflight explicitly classified Lv6–21 as migration candidates,
- old handoff explicitly planned later server-side migration of Lv6/Lv11/Lv16/Lv21 multiplayer effects.

They are not current Cloudflare authority and are not automatically re-frozen by this review.

### Lv26
**DESIGNED-NOT-AUTHORITATIVE.**
Explicit class concepts/proposed coefficients exist, but no playable authority implementation existed.

### Lv31
**UNRESOLVED for production implementation.**
Final class identities exist, but multiple damage/geometry/timing details remain underspecified.

Legacy `v016-core.js` has no `v016Has(26)` or `v016Has(31)` combat branch.

## Why this matters for 50-stage calibration
Under the old accepted EXP rule, Skilled players commonly reached Lv21 by Stage10. Therefore full ~50-stage calibration using only current Lv6 server authority would materially under-model player power.

Do not infer final Lv26/Lv31 reach timing yet; final EXP/campaign pacing remains to be calibrated.

---

# Active decision gate
No Lv11+ code should be written until the parity strategy is explicitly approved.

Recommended default:
- adopt exact v0.16 **Lv11/Lv16/Lv21** combat formulas as parity candidates,
- port them server-authoritatively as three bounded slices P1/P2/P3,
- keep **Lv26/Lv31** out of implementation until their contracts are reviewed against the new 9-monster roster and ~50-stage goals,
- do not production-freeze new Lv26/Lv31 numbers now.

Proposed slices:
- **P1 Lv11:** Knight penetration85%; Rogue +6pp crit; Tank wall -10% nonstack; Archer +10% damage; Mage radius×1.35/splash60%.
- **P2 Lv16:** Knight PERFECT ×1.18 damage/×1.20 knock; Rogue recovery390→312 with server cadence validation; Tank 80 shield/3s; Archer PERFECT armor-ignore/100% penetration; Mage delayed180ms 55% outer ring.
- **P3 Lv21:** Knight heavy×1.20/up to3 extra penetration; Rogue 100%+4×45%; Tank broad heavy/×2 knock; Archer strict-line 100+65+65; Mage heavy×1.20/radius×1.60.

After P1–P3 closure, explicitly review Lv26/Lv31 before final late-campaign calibration.

---

# Validation policy
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`.

# Governance
No unapproved numerical change:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
