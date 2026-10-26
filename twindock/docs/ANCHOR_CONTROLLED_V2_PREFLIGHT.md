# Twin Dock — Capture-Anchor Controlled Probe v2

Status: **IMPLEMENTED / BUILD PASS / PHYSICAL DEVICE EVALUATION PENDING**

The v1 controlled probe fixed station-COM translation and angular velocity but device play exposed a remaining causal confound: docking-point-relative motion still changed between stages.

The v2 probe controls the actual quantities seen by docking truth.

## Parent device evidence

v1 device ordering, hardest to easiest:

`2 > 4 > 1 > 3 > 5`

The user also perceived a regular pattern in station movement/rotation speed. Investigation confirmed:
- control sensitivity was unchanged
- profile station-COM translation and omega were nominally identical
- however the ship inherited prior capture-anchor velocity between docks
- changing anchor orientation rotated the station capture-anchor tangential velocity
- therefore actual relative target motion differed between trials

The v1 ranking is retained as evidence for that build but is not a causal anchor ranking.

## Frozen
- craft rotation center / COM
- accepted controls and physics constants
- Long Cargo hull
- rectangular port semantics
- docking thresholds
- ship-frame camera

## Independent-trial initial state
Each stage starts from the same ship body state:
- body center `x = W * 0.14`, `y = H * 0.46`
- `vx=0`, `vy=0`
- angle `0`
- angular velocity `0`
- angular-drive state `0`

There is no inherited velocity from the prior dock.

## Target capture-anchor truth
For every trial, independent of anchor direction/eccentricity:
- the vector from the **player docking anchor** to the target capture anchor at spawn is identical
- target capture-anchor world linear velocity is identical
- target angular velocity is identical (`-0.14`)
- initial target-port orientation is geometrically aligned to the player local anchor orientation

Station center pose/velocity are derived from these capture-anchor requirements. Station-COM velocity is therefore allowed to differ between trials; that difference is compensation required to keep the gameplay-relevant capture point identical.

## Variable under test
Only the player docking anchor local geometry changes:
1. upper side r61
2. front r98
3. lower side r61
4. rear r98
5. lower-right corner r98

## Implementation

Experimental branch:
- `twindock-geometry-capture-controlled-probe-v2`
- implementation commit `d9bdc66525f05c235178ce617e6c0f1f104da3f2`

Changed experimental surfaces:
- `src/mission.js`
- probe UI copy in `index.html` / `src/main.js`
- `tests/mission.mjs`
- `tests/anchor-controlled.mjs`
- CI branch allow-list

Frozen gameplay configuration, physics integration, docking checks, camera and P3 effects were not retuned.

## Automated evidence

GitHub Actions run:
- `40280944722`
- result **SUCCESS**

Passed:
- accepted web regressions
- capture-anchor controlled mission tests
- causal-control tests proving identical ship initial body state
- causal-control tests proving identical target docking-point relative spawn vector
- causal-control tests proving identical target docking-point linear velocity and omega
- retained Geometry v2/craft-family regressions
- Android staging and Capacitor contract checks
- Gradle debug APK build
- artifact upload

Artifact:
- artifact ID `12631408703`
- ZIP digest `sha256:da62774b431ebfd8ef52aaa62dbe2d0784efa9c653469944350ea93221e7e5d9`
- extracted APK bytes `4,147,637`
- extracted APK SHA-256 `08b5ce32ae3981234cf9281ff0eb65a63439b57ca44e4f1f0f4ee5090a8e8960`

## Device question

Play all five independent trials and report difficulty order again.

Most useful comparisons:
- 1 vs 3: same radius 61, opposite side
- 2 vs 4: same radius 98, front vs rear
- 2 vs 4 vs 5: same radius ~98, direction/placement only
- r61 group vs r98 group: eccentricity effect

A new ordering from this v2 build can now be interpreted much more directly as anchor geometry evidence.
