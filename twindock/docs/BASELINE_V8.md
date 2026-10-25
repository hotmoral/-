# Baseline V8 — Frozen Core Feel

V8 is the promoted control baseline.

## Freeze rules

Changes to the following require an explicit controlled experiment rather than incidental cleanup:
- input response curve
- thrust scale
- damping
- maximum linear/angular velocity
- angular response smoothing
- ship-frame camera semantics
- docking precision thresholds

Refactors must demonstrate device parity before changing gameplay values.

## Current constants
- force scale: 58
- input deadzone: 0.10
- input exponent: 2.05
- max speed: 78
- max angular speed: 0.90
- station omega: 0.18
- docking distance: 11
- docking relative speed: 10
- docking direction error: 0.095 rad
- docking angular-speed error: 0.10 rad/s

## Exact baseline artifact
- filename: `twin_dock_webapp_v8.html`
- bytes: 33069
- SHA-256: `fa569b3411acb59edcfde54b4bac6b59970f8aa0e1ef1fb7f7d339ab26a0ab89`
