# Timing Defense — Cloudflare v0.36 Slice A Automated Validation

Date: 2026-10-21 KST  
Status: **CF.3 HARNESS IMPLEMENTED / PUBLIC RUN PENDING**

## Baseline
- preserved v0.35 PASS: `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- v0.36 implementation branch: `timing-defense-cloudflare-v036-lv6-authority`
- Cloudflare watched branch candidate HEAD: `abb2d428df546c257181278ba6bd0814e0471c93`
- expected health after deployment: `0.36-cf.3`

## Validation-policy correction
Do not require a human to visually verify every numerical/class consequence on a phone.

For Slice A, divide validation into:
1. deterministic server simulation,
2. actual client-layer simulation,
3. live two-WebSocket Durable Object simulation,
4. one final short real-device smoke test only for browser/render/touch behavior that cannot be proven from code.

This is the default direction for later Stage 3–10 / 3–4-player / Lv11–21 work as well.

---

## Layer 1 — deterministic server self-test
Endpoint after cf.3 deploy:
`GET /api/diagnostics/v036-slice-a`

Implementation:
`timing-defense-cloudflare-poc/src/v036-selftest.js`

Important property: the test creates isolated in-memory room state but calls the **actual patched `TimingDefenseRoom.prototype` methods**. It does not duplicate the combat implementation as a separate simulator and does not mutate production Durable Object rooms.

Checks:
- N1 HEAVY+ exact EXP = 14 through real `playerAction`,
- duplicate `seq` rejected,
- N2 AI stage multiplier through real `applyDamage`: Stage1 100 / Stage2 103 / Stage10 132 for a 100-raw probe under exact JS rounding,
- Knight Lv5 100 -> Lv6 112,
- Rogue primary 100 + exactly one delayed 55 secondary with shared `actionId` and hitIndex 0/1,
- Tank Lv6 knockback ratio = 1.30,
- Archer exactly two aligned 52% secondary line hits while an off-line monster is excluded,
- Mage exactly three 50% nearby splash hits while a far monster is excluded,
- Stage1 -> shared Team Shop -> all-human READY -> Stage2 starting contract.

Any failed check makes the endpoint return HTTP 500 and `ok:false`.

---

## Layer 2 — actual client-layer self-test
Page:
`/v036-client-selftest.html`

This page loads the real `v036-lv6-authority.js` into a controlled browser fixture.

Checks:
- in network mode, Rogue's legacy local Lv6 secondary projectile is removed so it cannot execute local `visualImpact()` and transiently mutate local HP/kill/coin presentation,
- v0.35 resume event floor is adopted by the new Lv6 secondary-VFX layer,
- historical skill event below the floor is not rendered,
- a fresh skill event above the floor is rendered once,
- receiving the same state snapshot again does not enqueue a duplicate secondary VFX.

This specifically covers the two integration defects found by code audit after cf.1.

---

## Layer 3 — live two-client Durable Object simulation
Page:
`/v036-multiclient-sim.html`

One browser tab creates **two real WebSocket clients** against the deployed Cloudflare Durable Object.

Automated flow:
1. create room,
2. connect host + guest,
3. both READY,
4. host START,
5. wait for synchronized Stage1 combat,
6. host forced to Lv6 through candidate-only debug endpoint,
7. real Rogue primary + delayed secondary attack,
8. verify both clients receive the same authoritative `actionId/hitIndex/damage` event set and exactly one secondary,
9. resend same seq and require `stale-seq`,
10. call real resume endpoint and require empty historical event list + sufficient event floor,
11. close/reconnect guest and require same slot/run,
12. automatically clear Stage1,
13. require shared Team Shop,
14. both shop READY,
15. host NEXT,
16. require synchronized Stage2 state.

The simulator cleans up the temporary room afterward.

---

## One-click aggregate suite
Page:
`/v036-validation-suite.html`

It executes in order:
1. server diagnostics endpoint,
2. client-layer self-test in a same-origin hidden iframe,
3. live multi-client simulator in a same-origin hidden iframe,
4. final aggregate PASS/FAIL.

Target use: one automated suite run should replace repeated manual class-by-class device testing.

---

## What still requires a real device
Only a short smoke test remains after all automated layers PASS:
- Samsung/Chrome page loads the correct current asset version,
- touch/timing input actually responds,
- no obvious projectile duplication/flicker/visual corruption,
- Stage1 -> Shop -> Stage2 is visibly usable.

A real phone is **not** the primary oracle for exact EXP/damage/knockback/secondary target selection.

## N3 governance
N3 = experimental combo-milestone extra attacks.

N3 remains **deferred but mandatory future discussion**. It must not be silently added, removed, frozen or rebalanced as part of this automation work.
