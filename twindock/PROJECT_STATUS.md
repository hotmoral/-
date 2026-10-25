# Twin Dock Project Status

## Current phase
**P2 — World-readable docking feedback / mobile device-validation gate**

## Accepted foundation
- P0 modular foundation: ACCEPTED / canonical.
- P1 Mission 01 five-stage vertical slice: ACCEPTED / CLOSED.
- V8 remains the immutable fallback/control contract.
- Frozen input, thrust, speed, camera semantics and precision-docking thresholds are unchanged.

## Accepted P1 loop
Mission 01 sequence remains:
1. `STATIC`
2. `TRANSLATE`
3. `ROTATE`
4. `COMBINED`
5. `FINAL`

The ship keeps its motion state between targets, target translation and rotational port velocity both participate in relative-speed docking calculations, and the deterministic background remains continuous.

## P2 product question
Can the player judge docking readiness primarily from the world and docking hardware rather than a permanent four-condition debug checklist, without making the scene busier or changing the accepted feel?

## P2 candidate implemented
Branch: `twindock-p2-world-feedback-v1`

Normal-play HUD changes:
- permanent relative-speed number removed from normal HUD
- permanent position / speed / direction / spin checklist removed from normal HUD
- mission progress and compact status remain
- target/stage message remains compact at top center
- old numeric/checklist diagnostics remain available only with `?debug=1`

World-readable feedback is implemented as a separate transparent `FeedbackRenderer` overlay so the accepted renderer/physics stack remains untouched.

Feedback channels:
- **position**: four capture brackets close around the docking point and turn green inside the exact position threshold
- **orientation**: fixed ship-frame notches and rotating port notches visually overlap as facing alignment converges
- **angular velocity**: a short rotational trail shrinks as relative spin approaches zero and turns green inside the exact spin threshold
- **relative velocity**: a drift arrow shows relative-motion direction and magnitude, shrinking/turning green inside the exact relative-speed threshold
- successful capture receives a restrained green confirmation ring

## Regression boundary
Compared directly against accepted P1 closure HEAD `6c9ac2f0de5fbeb669f476b62a3a58d86b0324f2`.

Changed files only:
- `twindock/index.html`
- `twindock/styles.css`
- `twindock/src/main.js`
- `twindock/src/feedback.js` (new)

Unchanged frozen/core files include:
- `config.js`
- `input.js`
- `physics.js`
- `docking.js`
- `camera.js`
- `mission.js`
- `renderer.js`

Local JavaScript syntax checks for changed JS: PASS.

## Current gate
**Mobile device playtest of the P2 world-feedback candidate.**

Evaluate:
- can docking readiness be understood without looking for the old checklist?
- do the four visual channels become understandable after a few attempts without requiring text labels?
- are the markers restrained enough not to add motion sickness or clutter?
- does the reduced HUD improve focus on the station?
- is any signal misleading, especially relative velocity vs angular velocity?
- does control feel remain identical to accepted P1?

Do not retune frozen controls or docking thresholds during this gate. If a visual signal is unclear, change the visual mapping first.

## Next boundary after P2 acceptance
If P2 is accepted, close/synchronize P2 and then decide between:
1. presentation/game-feel polish (sound, restrained haptics, capture/transition polish), or
2. Android packaging/build lane if the mobile-web presentation is stable enough.

Do not add fuel, combat, upgrades/meta progression, or 3D migration as part of P2.

## Handoff rule
At each large-group closure, update this file and `docs/SESSION_HANDOFF.md` together and verify `docs/START_HERE.md` remains correct.
