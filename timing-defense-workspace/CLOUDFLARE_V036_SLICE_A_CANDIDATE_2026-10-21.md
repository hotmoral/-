# Timing Defense — Cloudflare v0.36 Slice A Candidate

Date: 2026-10-21 KST
Status: **IMPLEMENTED / WATCHED BRANCH TRIGGERED / LIVE & DEVICE VALIDATION PENDING**

## Baseline
Validated v0.35 PASS checkpoint:
`b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`

Preserved branch:
`timing-defense-cloudflare-v035-pass-20261021`

Implementation branch:
`timing-defense-cloudflare-v036-lv6-authority`

Implementation branch HEAD:
`ce3ea7f168fce26f6e76556cd73fea9fb08dce99`

Cloudflare watched branch:
`timing-defense-cloudflare-do-poc`

Current watched HEAD:
`8b1e2890ea582bd1ddaeae89157a82500adf40a0`

The preserved v0.35 PASS branch is untouched.

## Effective implementation scope
Relative to v0.35 PASS:
- add `timing-defense-cloudflare-poc/src/v036-entry.js`
- update Wrangler main to `src/v036-entry.js`
- add `timing-defense-v011/v036-cloudflare.html`
- add `timing-defense-v011/v036-lv6-authority.js`
- add candidate-only `timing-defense-v011/v036-debug-controls.js`
- watched branch additionally carries `V036_SLICE_A_DEPLOY_TRIGGER.md` as deployment evidence.

The watched loader and implementation loader use cache generation `cf0362` and load the same v0.36 execution layers. No Stage 3 content is enabled.

## Approved parity fixes
### N1
Restore exact legacy timing EXP:
NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28.

### N2
Restore exact legacy AI damage multiplier:
`1 + (stage - 1) * 0.035`.

### N3 — mandatory future discussion
Not implemented. N3 is **not discarded**. The experimental combo-milestone extra attacks remain a required future discussion/review item and may not be silently ported, removed, frozen or rebalanced.

## Lv6 authority implemented
Server now owns the consequences below when the player was already Lv6 before the action:
- Knight: exact legacy additive +12% attack multiplier component.
- Rogue: second dagger at 55%, scheduled +55 ms, same-target allowed with nearest-target fallback if the original target disappeared.
- Tank: exact +30% knockback multiplier component.
- Archer: up to two additional strict-line hits at 52% damage.
- Mage: up to three nearby splash targets at 50% damage.

An action identity is attached to primary/secondary events. Secondary events include hit indices and skill metadata for presentation.

## Prediction/authority split
- Server owns HP, deaths, knockback and all Lv6 secondary damage.
- Existing local projectile prediction remains presentation only.
- Rogue's existing local delayed-dagger visual is retained and the authoritative local Rogue secondary event is not drawn a second time.
- Archer/Mage secondary presentation is driven from authoritative skill events because the network primary-hit override bypasses their old local secondary resolver.
- Remote human secondary effects are rendered from authoritative events.

## Candidate-only validation control
Host-only endpoint:
`POST /api/room/<CODE>/debug-level`

Payload:
`{ session, slot?, level: 5|6 }`

Test UI is visible only when the game URL contains:
`v036debug=1`

It exposes `LV5` / `LV6` buttons to the host after a run exists. This is validation instrumentation, not a production feature, and should be removed/disabled after Slice A closure.

Recommended candidate URL:
`https://timing-defense-do-poc.sktjsek.workers.dev/?v036debug=1&fix=cf0362`

## Internal source/contract checks completed
- new server entry syntax PASS,
- new client authority-presentation syntax PASS,
- loader inline syntax PASS,
- isolated mock contract harness PASS:
  - N1 HEAVY+ returns 14 EXP rather than previous Cloudflare 8,
  - N2 Stage 2 100-raw AI example follows the exact JS legacy multiplier expression (`Math.round(100*1.035)` -> 103 under JS floating arithmetic),
  - Knight Lv5 100 vs Lv6 112 normal hit,
  - Rogue Lv6 100 + delayed 55 secondary,
  - Tank Lv6 exact 1.30 knockback multiplier,
  - Archer Lv6 two aligned 52% penetrations,
  - Mage Lv6 three 50% nearby splash hits.

These are source/contract checks, not substitutes for real Durable Object/API/device validation.

## Live validation boundary
The model-side external fetch environment cannot access the `workers.dev` host, so live health/deployment confirmation must be made from the user device/browser.

Expected health:
- `version: 0.36-cf.1`
- `n1: legacy-heavy-xp-restored`
- `n2: legacy-ai-stage-damage-scaling-restored`
- `n3: deferred-explicit-discussion-required`

Before PASS:
1. verify public health markers,
2. validate N1/N2 against real Durable Object state,
3. use host Lv5/Lv6 controls to validate each class boundary,
4. two-human Stage 1–2 regression,
5. confirm no duplicate authoritative damage from local prediction,
6. confirm reconnect/shop/result behavior remains v0.35-clean.

Do not start Slice B / Stage 3 until Slice A closes.
