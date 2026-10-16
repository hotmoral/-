# Einstein CP5 Packed Traversal Synthetic Provenance / V1 Projection Contract v1

Public-safe generic contract only.

This bundle contains **no private Einstein puzzle data, private state hash, seed, clue set, production source, or N5 evidence payload**.

It validates the bookkeeping design required before any private or production packed traversal work:

- unique semantic-state expansion with deterministic canonical arc order;
- same-depth reconvergence with divergent accumulated costs;
- cross-depth reconvergence while retaining longer provenance histories;
- parallel semantic arcs between the same source/target states;
- lossless reconstruction of ordered history, cost, and path identity;
- exact synthetic v1 history-occurrence projection under depth and edge cutoffs;
- FIFO frontier/cutoff projection behavior;
- construction-order/shuffle invariance;
- explicit separation of:
  - semantic-search completeness,
  - provenance-language coverage,
  - explicit materialization status;
- explicit packed-vs-v1 identity/version boundary;
- rejection of semantic cycles.

## Synthetic fixture

The fixture is intentionally small and abstract:

- `C` is reached by three histories:
  - one direct depth-1 history,
  - two depth-2 histories with different costs;
- `C -> D` has two parallel opportunity arcs;
- `D -> E` provides a depth-boundary continuation.

This forces the contract to preserve both divergent-cost and cross-depth provenance without requiring repeated semantic expansion.

## Run

```bash
python3 einstein/cp5-packed-traversal-projection-contract-v1/contract_test.py
```

Expected terminal prefix:

```text
PUBLIC_PACKED_PROVENANCE_PROJECTION_CONTRACT_PASS
```

## Claim boundary

A PASS proves only that the **generic synthetic bookkeeping contract** can preserve the tested history language and reproduce the tested legacy occurrence traversal.

It does **not** prove:

- production `HumanPathExplorer` correctness under a packed implementation;
- private N5 behavior;
- any performance gain;
- CP8/CP9/CP10 packed-native compatibility;
- Human-path existence or absence;
- CP13 admission/support;
- safety of destructive state pruning.

Any production or private semantic implementation requires a separate authorization and evidence step.
