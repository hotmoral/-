# Timing Defense — Cloudflare v0.39 N3 Automation PASS

Date: 2026-10-22 KST  
Status: **AUTOMATED LIVE VALIDATION PASS / FINAL DEVICE PRESENTATION SMOKE PENDING**

## Exact validated deployment
- watched branch: `timing-defense-cloudflare-do-poc`
- exact automated-live validated HEAD: `201ac36ac8ec97a3e033976cdea13c3fd2fe03c6`
- N3 implementation code is unchanged from the preceding v0.39 authority candidate; this HEAD adds/fixes only the live-validation workflow around that deployed candidate.
- health: `0.39-cf.1`

Preserve automation checkpoint as:
`timing-defense-cloudflare-v039-automation-pass-20261022`

## GitHub Actions live runner
Public GitHub Actions now performs the browser validation that previously required the user to open the validation URL manually.

Workflow:
`.github/workflows/timing-defense-v039-live-validation.yml`

Execution model:
1. wait for Cloudflare health to report the expected version,
2. install/launch real headless Chromium through Playwright,
3. open the deployed `v039-validation-suite.html`,
4. execute real browser JS + WebSocket tests against the public Durable Object deployment,
5. require `FINAL · PASS`,
6. upload health text, full page text, browser console log and validation screenshot as evidence.

Validated GitHub Actions run:
- run id `39686204069`
- job id `119520775498`
- all workflow steps PASS.

The first runner attempt failed before validation completion because `page.waitForFunction` was called with the timeout object in the argument position, leaving Playwright's default 30 second timeout. That was a runner defect, not a game/N3 failure. The call was corrected to use the proper third-argument options position and failure evidence capture was hardened.

## Automated validation evidence
Live Chromium output:
- `V038 FULL REGRESSION · PASS`
- `N3 SERVER · PASS · 57/57`
- `N3 CLIENT · PASS`
- `N3 4H STRESS · PASS`
- `FINAL · PASS`

### N3 deterministic coverage
All five classes were tested at forced combo milestones:
- 5
- 10
- 20
- 30
- 40

Validated contract:
- exact milestone budgets 60 / 90 / 150 / 210,
- 30+ remains capped at 210,
- Rogue 2 / 3 / 4 / 5 daggers,
- Knight 67/33 geometry,
- Tank 60/20/20 geometry,
- Archer strict-line 70/30 geometry,
- Mage 55/15/15/15 geometry,
- deterministic remainder-safe allocation,
- no EXP from N3,
- no extra charge from N3,
- no combo increment from N3,
- no ordinary proc crit,
- no recursive Lv6 skill trigger,
- no recursive N3,
- unused secondary budget is not redirected to primary,
- kill / coin / cumulative kill-coin / contribution attribution works,
- Rogue boss damage scalar 0.70 works for the covered assertion,
- Tank Lv6 knockback identity remains ×1.30 relative to Lv5 for N3,
- Lv6 Rogue ordinary secondary dagger and N3 five-dagger milestone coexist without duplication.

### Four-human worst-case burst coverage
Automated live WebSocket stress forces four Lv6 Rogue humans to combo 29, then sends simultaneous PERFECT actions.

Expected per synchronized milestone wave:
- ordinary hit: 4 events,
- Lv6 Rogue second dagger: 4 events,
- N3 Rogue milestone daggers: 20 events,
- total combat events: 28.

PASS requires all four clients to receive the complete sequence with:
- correct N3 milestone = 30,
- correct N3 budget = 210,
- no `event-gap`,
- monotonic contiguous post-floor event IDs,
- all four authoritative combos become 30.

This live stress PASS confirms the v0.38 cursor/batch event kernel handles the previously unsafe >24-event N3 burst case.

## Current closure boundary
v0.39 N3 authority is **automation PASS**, not yet full device PASS.

Remaining manual gate is presentation/input only:
- one short Samsung Browser smoke,
- no numerical rechecking,
- verify an N3 milestone burst is visibly coherent and does not cause obvious duplicate projectiles, flicker, Canvas corruption or input blockage.

After that smoke passes, preserve a full v0.39 PASS checkpoint and move to Stage 4 SHIELD / armor.

## Validation policy going forward
Do not ask the user to manually open automated validation pages when a public GitHub Actions live browser runner can cover the gate.

Default sequence:
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`.
