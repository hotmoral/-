"""Generic public example: synthetic exposure-aware educational checks.

Independent toy implementation. Not a copy of any private learning engine.
No account, private-bank, or student data may ever be supplied to this module.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Attempt:
    example: str
    view: str
    result: str
    role: str = "TRAINING"
    delay_verified: bool = False


def summarize(attempts):
    """Evaluate toy curriculum: 3 first-try training examples, 2 views, new probe.

    Return *descriptive* coverage states, not a psychological diagnosis,
    mastery promotion, or a substitute for the private canonical runtime.
    """
    exposed = set()
    first_correct = {}
    fresh_probes = []
    fresh_delayed = []
    unresolved = set()

    for a in attempts:
        if a.role not in ("TRAINING", "NEW_PROBE", "LATE_PROBE"):
            raise ValueError("Unrecognized synthetic trial kind")
        if a.result not in ("FIRST_TRY", "CORRECTED", "GUIDED", "UNRESOLVED"):
            raise ValueError("Unrecognized synthetic trial result")
        if not a.example or not a.view:
            raise ValueError("Invalid synthetic example metadata")
        fresh = a.example not in exposed
        if a.result == "UNRESOLVED":
            unresolved.add(a.example)
        else:
            unresolved.discard(a.example)
        if a.role == "TRAINING" and fresh and a.result == "FIRST_TRY":
            first_correct[a.example] = a.view
        if a.role == "NEW_PROBE":
            fresh_probes.append((fresh, a.result == "FIRST_TRY"))
        if a.role == "LATE_PROBE":
            fresh_delayed.append((fresh, a.result == "FIRST_TRY", a.delay_verified))
        exposed.add(a.example)

    clean = not unresolved
    prepared = clean and len(first_correct) >= 3 and len(set(first_correct.values())) >= 2
    if not clean:
        return ("RECHECK", "RECHECK", "RECHECK")
    if not prepared:
        return ("INSUFFICIENT", "NOT_READY", "NOT_ASSESSED")
    if not fresh_probes:
        return ("PREPARED", "NOT_ASSESSED", "NOT_ASSESSED")
    if not any(fresh and correct for fresh, correct in fresh_probes):
        return ("PREPARED", "INCONCLUSIVE", "NOT_ASSESSED")
    if not fresh_delayed:
        return ("PREPARED", "SUPPORTED", "PENDING")
    if any(fresh and correct and checked for fresh, correct, checked in fresh_delayed):
        return ("PREPARED", "SUPPORTED", "SUPPORTED")
    return ("PREPARED", "SUPPORTED", "INCONCLUSIVE")
