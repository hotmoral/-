# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 real-game waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**

Read before execution:
1. `CLOUDFLARE_DO_MIGRATION_DECISION_2026-10-21.md`
2. `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`
3. `CLOUDFLARE_V031_V032_PARITY_PASS_2026-10-21.md`
4. `CLOUDFLARE_V033_STAGE1_PASS_2026-10-21.md`
5. `CLOUDFLARE_V034_RENDER_CANDIDATE_2026-10-21.md`
6. `PROJECT_STATUS.md`
7. `V034_MULTIPLAYER_RENDER_SMOOTHING_REPORT.md`

Public Cloudflare URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Current candidate:
- branch: `timing-defense-cloudflare-v034-render`
- implementation: `c78765b2c29b1ab0812e64c6de7a8ca3b379c2cc`
- deployment trigger: `adc6709d51e9b076498c7c26e172478d24d9f797`

## Immediate execution group — v0.34 render parity validation
No numerical balance changes. No Team Shop or Stage 2 yet.

Validate Android + PC:
1. existing room / READY / START still works,
2. both clients still see identical authoritative monster HP / BASE HP / EXP / charge / clear,
3. monster motion is smooth and does not regress into visible snapping/jitter,
4. remote human projectile is visible on the other client,
5. AI/passive projectile presentation is visible where applicable,
6. presentation projectiles never apply local gameplay damage,
7. local projectile arrival immediately produces visual hit feedback,
8. server-confirmed local hit does not replay the same flash/particle a second time,
9. authoritative damage number / HP change still comes from server state,
10. Samsung Browser remains usable.

The v0.34 candidate intentionally keeps the v0.33 Durable Object combat authority unchanged.

## Closure rule
Close v0.34 only when:
- public deployment is confirmed,
- Android + PC device validation passes,
- no duplicate damage or duplicate impact presentation is observed,
- v0.33 authority parity remains intact,
- canonical docs are synchronized.

A v0.34 PASS authorizes only the next migration slice: **v0.35 reconnect / Team Shop / Stage 2 parity**.

## Following slice — only after v0.34 PASS
Port legacy v0.35 semantics:
- same-session/reload recovery,
- Stage 1 -> Team Shop,
- authoritative coin/ranks/purchases,
- purchase READY lock/unlock,
- all-human shop READY gate,
- host-only NEXT,
- synchronized future Stage 2 start,
- Stage 2 GRUNT/RUNNER authoritative combat,
- bounded Stage 2 clear.

Then device-test reconnect in Stage 1 / Team Shop / Stage 2.

## Frozen governance
Do not numerically patch attack damage, monster HP, passive interval, combo coefficients, EXP, shop costs, knockback, stage count/gaps or class balance during migration without the established measure/report/discuss/explicit-decision workflow.

## Current truth boundary
Safe:
- Cloudflare v0.31/v0.32 waiting-room parity device-PASS,
- Cloudflare v0.33 authoritative Stage 1 device-PASS,
- legacy v0.34 smoothing/projectile behavior device-PASS,
- legacy v0.35 reconnect/shop/Stage-2 code exists and passed local/API integration checks.

Not yet safe:
- Cloudflare v0.34 render parity PASS,
- Cloudflare v0.35 parity,
- Stage 3–10 multiplayer,
- full Lv6+ multiplayer authority,
- final numerical freeze.
