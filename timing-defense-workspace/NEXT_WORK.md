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
9. v0.39 N3 automated live validation — **PASS**

Exact v0.38 full-PASS checkpoint:
- branch `timing-defense-cloudflare-v038-slice-c-pass-20261022`
- HEAD `cbcddf35443ff901b4a30dd6621da5a984335fb5`

Exact v0.39 automated-live PASS checkpoint:
- branch `timing-defense-cloudflare-v039-automation-pass-20261022`
- HEAD `201ac36ac8ec97a3e033976cdea13c3fd2fe03c6`

## N3 product contract — APPROVED / FROZEN
- combo 5 / 10 / 20 / 30 / every +10 after 30
- exact max raw-equivalent budgets 60 / 90 / 150 / 210
- class-specific geometry retained
- deterministic remainder-safe allocation
- no EXP / charge / combo increment / ordinary crit / recursive skill / recursive N3
- normal armor / kill / kill coin / contribution
- frozen boss scalars
- generic N3 knockback uses NORMAL-equivalent semantics
- Tank retains class knockback identity

## v0.39 automated-live result — PASS
Public GitHub Actions runs real Playwright Chromium against the deployed Cloudflare Worker.

Validated:
- complete v0.38 regression
- N3 server 57/57
- N3 client authority/presentation event contract
- synchronized 4-human N3 stress
- FINAL PASS

4H stress:
- four Lv6 Rogue humans at combo29
- simultaneous PERFECT
- 4 ordinary hit + 4 Lv6 skill + 20 N3 = 28 combat events
- no event-gap
- contiguous post-floor event IDs
- all authoritative combos become 30

The Actions workflow now owns automated validation. Do not ask the user to manually open validation suites unless CI cannot execute a required gate.

## Immediate next step — one Samsung Browser N3 presentation/input smoke
Current watched smoke-candidate HEAD:
`f9e824eac87cc2fe39d80a75b345ce5aa8f574ce`

Candidate-only helper:
- query `n3smoke=1`
- once host combat has a monster, automatically arms humans to Lv6/combo29
- small non-blocking combat badge says `N3 ARMED · PERFECT 1회`
- normal game access is unaffected

Use one simulated second human (`peerbot=1`) so no PC is required.

Manual smoke acceptance is presentation/input only:
1. local player remains intended HOST/ROGUE
2. peer remains separate human
3. timing input works
4. after `N3 ARMED`, one PERFECT causes a visibly coherent N3 Rogue multi-dagger burst
5. no obvious duplicate-projectile storm, flicker, Canvas corruption or blocked controls
6. gameplay continues after the burst

Do not manually recheck damage budgets, event counts, EXP, charge, kill attribution or 4H delivery; Actions automation already owns those gates.

After this smoke passes:
- preserve exact v0.39 full-PASS checkpoint at the smoke HEAD
- write v0.39 full PASS report
- synchronize canonical docs
- move to Stage 4 SHIELD / armor

## Validation policy
Default:
`code audit -> deterministic tests -> GitHub Actions live Chromium/WebSocket validation -> only necessary Samsung Browser visual/input smoke`.

## Following slices
- Stage 4 SHIELD / armor
- Stage 5–6 checkpoint boss + FLYER + authoritative Y geometry
- Stage 7–9 mixed-roster stress
- Stage 10 final boss/result
- Lv11/16/21 authority

## Deferred UX
Responsive safety across heterogeneous phone sizes/aspect ratios remains deferred as one shared responsive layer.

## Governance
No unapproved numerical change. Continue:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
