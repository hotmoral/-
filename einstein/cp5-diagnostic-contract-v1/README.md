# Einstein CP5 Diagnostic Serialization Contract v1

This public micro-harness validates only the generic serialization boundary used by a private diagnostic workflow.

## Public scope

- strict canonical JSON parsing/writing
- integer-only canonical numeric domain
- Python -> persisted JSON -> Java parser handoff
- Java canonical round-trip and SHA-256 determinism
- nested `budgetConsumed.maxDepthReached` structure
- rejection of decimal JSON, Java `Float`, and Java `Double`
- representative float-free diagnostic checkpoint writing

## Explicitly excluded

This namespace contains no private puzzle sample, seed, generated puzzle, R/A/N identity, CP5 result hash, Bridge implementation, HumanPathExplorer implementation, downstream PSS logic, campaign evidence, or Android/runtime source.

Passing this harness does **not** prove CP5 budget suitability. It only proves that the task-local serialization/orchestration contract is safe to reuse before the private acceptance run.

## Run locally

```bash
python3 einstein/cp5-diagnostic-contract-v1/contract_test.py
```

Expected terminal line:

```text
PUBLIC CONTRACT PASS checks=<n>
```
