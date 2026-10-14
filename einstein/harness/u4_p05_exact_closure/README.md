# Einstein U4/P05 public-safe exact-closure model

This directory is a standalone, synthetic execution model for the currently authorized EinsteinGame U4/P05 public execution gate.

It is deliberately **not** a copy of the private `hotmoral/EinsteinGame` production Java implementation and contains no private puzzle fixture, private source, credential, signing material, asset, or personal data.

## What it checks

The model exercises the public-safe algorithmic invariants already fixed by the canonical U4/P05 preflight:

- exact state content is authoritative; a hash alone is never identity;
- terminal precedence is guard -> solved -> productive opportunities -> stalled iff none;
- every productive edge preserves complete opportunity/provenance plus the exact transition step and destination;
- equal destinations may be expanded once, but parallel provenance edges remain distinct;
- complete outgoing edge comparison is multiset-based, so harmless ordering changes are accepted while omissions, additions, and provenance loss are rejected;
- productive transitions must strictly decrease the synthetic FD01-style rank;
- closure-only and solved-terminal absence are separate propositions;
- `targetPredicate = null` proves closure only;
- only the synthetic `SOLVED_TERMINAL` target is accepted;
- unresolved frontier is `INCOMPLETE`, never absence;
- malformed/tampered/mismatched evidence is rejected rather than converted into a puzzle semantic failure.

The suite contains 25 deterministic controls: public-safe synthetic realizations of G009, G010, G011, G012, G013, G016, G035, G037 and G047; two positive controls for closure/absence separation; and fourteen implementation mutation controls.

## Non-claim

A PASS from this harness means only that this standalone public model and its mutation controls behaved as specified.

It does **not** establish that the private EinsteinGame Java implementation compiles, integrates, preserves the frozen production source surface, or passes its real tests. Any later private implementation/integration remains a separate gate.
