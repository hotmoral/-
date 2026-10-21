# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**
6. v0.36 Slice A N1/N2 + Lv6 authority — **PASS**
7. v0.37 Slice B Stage 3 + BRUTE — **PASS**
8. v0.38 Slice C larger-party/event kernel — **FULL PASS**
9. v0.39 N3 authority — **FULL PASS**

Exact v0.39 full-PASS checkpoint:
- branch `timing-defense-cloudflare-v039-pass-20261022`
- HEAD `911dd67cf4bb4d704e050f8e3a92cb34c48deb3a`
- health `0.39-cf.1`

## Active slice — v0.40 Stage 4 SHIELD / armor
Preflight:
`CLOUDFLARE_V040_STAGE4_PREFLIGHT_2026-10-22.md`

Exact legacy contract recovered:
- Stage 4 = 13 enemies / 940 ms
- GRUNT 36% / RUNNER 26% / SHIELD 20% / BRUTE 18%
- SHIELD base HP 540 / speed .057 / size 1.08 / wall 120 / knock resist .62 / armor .72 / reward 10
- Stage 4 ordinary SHIELD HP = 826 under existing approved HP rules
- armor applies as `round(incoming * .72)` with minimum 1

Required integration work:
- exact SHIELD server authority
- add SHIELD metadata to Lv6 and N3 geometry/knock paths so it cannot fall back to GRUNT
- Stage 3 shop -> Stage 4
- Stage 4 clear -> Team Shop
- Stage 5 blocked
- no Stage 1–3/N3 numerical change

Validation:
- deterministic Stage 4/SHIELD contract tests
- complete v0.39 regression
- event-stream/larger-party regression
- GitHub Actions live Playwright/WebSocket validation
- only minimum Samsung Browser visual/input smoke that cannot be automated

Do not ask the user to manually execute validation suites when CI can run them.

## Following slices
- Stage 5–6 checkpoint boss + FLYER + authoritative Y geometry
- Stage 7–9 mixed-roster stress
- Stage 10 final boss/result
- Lv11/16/21 authority

## Deferred UX
Responsive safety across heterogeneous phone sizes/aspect ratios remains deferred as one shared responsive layer.

## Governance
No unapproved numerical change. Continue:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
