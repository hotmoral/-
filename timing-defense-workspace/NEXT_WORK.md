# Timing Defense — Next Work Boundary

## Current public state
- Public LIVE version: **v0.24**
- URL: `https://timing-defense-v011.onrender.com/v024.html`
- Live source HEAD: `61ad74d833148d409dc65292f302bb9086c4e7c9`
- Render deploy: `dep-dbbg528m7kps73esejbg` / LIVE

## Balance governance remains unchanged
Do **not** production-freeze passive/combo/enemy-HP/projectile-speed values from UX feedback alone.
Required order:
`implement/test → measure → classify intent/artifact/defect → report → discuss → explicit decision → numerical freeze/patch`.

---

# Immediate device validation — v0.24

## Character profile radar
Verify on Android landscape:
- five concentric hex rings fit cleanly,
- all six labels fit: 공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역,
- class-color polygon is easy to read,
- class-switch animation feels fast/premium,
- center-out scan + staggered vertex fill does not look laggy,
- old animation cancels when the user rapidly changes classes.

Approved five-level profiles are frozen as presentation data in `CHARACTER_PROFILE_RADAR_V1.md`.

## Character / skill layout
Verify:
- center hero has clearly more vertical room than v0.23,
- hero never overlaps the right panel,
- navigation arrows visually belong to the hero and remain easy to tap,
- swipe still works,
- all six skill cards fit as `3 × 2`,
- every skill card shows icon/name/level/description without awkward clipping.

## TEAM lineup
Verify:
- bottom SUMMARY is gone,
- each AI unit has enough vertical height,
- five class choices wrap into two rows and none are clipped,
- SOLO still allows 0–3 AI,
- TEAM AI FILL still allows 0–2 AI and reserves at least one human slot.

## Rogue HUD
Verify:
- Timing Square reads charcoal/black + silver, not red,
- charge pips read black/silver in active and inactive states,
- LV/EXP gauge and `+EXP N` read as black/silver,
- contrast remains sufficient over both bright sky/ground and dark scenery.

## Projectile visibility
Verify each class in live combat:
- Knight blade wave recognizable,
- Rogue dagger recognizable,
- Tank shockwave recognizable,
- Archer arrow recognizable,
- Mage orb recognizable.

v0.24 changes contrast/trails only; projectile travel life/timing remains unchanged.
If the user still perceives only a blur after this pass, report the class(es) and discuss a small travel-time adjustment before applying it.

## Existing regression checks
- all valid timing EXP gains still show `+EXP N`,
- lower-left EXP float absent,
- attack debug line absent,
- inside-square judgment still quick/readable,
- result board rows/nickname remain correct,
- READY → START flow intact.

---

# Next implementation slice — waiting-room UX
The originally planned waiting flow has been deferred because v0.23 and v0.24 were used for device-feedback polish.
After v0.24 visual validation, implement the user-visible TEAM waiting states without pretending networking already works.

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

---

# Later balance execution
After lobby/network architecture reaches a stable combat model:
1. full-run wall HP carry,
2. local + AI/human-equivalent EXP/level progression,
3. shop progression,
4. passive-only / Average / Skilled / Expert,
5. solo / 2P / 3P / 4P,
6. pressure recipe rerun,
7. report before numerical production freeze.

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
