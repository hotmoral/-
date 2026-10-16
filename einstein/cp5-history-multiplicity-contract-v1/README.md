# Einstein CP5 History-Multiplicity Contract v1

This public bundle validates only the mechanics of a synthetic history/state multiplicity aggregator.

It is intentionally isolated from the private EinsteinGame repository and contains no production puzzle, seed, state hash, path ID, solver source, normalization implementation, or private diagnostic evidence.

## Contract scope

The synthetic fixture exercises:

- generated history arrivals versus unique semantic states;
- exact repeated-arrival count as `edge occurrences - unique arrival states`;
- inbound-history multiplicity histogram and deterministic top-state ordering;
- depth-local occurrences, depth-local distinct states, globally new states by minimum arrival depth, and repeat-pressure occurrences;
- same-state arrivals across multiple depths and path-cost ranges;
- synthetic skill labels for arrivals into reconverged states;
- frontier history multiplicity by semantic state;
- collection-order invariance;
- fail-closed rejection of duplicate target-history identity;
- integer/string/list/map-only semantic evidence.

## Explicit non-claims

A PASS does **not** establish any of the following:

- actual N5 multiplicity values;
- existence or absence of a human solution path;
- completeness of CP5 search;
- admissibility of global state pruning;
- correctness of a DAG conversion;
- preservation of CP8/CP9 or other downstream history-sensitive evidence;
- production EinsteinGame behavior.

This harness exists only to falsify mechanical aggregation mistakes before any private fixed-sample instrumentation is considered.

## Run

```bash
python3 einstein/cp5-history-multiplicity-contract-v1/contract_test.py
```

The test compiles the standalone Java source with the runner JDK, compares exact JSON from the normal and shuffled synthetic collections, checks the expected aggregate record, and verifies a negative duplicate-history control.
