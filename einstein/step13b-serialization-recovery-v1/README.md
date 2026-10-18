# Einstein Step 13B Serialization Recovery — Public Contract Harness

This directory is a **public-safe synthetic contract harness**. It does not contain private EinsteinGame source, private historical evidence, real puzzle/sample data, or real private identities.

## Scope

The harness models one narrow failure mode: a raw diagnostic JSON document may contain operational floating-point timing fields while a downstream canonical consumer accepts integer numeric literals only.

The tested recovery contract is:

1. parse raw JSON with duplicate-key rejection;
2. construct an explicit allowlist-based semantic projection;
3. reject unsupported numeric/types recursively before serialization;
4. serialize deterministically;
5. verify the projected document with an independent Java integer-only JSON contract probe.

The synthetic raw fixtures intentionally contain decimal timing values. The committed expected projections intentionally omit those operational fields.

## Run

```bash
python3 contract_test.py
```

The test suite compiles `StrictIntegerJsonProbe.java` with the available JDK and executes both valid and adversarial cases.

## Non-claims

A PASS here does **not** prove that any private historical EinsteinGame evidence, private producer, N5 sample, packed search, or production parser succeeds. It proves only that this public semantic-projection design is deterministic, float-free, fail-closed, and compatible with the independent integer-only contract probe under synthetic evidence.
