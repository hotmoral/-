# Linkline A3 difficulty rebalance — public execution approval

Approval date: 2026-10-28
Approved by: project owner in ChatGPT session

## Approved work unit

Use the already-public target-pair candidate machinery to rebalance the 1,300-stage
campaign so trivial shortest solutions no longer dominate progression.

Owner requirements captured for this work unit:

- shortestDistance=1 may appear only in stages 1..5;
- shortestDistance=2 and 3 must be extremely rare;
- difficulty must rise rather than allowing hundreds of trivial repetitions;
- target-pair repetition remains a first-class constraint and must not be traded
  away merely to raise shortestDistance.

## Target-pair constraints retained

- N3/N4 displayed exact target-pair cap: 1;
- N5/N6 displayed exact target-pair cap: 2;
- for N5/N6, use all available exact target pairs once before any second use;
- expansion of public-safe candidate supply is preferred over dropping unique
  target-pair coverage when difficulty supply is insufficient.

## Public surfaces allowed

- deterministic sampling/execution parameters;
- already-public mechanic/solver/structural-analysis source projections;
- de-identified research-equivalence IDs;
- structural difficulty metadata including shortestDistance;
- aggregate difficulty/target-pair capacity summaries;
- public-safe generated candidate and selection artifacts needed for private
  canonical closure.

## Not approved for public exposure

- private canonical documents or private repository contents;
- private isolation IDs/lists or repair membership;
- human/self-test/telemetry exports or user data;
- secrets, credentials, or private environment values;
- raw private evidence or source corpora.

Final production adoption remains private and requires canonical isolation,
solver/materialization validation, hosted interaction QA, and explicit product
acceptance.
