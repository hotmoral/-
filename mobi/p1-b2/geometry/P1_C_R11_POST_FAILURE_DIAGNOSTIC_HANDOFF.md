# Mobi P1-C-R11 Post-Failure Diagnostic Handoff

Date: 2026-10-16
Status: **CLOSED / DIAGNOSTIC PASS / CAUSE LOCALIZED**
Decision token: **`R11_DIAGNOSTIC_ALL_PAW_BIND_SURFACE_SEPARATION`**

## Completed checkpoint

The frozen observational diagnostic executed successfully without modifying the failed R11 implementation.

Execution:

- branch `mobi/run-p1-c-r11-post-failure-diagnostic-20261016`
- frozen execution HEAD `9d6d8de674c7d164975b0bf0286f8e573cbebe6e`
- run `38929129248` — SUCCESS
- artifact `12058232236`
- artifact digest `sha256:d7d1fb4abffd8f4ce05d35feedc8c2c20cbd1715f6d8e167acad1bff7c4556a3`

Determinism:

- seed1 JSON SHA-256 `9c11d312f9fe32ff458488bf0e6b3f8a304102dbc159d4e2819aaaf827b8f9be`
- seed777 JSON SHA-256 identical
- deterministic diff empty.

## Cause localized

All four paw terminals have zero V3125 surface vertices within the frozen `4*pitch` radius of their medial-path terminal bind.

Classifications:

- `FORE_L_PAW_CTRL` — `BIND_SURFACE_SEPARATION`
- `FORE_R_PAW_CTRL` — `BIND_SURFACE_SEPARATION`
- `HIND_L_PAW_CTRL` — `BIND_SURFACE_SEPARATION`
- `HIND_R_PAW_CTRL` — `BIND_SURFACE_SEPARATION`

Cross-side result:

> **`ALL_PAW_SYSTEMATIC`**

The failed paw controls are not dead. Their weighted/differential support counts are nonzero and substantial, but begin outside the frozen local radius.

Therefore domain exclusion and top-4 eviction are not the primary failure mechanism for the observed Stage-1 paw-local gate.

## Preserved authority

- V3125 remains the neutral morphology authority.
- V3125 mesh-array SHA remains `839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77`.
- R11 Stage 1 remains CLOSED / FAIL.
- `+X_R10 = anatomical left` remains unchanged.
- exactly six external domains remain authoritative.
- canonical contact semantics remain separate from this failed visual/deformation scaffold.

## No repair selected

This diagnostic does not authorize or choose among possible structural responses.

Separate private change-control must decide whether a next hypothesis should:

- derive terminal deformation binds differently from medial endpoints;
- explicitly separate surface/contact anchors from internal deformation-control endpoints;
- revise the six-domain/interface weighting architecture;
- revise influence/control layout;
- or abandon this RF-M scaffold family.

No option has been selected yet.

## Exact next boundary

> **Post-R11 structural change-control — ELIGIBLE / NOT STARTED.**

Do not start finite pose deformation, gait, IK, animation or downstream P1-G/P1-H work from this handoff.
