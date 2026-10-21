# Timing Defense — Cloudflare v0.37 Slice B PASS

Date: 2026-10-21 KST  
Status: **FULL PASS**

## 0. Exact checkpoint

Validated deployment / preserved checkpoint:
- watched deployment branch at validation: `timing-defense-cloudflare-do-poc`
- exact validated HEAD: `08af6e1e9f399ad13369990dcc452f012ddda1fa`
- preserved PASS branch: `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- health/version family: `0.37-cf.1`

v0.36 Slice A checkpoint remains preserved separately at `c540119f469cff6795a74a3867c26f4c67de9071`.

## 1. Frozen Slice B scope

Only Stage 3 was added.

Exact Stage 3 contract:
- 12 enemies
- 980 ms spawn gap
- GRUNT 44%
- RUNNER 34%
- BRUTE 22%
- BRUTE base contract: HP 900 / speed .040 / wall damage 180 / knock resist .38 / armor 1.00 / reward 14
- existing stage HP factor retained: `1 + (stage - 1) * 0.13`
- existing ordinary non-boss `x1.10` HP experiment retained
- Stage 3 ordinary BRUTE HP = 1247

Flow:
- Stage 1 clear -> Team Shop
- Stage 2 clear -> Team Shop
- host NEXT -> Stage 3
- Stage 3 clear -> Team Shop
- Stage 4 blocked in both server and candidate UI

No new numerical balance decision was introduced.

## 2. Pre-deployment defects caught by code audit

Two integration assumptions were corrected before final validation:

1. Stage 3 scheduler self-test initially expected `combatAt` as the first due time. The existing Durable Object contract correctly schedules `startAt` first, then `combatAt`, then combat/spawn work. The test was corrected rather than changing production scheduling semantics.

2. The validated Stage 1-2 wall loop closes over a GRUNT/RUNNER-only type table. Without an adapter, BRUTE wall contact could have fallen back to GRUNT wall damage 90. Stage 3 now handles BRUTE wall contact authoritatively with base damage 180 and the existing DEF reduction rule. Deterministic validation includes BRUTE 180 and DEF-rank-4 result 162.

## 3. Automated validation evidence — PASS

User-executed Samsung Browser one-click validation suite reported:

- `SERVER · PASS · 21/21`
- `V036 CLIENT REGRESSION · PASS · 4/4`
- `STAGE3 CLIENT · PASS · 6/6`
- `MULTICLIENT · PASS · 10/10`
- `FINAL · PASS`

Coverage includes:
- v0.36 N1/N2 + Lv6 regression,
- Stage 3 plan/count/gap/composition thresholds,
- BRUTE movement/HP/reward/knockback/AI scale,
- BRUTE authoritative wall damage + DEF path,
- Stage 2 -> Shop -> Stage 3,
- Stage 3 -> Shop,
- Stage 4 server block,
- generic Stage 2/3 client transition/input behavior,
- two real WebSocket human clients through Stage 1 -> Shop -> Stage 2 -> Shop -> Stage 3 -> Shop,
- reconnect and shared-state behavior.

## 4. Final Samsung Browser smoke — PASS

Final device evidence was a ~90.5 s Samsung Browser recording using the single-device simulated-human peer harness.

Observed:
- local human remained the intended host/player,
- `SIM-PC` remained a separate human ARCHER participant,
- Stage 1 and Stage 2 proceeded through Team Shop normally,
- Stage 3 intro and combat became interactive,
- BRUTE appeared with the existing large BRUTE body/silhouette rather than a GRUNT fallback,
- multiple Stage 3 monsters including BRUTE rendered and moved without obvious disappearance, teleport storm, flicker or canvas corruption,
- timing attacks remained usable during Stage 3,
- Stage 3 cleared into Team Shop,
- final shop displayed `STAGE 3 CLEAR` / `STAGE 3 COMPLETE`,
- both host and `SIM-PC` were separately present and READY,
- `STAGE 4 LOCKED` was visibly enforced.

Exact combat numbers were not re-verified by eye because they were already covered by deterministic/live automated validation.

## 5. Closure decision

**v0.37 Slice B / Stage 3 = FULL PASS.**

Do not reopen Stage 3 numerical values without the normal numerical governance process.

N3 remains unresolved and mandatory for future explicit discussion:
- combo-milestone extra attacks are neither implemented nor discarded,
- do not silently port/remove/freeze/rebalance N3.

## 6. Next bounded boundary

Next slice is **Slice C — larger-party baseline**, before Stage 4.

Planned combinations:
- 3 humans,
- 4 humans,
- 2 humans + 2 AI,
- 3 humans + 1 AI.

Primary goals:
- READY / host START / Team Shop NEXT across larger parties,
- reconnect identity,
- result/participant consistency,
- event-volume/loss resistance under more concurrent human/AI/passive/Lv6 events,
- automated multi-client harness expansion first,
- manual device work reduced to one final render/input smoke.

Stage 4 SHIELD remains out of scope until Slice C closes.