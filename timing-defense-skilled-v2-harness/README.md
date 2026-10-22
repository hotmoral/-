# Timing Defense — SKILLED_V2 Calibration Harness V0.1

Isolated browser harness for observed skilled-player trace collection.

## Safety boundary

- `HARNESS_ONLY`
- separate Worker name: `timing-defense-skilled-v2-harness`
- no campaign stars/Tier/achievement/EXP/coin/shop persistence
- no production multiplayer connection
- no external telemetry service
- raw traces stay in-browser until the user explicitly copies/saves JSONL
- no deployment to the live v0.45 worker

## Source baseline

Implementation branch was created from validated source:
`ea22cc279603394dc4b439b6fdbb0c83aff4299a`

## Preserved timing semantics

- normal one-way sweep 1100ms
- input lock 100ms
- GOOD width 0.42
- PERFECT width 0.17
- normal recovery 390ms
- charge 3 -> heavy opportunity
- heavy X -> Y delay 85ms
- PERFECT maintains/increments combo; non-PERFECT breaks it
- P×P is tracked explicitly

H1/H5 intentionally alter pressure cadence as calibration context; this is not a production balance setting.

## Harness contexts

- H0 TIMING_BASELINE
- H1 SUSTAINED_TEMPO
- H2 DURABLE_RHYTHM
- H3 TURNOVER_DENSITY
- H4 STATEFUL_READ
- H5 MIXED_PRESSURE

## Trace output

The UI emits local JSONL record families:
- `SESSION_START`
- `ACTION`
- `STATE`
- `SESSION_END`

The browser performs a bounded semantic validation at run end. The canonical planning validator remains the authority for collected datasets.

## Local commands

```bash
npm install
npm test
npm run dev
```

Do not run `npm run deploy` as a production step. Any calibration deployment must be explicitly authorized and must remain separate from the v0.45 production Worker.
