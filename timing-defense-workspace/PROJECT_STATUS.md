# Timing Defense — Project Status

Updated: 2026-10-21 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- current validated watched HEAD: `08af6e1e9f399ad13369990dcc452f012ddda1fa`

Last fully closed checkpoint:
- **v0.37 Slice B / Stage 3 FULL PASS**
- branch `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- HEAD `08af6e1e9f399ad13369990dcc452f012ddda1fa`

Preserved earlier checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`
- v0.36 automated PASS: `timing-defense-cloudflare-v036-automation-pass-20261021`
- v0.36 Slice A full PASS: `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- v0.37 Slice B full PASS: `timing-defense-cloudflare-v037-slice-b-pass-20261021`

Read first:
- `NEXT_WORK.md`
- `CLOUDFLARE_V037_SLICE_B_PASS_2026-10-21.md`
- `CLOUDFLARE_V036_SLICE_A_PASS_2026-10-21.md`
- `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`
- `CLOUDFLARE_V035_PASS_2026-10-21.md`

---

# Closed Cloudflare gates
## v0.31/v0.32 — PASS
- room create/join,
- nickname/class/slot/AI FILL,
- READY/READY cancel,
- host-only START,
- synchronized future start,
- waiting-room reconnect,
- Samsung Browser short-landscape layout.

## v0.33 — PASS
- authoritative shared Stage 1,
- synchronized monster HP/death and BASE HP,
- cross-device attacks affect same state,
- EXP/charge synchronization,
- shared clear.

## v0.34 — PASS
- remote human projectile visible,
- local immediate-hit presentation,
- server HP/EXP/coin/kills authority retained,
- acceptable smoothing.

## v0.35 — PASS
- Stage 1 -> Team Shop -> Stage 2,
- authoritative purchase/coin/rank,
- shop pending feedback + duplicate-tap protection,
- all-human READY + host NEXT,
- synchronized Stage 2 intro/input/combat,
- authoritative GRUNT/RUNNER state and clear,
- authoritative result board,
- reconnect,
- Rogue CHARGE visual correction,
- remote human timing-projectile parity.

## v0.36 Slice A — FULL PASS
Scope:
- Stage 1–2,
- N1 exact legacy timing EXP,
- N2 exact AI stage damage scaling,
- authoritative Lv6 consequences for all five human classes,
- action identity / secondary hit metadata,
- authoritative secondary-skill presentation.

N1 frozen migration parity values:
- NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28.

N2 frozen migration parity rule:
`AI damage × (1 + (stage - 1) * 0.035)`.

Lv6 authority validated:
- Knight +12% authoritative damage.
- Rogue one authoritative 55% second dagger after +55 ms.
- Tank +30% authoritative knockback.
- Archer up to two strict-line 52% secondary hits.
- Mage up to three nearby 50% splash hits.

Exact full-PASS deployment:
- branch `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- HEAD `c540119f469cff6795a74a3867c26f4c67de9071`

## v0.37 Slice B — FULL PASS
Scope:
- Stage 3 only,
- Stage 1–2 behavior preserved,
- Stage 2 clear -> Team Shop -> host NEXT -> Stage 3,
- Stage 3 clear -> Team Shop,
- Stage 4 blocked.

Exact Stage 3 encounter:
- 12 enemies,
- 980 ms gap,
- GRUNT 44% / RUNNER 34% / BRUTE 22%.

BRUTE authority:
- base HP 900,
- speed .040,
- wall damage 180,
- knock resist .38,
- armor 1.00,
- kill reward 14,
- existing stage HP factor and ordinary non-boss ×1.10 retained,
- Stage 3 ordinary BRUTE HP 1247.

Pre-deployment audit caught and fixed the legacy Stage1–2 wall-loop fallback that could otherwise have treated BRUTE wall damage as GRUNT 90. Stage 3 BRUTE wall contact now uses 180 and the existing DEF rule.

Automated validation PASS:
- SERVER 21/21,
- v0.36 CLIENT REGRESSION 4/4,
- STAGE3 CLIENT 6/6,
- MULTICLIENT 10/10,
- FINAL PASS.

Samsung Browser smoke PASS:
- Stage 1 -> Shop -> Stage 2 -> Shop -> Stage 3,
- BRUTE renders with the existing large BRUTE silhouette/body,
- no obvious monster/canvas corruption or teleport/flicker storm,
- timing input remains usable,
- Stage 3 clear -> Team Shop,
- host + SIM-PC separate participants,
- `STAGE 4 LOCKED` visible/enforced.

Exact full-PASS deployment:
- branch `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- HEAD `08af6e1e9f399ad13369990dcc452f012ddda1fa`

### N3 — DEFERRED / MANDATORY FUTURE DISCUSSION
Experimental combo-milestone extra attacks remain unresolved. They are not implemented and are not discarded. Do not silently port, remove, freeze or rebalance them.

---

# Immediate boundary — Slice C / larger-party baseline
Stage 4 must not start before Slice C closes.

Scope:
- 3 humans,
- 4 humans,
- 2 humans + 2 AI,
- 3 humans + 1 AI.

Primary validation targets:
- slot/host semantics,
- READY and START across 3–4 humans,
- Team Shop READY/NEXT across larger parties,
- reconnect identity under larger parties,
- participant/result consistency,
- human + AI + passive + Lv6 event concurrency,
- event delivery loss resistance and reconnect event-floor behavior.

Method:
- code audit first,
- expand deterministic and multi-WebSocket automation before manual play,
- use simulated peers where possible,
- final real-device work remains only a short render/input smoke.

Following slices:
- Stage 4 SHIELD / armor,
- Stage 5–6 boss + FLYER + authoritative Y geometry,
- Stage 7–9 mixed-roster stress,
- Stage 10 final boss/result,
- Lv11/16/21 authority with forced-level automated tests before natural progression relies on them.

---

# Frozen combat / balance governance
- Rhythm: `X -> X -> X -> X+Y`.
- Knight = stable generalist / penetration / strong heavy.
- Rogue = multihit / crit; same-target dagger hits uncapped.
- Tank = knockback / wall protection / team specialist.
- Archer = strict straight-line trajectory; no seeking/bending.
- Mage = density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP only from valid timing events; passive grants no EXP.
- Current combo presentation remains frozen unless explicitly changed.

Experimental, not production-frozen:
- passive `40 raw / 2.0 s`,
- ordinary non-boss HP +10%,
- combo persistent candidate `5/8/12/15%`,
- combo milestone raw-equivalent `60/90/150/210` — N3 mandatory future review.

Numerical workflow remains:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> numerical patch/freeze`.

## Deferred UX item
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred. Handle later as a shared responsive-safety layer rather than per-device patches.
