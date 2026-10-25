# Foundation Manifest

## Accepted prototype
- V8 HTML SHA-256: `fa569b3411acb59edcfde54b4bac6b59970f8aa0e1ef1fb7f7d339ab26a0ab89`
- V8 HTML size: 33069 bytes

## Local modularization candidate
A local P0 candidate was created by separating config, math, state, docking, input, physics, camera, UI, renderer and main orchestration while preserving V8 tuning constants.

- candidate archive SHA-256: `4d459bf474bca9e8eb9da83b2e0dd919b0bd76705493957fab778cd33da1773b`
- candidate archive size: 31837 bytes
- deterministic smoke test: PASS

The candidate is intentionally **not yet canonical**. It must first pass mobile feel/parity comparison against V8 before source promotion.
