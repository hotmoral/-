from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit('usage: patch.py <old-runner-file> <new-runner-file>')

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
s = src.read_text()

replacements = [
    ('static final String VERSION="1.1.0";', 'static final String VERSION="1.2.0";'),
    ('static final String EXPECTED_PRODUCTION_SOURCE="1d56f63da7217f2a96e72ddf5782d70fc1416c5f";', 'static final String EXPECTED_PRODUCTION_SOURCE="cdb66a3e0509bfec050a907bb43efb4e01b4ffeb";'),
    ('static final String EXECUTE_TOKEN="RUN_AUTHORIZED_DRAW0_RECOVERY_INVOCATION_3";', 'static final String EXECUTE_TOKEN="RUN_AUTHORIZED_DRAW0_RECOVERY_INVOCATION_4";'),
    ('static final String FORMAL_REMOTE_ROOT="evidence/bounded-acquisition/draw0-recovery-invocation-3";', 'static final String FORMAL_REMOTE_ROOT="evidence/bounded-acquisition/draw0-recovery-invocation-4";'),
    ('"historicalDraw0InvocationCount",2,"recoveryInvocationOrdinal",3', '"historicalDraw0InvocationCount",3,"recoveryInvocationOrdinal",4'),
    ('"recoveryInvocationOrdinal",3,"productionSource"', '"recoveryInvocationOrdinal",4,"productionSource"'),
    ('draw0InvocationOrdinal=3', 'draw0InvocationOrdinal=4'),
]

for old, new in replacements:
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'expected exactly one match for {old!r}, found {n}')
    s = s.replace(old, new, 1)

for forbidden in [
    'RUN_AUTHORIZED_DRAW0_RECOVERY_INVOCATION_3',
    'evidence/bounded-acquisition/draw0-recovery-invocation-3',
    '"historicalDraw0InvocationCount",2,"recoveryInvocationOrdinal",3',
    'draw0InvocationOrdinal=3',
]:
    if forbidden in s:
        raise SystemExit(f'old invocation3 marker remains: {forbidden}')

dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(s)
print('INVOCATION4_RUNNER_PATCH=PASS')
