# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- current N3 device-smoke candidate HEAD: `f9e824eac87cc2fe39d80a75b345ce5aa8f574ce`

Last fully closed checkpoint:
- **v0.38 Slice C / larger-party event kernel FULL PASS**
- branch `timing-defense-cloudflare-v038-slice-c-pass-20261022`
- HEAD `cbcddf35443ff901b4a30dd6621da5a984335fb5`

Active candidate:
- **v0.39 N3 Option B authority**
- implementation branch `timing-defense-cloudflare-v039-n3-authority`
- health `0.39-cf.1`
- automated-live validation **PASS** on watched HEAD `201ac36ac8ec97a3e033976cdea13c3fd2fe03c6`
- automation checkpoint `timing-defense-cloudflare-v039-automation-pass-20261022`
- remaining gate: one Samsung Browser N3 presentation/input smoke only

Preserved checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`
- v0.36 automation PASS: `timing-defense-cloudflare-v036-automation-pass-20261021`
- v0.36 Slice A full PASS: `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- v0.37 Slice B full PASS: `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- v0.38 automation PASS: `timing-defense-cloudflare-v038-automation-pass-20261022`
- v0.38 Slice C full PASS: `timing-defense-cloudflare-v038-slice-c-pass-20261022`
- v0.39 N3 automation PASS: `timing-defense-cloudflare-v039-automation-pass-20261022`

Read first:
- `NEXT_WORK.md`
- `CLOUDFLARE_V039_N3_AUTOMATION_PASS_2026-10-22.md`
- `N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`
- `CLOUDFLARE_V038_SLICE_C_PASS_2026-10-22.md`

---

# Closed Cloudflare gates
- v0.31/v0.32 waiting-room parity — PASS
- v0.33 Stage 1 authority — PASS
- v0.34 render/remote projectile parity — PASS
- v0.35 reconnect / Team Shop / Stage 2 — PASS
- v0.36 N1/N2 + Lv6 authority — FULL PASS
- v0.37 Stage 3 + BRUTE — FULL PASS
- v0.38 larger-party/event-delivery kernel — FULL PASS

## v0.36 frozen parity
N1 exact EXP:
- NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28.

N2:
`AI damage × (1 + (stage - 1) * 0.035)`.

Lv6 authority:
- Knight +12% damage
- Rogue 55% second dagger after +55 ms
- Tank +30% knockback
- Archer up to two strict-line 52% secondary hits
- Mage up to three nearby 50% splash hits

## v0.37 Stage 3 frozen contract
- 12 enemies / 980 ms
- GRUNT 44% / RUNNER 34% / BRUTE 22%
- BRUTE base HP 900 / speed .040 / wall 180 / knock resist .38 / armor 1 / reward 14
- ordinary Stage 3 BRUTE HP 1247 under existing HP rules
- Stage 3 clear -> Team Shop
- Stage 4 blocked

## v0.38 Slice C closure
Event kernel:
- 512 retained authoritative events
- per-WebSocket `eventRunId` + `eventCursor`
- monotonic `event-batch`
- state snapshots do not depend on the old fixed 24-event tail
- explicit `event-gap`
- resume/eventFloor historical replay suppression preserved

Automation PASS:
- SERVER 28/28
- v0.36 client regression PASS
- v0.37 client regression PASS
- event client PASS
- larger-party simulation PASS
- FINAL PASS

Party/device coverage:
- 3H / 4H / 2H+2AI / 3H+1AI
- host reconnect
- READY/START
- Stage 1 -> Shop -> Stage 2
- >24-event delivery without silent loss
- final Samsung Browser 4H smoke user-confirmed PASS

---

# N3 — OPTION B APPROVED / FROZEN / v0.39 AUTOMATION PASS
Frozen contract:
- combo 5 / 10 / 20 / 30 / every +10 after 30
- exact raw-equivalent max budgets 60 / 90 / 150 / 210
- Rogue 2/3/4/5 daggers
- Knight 67/33
- Tank 60/20/20
- Archer 70/30 strict line
- Mage 55/15/15/15
- deterministic remainder-safe allocation
- no EXP / charge / combo / ordinary crit / recursive class skill / recursive N3
- normal armor, kill, kill coin and contribution attribution
- frozen boss scalars apply
- generic N3 knockback uses NORMAL-equivalent base
- Tank retains independently-authoritative knockback identity

Automated-live validation on public Cloudflare via GitHub Actions + Playwright Chromium:
- V038 FULL REGRESSION PASS
- N3 SERVER **57/57 PASS**
- N3 CLIENT PASS
- N3 4H STRESS PASS
- FINAL PASS

Four-human stress validates one synchronized Lv6 Rogue combo-30 wave:
- 4 ordinary hits
- 4 Lv6 second daggers
- 20 N3 daggers
- 28 combat events per observer
- no event-gap
- contiguous event IDs
- all combos -> 30

The first Actions attempt timed out because the Playwright runner passed timeout options in the wrong argument position. This was a runner defect, not an N3/game failure. The corrected runner completed full PASS.

Current candidate adds only an opt-in `?n3smoke=1` helper for the final device presentation gate. It automatically arms the host to Lv6/combo29 once combat has a monster; normal access is unaffected.

Stage 4 remains blocked until the v0.39 Samsung Browser presentation smoke passes.

---

# Validation policy going forward
Automated validation should not be delegated to the user when GitHub Actions can execute it.

Default sequence:
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`.

Actions evidence should retain health response, page body, browser log and screenshot on failure/success as configured.

---

# Following bounded work
1. Close v0.39 with one N3 Samsung Browser presentation/input smoke.
2. Stage 4 SHIELD / armor.
3. Stage 5–6 boss + FLYER + authoritative Y geometry.
4. Stage 7–9 mixed-roster stress.
5. Stage 10 final boss/result.
6. Lv11/16/21 authority with forced-level deterministic tests.

## Deferred UX
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred as one shared responsive-safety layer.

## Governance
No unapproved numerical change. Continue:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
