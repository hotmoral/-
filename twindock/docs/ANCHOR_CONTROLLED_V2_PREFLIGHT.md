# Twin Dock — Capture-Anchor Controlled Probe v2 Preflight

Status: **READY TO IMPLEMENT**

The v1 controlled probe fixed station-COM translation and angular velocity but device play exposed a remaining causal confound: docking-point-relative motion still changed between stages.

The v2 probe controls the actual quantities seen by docking truth.

## Frozen
- craft rotation center / COM
- accepted controls and physics constants
- Long Cargo hull
- rectangular port semantics
- docking thresholds
- ship-frame camera

## Independent-trial initial state
Each stage starts from the same ship body state:
- same body center position
- `vx=0`, `vy=0`
- angle `0`
- angular velocity `0`
- angular-drive state `0`

There is no inherited velocity from the prior dock.

## Target capture-anchor truth
For every trial, independent of anchor direction/eccentricity:
- the vector from the **player docking anchor** to the target capture anchor at spawn is identical
- target capture-anchor world linear velocity is identical
- target angular velocity is identical
- initial target-port orientation is geometrically aligned to the player local anchor orientation

Station center pose/velocity are derived from these capture-anchor requirements. Station-COM velocity is therefore allowed to differ between trials; that difference is compensation, not gameplay variation.

## Variable under test
Only the player docking anchor local geometry changes:
1. upper side r61
2. front r98
3. lower side r61
4. rear r98
5. lower-right corner r98

## Acceptance boundary
A device difficulty ordering from v2 may be interpreted as anchor geometry evidence only after automated tests prove the independent initial body state and target capture-anchor position/velocity/spin invariants.
