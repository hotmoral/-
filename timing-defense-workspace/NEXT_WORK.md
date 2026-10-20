# Timing Defense — Next Work Boundary

## Current public state
- Public LIVE version: **v0.25**
- URL: `https://timing-defense-v011.onrender.com/v025.html`
- Live source HEAD: `fce42eb1261ff43277c27d844617b96a546d6d1a`
- Render deploy: `dep-dbbga8c9v7es73f567b0` / LIVE

## Balance governance remains unchanged
Do **not** production-freeze passive/combo/enemy-HP/projectile-speed values from UX feedback alone.
Required order:
`implement/test → measure → classify intent/artifact/defect → report → discuss → explicit decision → numerical freeze/patch`.

---

# Immediate device validation — v0.25

## Character-select vertical hierarchy
Test on the same Android landscape/browser used for the v0.24 recording:
- top brand/nickname whitespace is materially reduced,
- nickname remains easy to use,
- character-selection window is visibly taller,
- hero has more vertical presence,
- footer/PLAY SETTING remains reachable,
- no clipping against browser safe areas.

## Left combat profile
Verify:
- COMBAT PROFILE / Korean class name / large English class name / tag are readable,
- radar labels are materially larger than v0.24,
- all six labels fit: 공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역,
- five rings remain visible,
- role summary + one-sentence class description restore the richer character flavor,
- class-switch animation still cancels stale frames and restarts cleanly.

Approved profiles remain frozen presentation data:
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`

## Right skill panel
Verify:
- six skill cards remain `3 × 2`,
- icons/names/levels/descriptions use the extra vertical room cleanly,
- no card overlaps the hero,
- no description clipping on the target device.

## Existing v0.24 regression checks
- TEAM lineup class buttons remain fully visible in two rows,
- bottom SUMMARY remains removed,
- Rogue Timing Square/charge/EXP remains charcoal/black + silver,
- all valid timing EXP gains show `+EXP N`,
- projectile contrast/trails remain visible over natural scenery,
- projectile travel timing remains unchanged,
- READY → START, inside-square judgment and result board remain intact.

Fix visual/implementation defects directly. Do not change numerical combat balance from this validation.

---

# Next implementation slice — waiting-room UX
After v0.25 visual validation, implement the deferred TEAM waiting states without pretending networking already works.

## FRIEND
- waiting-room surface,
- local nickname/class/slot,
- reserved human slots,
- invite control placeholder,
- ready/start separate from connection state.

## LINK
- room/link presentation,
- truthful copy/share limitation before backend wiring,
- joining/waiting/participant-slot state,
- no fake join confirmation.

## RANDOM
- searching state,
- cancel action,
- participant placeholders,
- match-found transition design,
- no fake match success.

## Shared rules
- chosen nickname/class/tier preserved,
- AI filler configuration preserved where valid,
- TEAM AI max remains +2,
- leaving waiting returns safely to play settings,
- combat never runs behind waiting UI.

---

# Following boundary — real multiplayer architecture
After waiting UX stabilizes:
- room creation/authority,
- shareable invite/link contract,
- join/leave lifecycle,
- random matchmaking queue,
- slot/class ownership,
- synchronized start,
- Attack Round/combat events,
- disconnect/reconnect,
- state reconciliation/desync policy.

Do not claim real multiplayer until two independent clients share authoritative game state.

---

# Experimental combat values retained unchanged
Passive:
- 40 raw / 2.0 s
- no EXP / charge / crit / skill / combo
- ordinary non-boss HP +10%

Combo:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap
- milestone budgets 60 / 90 / 150 / 210 cap.

No retuning from lobby/readability observations.

## Still unresolved
- final passive damage/interval,
- final ordinary/elite/boss HP compensation,
- combo/milestone coefficients,
- final result-board metrics,
- final E/X pressure coefficients,
- exact tier progression/count/names,
- multiplayer economy/shop ownership,
- duplicate-class policy,
- sync DUO/TRIPLE/FULL rules,
- Lv26/Lv31 coefficients,
- room authority/network protocol,
- invite/link security contract,
- matchmaking policy,
- disconnect/rejoin behavior.
