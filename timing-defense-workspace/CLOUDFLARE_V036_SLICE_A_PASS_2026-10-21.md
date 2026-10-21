# Timing Defense Cloudflare v0.36 Slice A — PASS

Date: 2026-10-21 KST

## Result
v0.36 Slice A is **PASS**.

Slice A scope:
- Stage 1–2 only,
- N1 legacy exact timing EXP restoration,
- N2 legacy AI stage damage scaling restoration,
- server-authoritative Lv6 consequences for all five human classes,
- action identity / secondary-hit metadata,
- authoritative secondary skill presentation,
- no Stage 3.

## Preserved full-PASS deployment
- branch: `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- HEAD: `c540119f469cff6795a74a3867c26f4c67de9071`
- watched source branch: `timing-defense-cloudflare-do-poc`

The cf.3 automated suite deployment was separately preserved at:
- `timing-defense-cloudflare-v036-automation-pass-20261021`
- HEAD `abb2d428df546c257181278ba6bd0814e0471c93`

## Explicit numerical decisions
N1 — approved / implemented / PASS:
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 10
- HEAVY+ 14
- GREAT 18
- SUPER 23
- CRITICAL 28

N2 — approved / implemented / PASS:
`AI damage × (1 + (stage - 1) * 0.035)`

N3 — deferred / mandatory future discussion:
Experimental combo-milestone extra attacks are not implemented and are not discarded. They must not be silently ported, removed, frozen or rebalanced.

## Automated validation evidence
The user ran the deployed one-click validation suite in Samsung Browser.
Observed final result:
- `SERVER · PASS · 10/10`
- `CLIENT · PASS · 4/4`
- `MULTICLIENT · PASS · 9/9`
- `FINAL · PASS`

The suite covered:
- N1/N2,
- Knight +12% server damage,
- Rogue 55% authoritative delayed second dagger,
- Tank +30% knockback,
- Archer strict-line 52% secondary hits,
- Mage 50% splash,
- actionId / hitIndex continuity,
- stale/duplicate seq rejection,
- Rogue local-network secondary gameplay mutation block,
- reconnect event-floor / no historical secondary VFX replay,
- two real WebSocket clients against the deployed Durable Object,
- READY / START / shared Stage 1 / reconnect / Team Shop / Stage 2 synchronization.

## Device smoke evidence
A single-device smoke harness was added only for validation. It injects a second simulated human through the real room WebSocket/API path while the Samsung Browser remains the local human renderer/input client.

An initial harness defect was found and corrected:
- the simulated peer socket was being observed by the main bridge and could overwrite the local slot/session,
- debug overlays could cover normal READY/START/NEXT controls.

Correction:
- simulated peer now uses the original native WebSocket constructor and does not mutate the main bridge,
- local debug level control pins the original local session/slot,
- test overlays are combat-only and do not cover lobby/shop CTA controls.

Final Samsung Browser smoke recording confirmed:
- local player remains `ROGUE`,
- local debug display shows `ROGUE LV6` with LV6 selected,
- `SIM-PC` remains a separate `ARCHER` human participant,
- timing input is functional,
- no obvious projectile duplication storm, flicker or visual corruption was observed,
- Stage 1 Team Shop is usable,
- Stage 2 completes,
- result board separately lists local Rogue and SIM-PC Archer with authoritative contribution values.

## Lv6 authority frozen by this slice
- Knight: +12% authoritative damage.
- Rogue: one authoritative 55% second dagger after +55 ms; same-target allowed with nearest fallback.
- Tank: +30% authoritative knockback.
- Archer: up to two strict-line additional hits at 52%; no seeking/off-line retarget.
- Mage: up to three nearby splash hits at 50%.

## Known non-production test assets
The peerbot/debug controls are candidate-only validation tools. They do not redefine gameplay rules. Normal gameplay must not depend on their presence.

## Next boundary
Slice B may now begin.

Slice B scope only:
- Stage 3,
- two humans first,
- Stage 2 clear -> Team Shop -> host NEXT -> Stage 3,
- exact legacy Stage 3: `12 enemies / 980 ms / GRUNT 44% / RUNNER 34% / BRUTE 22%`,
- authoritative BRUTE,
- Stage 3 clear -> Team Shop,
- Stage 4 remains blocked.

No additional numerical balance change is authorized by this PASS.
