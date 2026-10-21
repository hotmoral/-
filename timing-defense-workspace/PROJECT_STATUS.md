# Timing Defense — Project Status

Updated: 2026-10-21 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- current tested watched HEAD: `c540119f469cff6795a74a3867c26f4c67de9071`

Last fully closed checkpoint:
- v0.36 Slice A full PASS
- branch `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- HEAD `c540119f469cff6795a74a3867c26f4c67de9071`

Preserved earlier checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`
- v0.36 automated PASS: `timing-defense-cloudflare-v036-automation-pass-20261021`
- v0.36 Slice A full PASS: `timing-defense-cloudflare-v036-slice-a-pass-20261021`

Read first:
- `NEXT_WORK.md`
- `CLOUDFLARE_V036_SLICE_A_PASS_2026-10-21.md`
- `CLOUDFLARE_V036_AUTOMATION_PASS_2026-10-21.md`
- `CLOUDFLARE_V036_AUTOMATED_VALIDATION_2026-10-21.md`
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
- Stage 1–2 only,
- no Stage 3,
- N1 legacy exact timing EXP restoration,
- N2 legacy AI stage damage scaling restoration,
- authoritative Lv6 consequences for all five human classes,
- action identity / secondary hit metadata,
- authoritative secondary-skill presentation.

### N1 — APPROVED / IMPLEMENTED / PASS
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 10
- HEAVY+ 14
- GREAT 18
- SUPER 23
- CRITICAL 28

### N2 — APPROVED / IMPLEMENTED / PASS
`AI damage × (1 + (stage - 1) * 0.035)`

### N3 — DEFERRED / MANDATORY FUTURE DISCUSSION
Experimental combo-milestone extra attacks are not implemented and are not discarded. Do not silently port, remove, freeze or rebalance them.

### Lv6 authority now validated
- Knight: +12% authoritative damage.
- Rogue: one authoritative 55% second dagger after +55 ms, same-target allowed with nearest fallback.
- Tank: +30% authoritative knockback.
- Archer: up to two strict-line 52% secondary hits; no seeking/off-line retarget.
- Mage: up to three nearby 50% splash hits.

### Automated validation — PASS
Samsung Browser one-click suite:
- `SERVER · PASS · 10/10`
- `CLIENT · PASS · 4/4`
- `MULTICLIENT · PASS · 9/9`
- `FINAL · PASS`

Covers N1/N2, all five Lv6 boundaries, action identity, hit indices, stale seq rejection, Rogue local mutation block, reconnect event floor, two real WebSocket clients, READY/START/shared Stage1/reconnect/Shop/Stage2.

### Final device smoke — PASS
Single-device simulated-human harness was used only for the final browser/render/input smoke.
An initial harness bug was found and fixed: the simulated peer had overwritten the local bridge slot/session and overlays could cover normal CTAs.
After correction:
- local remains `ROGUE`,
- local `ROGUE LV6` is visibly selected,
- `SIM-PC` remains a separate `ARCHER` human participant,
- timing input works,
- no obvious projectile duplication storm/flicker/visual corruption,
- Stage 1 Team Shop is usable,
- Stage 2 completes,
- result board separately lists local Rogue and SIM-PC Archer.

Exact full-PASS deployment:
- `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- HEAD `c540119f469cff6795a74a3867c26f4c67de9071`

---

# Immediate boundary — Slice B
Slice B may start now.

Scope only:
- Stage 3,
- two humans first,
- Stage 2 clear -> Team Shop -> host NEXT -> Stage 3,
- exact legacy Stage 3: `12 enemies / 980 ms / GRUNT 44% / RUNNER 34% / BRUTE 22%`,
- authoritative BRUTE,
- Stage 3 clear -> Team Shop,
- Stage 4 remains blocked.

Validation policy:
- extend deterministic/server/multiclient automated harness first,
- use manual device play only for final render/input smoke,
- do not ask the user to visually verify exact numerical values already covered by automation.

## Later slices
- larger-party baseline: 3H / 4H / 2H+2AI / 3H+1AI,
- Stage 4 SHIELD,
- Stage 5–6 boss + FLYER + authoritative Y geometry,
- Stage 7–9 mixed stress,
- Stage 10 final boss/result,
- Lv11/16/21 authority with forced-level automated tests before natural progression depends on them.

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
