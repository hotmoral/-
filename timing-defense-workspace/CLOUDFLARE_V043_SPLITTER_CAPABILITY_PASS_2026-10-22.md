# Cloudflare v0.43 — SPLITTER Capability PASS

Date: 2026-10-22 KST

## Exact checkpoint
- branch: `timing-defense-cloudflare-v043-splitter-pass-20261022`
- HEAD: `d1bac2effbd866aa221d55829678f959bc099b82`
- public health: `0.43-cf.1`
- live validation run: `39705143877`
- live validation job: `119583316125`

## Scope
This slice implements SPLITTER as a stage-number-independent authoritative child-spawn capability. It does **not** author a production stage recipe and does **not** freeze final economy or monster tuning.

Frozen structural behavior:
`parent death -> exactly two deterministic children -> children never split again`

## Provisional capability-test anchors
Parent:
- HP 420
- speed `.065`
- wall damage 100
- knock resistance `.82`
- armor `1.00`
- size `1.00`

Children:
- HP 120
- speed `.115`
- wall damage 40
- knock resistance `.82`
- armor `1.00`
- size `.62`
- Y offsets `-.018 / +.018`

Reward accounting used only to make the sandbox executable:
- parent 4
- child 2 each
- package total 8

**This 4+2+2 split is PROVISIONAL TEST ACCOUNTING ONLY. It is NOT the production reward/economy freeze.** Production reward allocation remains a later campaign-calibration decision.

## Closed authoritative semantics
- parent death inserts exactly two children at the parent-death timestamp,
- child IDs come deterministically from authoritative `nextMonsterId`,
- child ordering and Y offsets are deterministic,
- children persist `canSplit=false` and generation 1,
- killing a child never recursively spawns more children,
- parent and both children share a stable `splitterPackageId`,
- parent/child movement and wall timing use explicit SPLITTER metadata rather than GRUNT fallback,
- child combat geometry uses explicit size `.62` and knock resistance `.82`,
- simultaneous parent deaths allocate deterministic child IDs/order,
- spawned children prevent premature stage-clear evaluation,
- Rogue N3 can kill the parent and deterministically retarget the first child on its next delayed dagger,
- Tank N3 uses child knock metadata correctly,
- reconnect reconstruction preserves child movement, wall time and non-recursive state,
- event IDs remain monotonic,
- no extra immediate split event is inserted; split metadata is attached to the existing damage event so earlier hit/EXP/Lv6/N3 annotation contracts remain intact.

## Validation hardening
The first candidate diagnostic reported 13/14 because the wall-identity test advanced a room to the slower parent wall time, which legitimately removed the faster child first, then attempted to query the removed child. This was a **self-test sequencing defect**, not a production-code or numerical failure.

The test was corrected to validate parent and child wall identity in independent deterministic actors. Production monster values were not patched in response.

A later metadata-only hardening made the parent kill event and both children share the same package attribution. This did not change combat or balance.

## Candidate validation
Final candidate CI after attribution hardening: **SUCCESS**.

Deterministic diagnostics:
- Monster Capability Foundation: **22/22 PASS**
- v0.39 N3: **57/57 PASS**
- v0.40 SHIELD: **11/11 PASS**
- v0.41 FLYER: **10/10 PASS**
- v0.42 CHARGER: **17/17 PASS**
- v0.43 SPLITTER: **14/14 PASS**

## Live validation
GitHub Actions run `39705143877` validated the exact public deployment.

PASS evidence:
- exact deployment marker `0.43-cf.1`
- foundation **22/22 PASS**
- N3 **57/57 PASS**
- SHIELD **11/11 PASS**
- FLYER **10/10 PASS**
- CHARGER **17/17 PASS**
- SPLITTER **14/14 PASS**
- root-loader smoke PASS
- V038 FULL REGRESSION PASS
- N3 CLIENT PASS
- N3 4H STRESS PASS
- **FINAL PASS**

## Device-smoke decision
No Samsung Browser smoke is required for this slice because SPLITTER has not yet been inserted into a visible authored encounter and no final split VFX/presentation has been introduced.

## Closure
v0.43 SPLITTER authoritative child-spawn capability is **FULL PASS**.

Next bounded capability:
**SUPPORTER dynamic movement-speed aura**, still stage-number-independent.

The SUPPORTER implementation must not approximate dynamic aura movement in a way that introduces timestamp drift. Aura topology/crossing semantics must be audited before implementation.
