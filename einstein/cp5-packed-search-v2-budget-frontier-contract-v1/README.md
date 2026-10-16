# Einstein CP5 Packed Search v2 Budget / Frontier Synthetic Contract v1

Public-safe synthetic prerequisite for packed-v2 native budget/frontier semantics.

This bundle contains **no private Einstein production source, puzzle data, state hashes, seeds, clues, N5 payloads, credentials, or private evidence**.

It validates only generic packed-search resource-accounting semantics that were not covered by the earlier public packed-provenance / v1-projection contract:

- unique semantic-state FIFO first-discovery order;
- deterministic semantic-arc order;
- semantic-state limit before dequeue/inspection;
- semantic-arc limit at zero, mid-source, and exact end-of-source;
- no premature cutoff merely because the arc count equals its cap;
- solved / invalid / stalled inspection after the arc count already equals the cap;
- first later productive state becomes the actual ARC_LIMIT source when a new arc would be required;
- exact pending suffix / offset and queued-unvisited ordering after a real arc cutoff;
- depth-bound states are inspected and enumerated but emit no outgoing arc;
- productive depth-bound search cannot conclude global no-Human-path;
- uninspected is distinct from stalled;
- parallel arcs, reconvergence, and cross-depth minimum-depth bookkeeping;
- separate semantic-search completeness, cutoff causes, provenance-language status, and explicit materialization status;
- packed-v2 identity is distinct from legacy-v1 projection identity;
- construction-order invariance and semantic-cycle rejection.

## Run

```bash
python3 einstein/cp5-packed-search-v2-budget-frontier-contract-v1/contract_test.py
```

Expected terminal prefix:

```text
PUBLIC_PACKED_V2_BUDGET_FRONTIER_CONTRACT_PASS
```

## Claim boundary

A PASS proves only this **generic synthetic packed-v2 budget/frontier contract**.

It does **not** prove private production integration, production `HumanPathExplorer` compatibility, CP8/CP9/CP10 behavior, N5 performance, Human-path existence/absence on private puzzles, scale suitability, or any policy/admission decision.
