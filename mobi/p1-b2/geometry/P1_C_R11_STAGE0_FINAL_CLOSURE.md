# Mobi P1-C-R11 — Stage-0 Final Closure After Frame-Sign Audit

Date: 2026-10-16
Status: **CLOSED / FROZEN / PRE-EVIDENCE PASS**
Decision token: **`R11_STAGE0_IMPLEMENTATION_AND_FRAME_SIGN_FROZEN_NO_EVIDENCE_RUN`**

## Final public identity

- branch: `mobi/run-p1-c-r11-semantic-scaffold-20261016`
- R10 base HEAD: `a2138902b1070bc2d9ecb54c7e5d08efecbda1d2`
- implementation commit: `176bbb42b06e49c216ecd2f6de9d16e12feaa709`
- implementation-freeze commit: `bd3106762977166368b9c16788298319905222d6`
- initial Stage-0 closure commit: `fa9c0ce061d7a7aa361c65eb134b52d89dc7ae2d`
- frame/sign audit commit: `964c34c2c0723e3b12567d3690039b375a8615c5`
- freeze document blob: `e9b64933831973789ba68c4c0ff43e7f43230713`
- identity JSON blob: `1073fec0eaaa9daaa16488a157e24cc801db3f13`
- frame/sign audit document blob: `39d80a52a6c73aad457ce2b41e4cf7a8b1aa1053`
- frame/sign audit executable blob: `a49c4b6b9efc2ea6809624a09c474721980a10a8`
- frame/sign result blob: `63b9a3e829816e777e0bfdfabd47314a5e828b94`
- assembled Stage-1 implementation SHA-256: `af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87`

## Final Stage-0 decisions

1. All implementation constants required by the private R11 contract are frozen pre-evidence.
2. Public workflow scope is dispatch-only and branch/token gated.
3. No R11 public Actions evidence run has occurred.
4. Actual accepted source geometry plus frozen projection convention establish:

> **`+X_R10 = anatomical left`**

5. Therefore the frozen mapping is accepted without sign repair:

```text
x_B3 = z_R10
y_B3 = y_R10
z_B3 = x_R10
```

6. The actual V3125 mesh-array hash remains an execution-derived input identity because the accepted R10 artifact does not contain authoritative reduced arrays. Its reproduction implementation and serialization/hash rule are frozen. A future separately authorized Stage-1 workflow must derive and verify it under seeds `1` and `777` before any voxelization/scaffold extraction.
7. No Stage-1 structural output, finite pose or animation has been generated.

## Exact next boundary

> **R11 Stage-1 public evidence run — ELIGIBLE FOR A SEPARATE EXECUTION DECISION / NOT STARTED.**

Do not alter the Stage-0 constants or frame sign in response to future evidence. Any material change requires explicit change control.
