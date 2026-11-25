"""Independent 24-attribute sampler. Candidate pools are supplied by the caller.

This module does not define or approve the canonical option vocabulary.
No topic, age or level enters the draw. Adjustments belong in a separate log.
"""
from datetime import datetime, timezone
import hashlib
import json
import random
import secrets

ATTRIBUTE_NAMES = (
    "전문적 배경", "직업적 시각", "관심 초점", "사고 접근",
    "관찰 범위", "서술 목적", "독자와 거리", "어조",
    "어휘 성향", "문장 길이", "통사 구조", "문장 리듬",
    "도입", "정보 전개", "문단 구성", "결말",
    "종결 습관", "접속 표현", "주어 표현", "수식어 배치",
    "정보 제시 순서", "구체화", "문단 연결", "설명 압축도",
)


def validate_pools(pools):
    if not isinstance(pools, dict) or set(pools) != set(ATTRIBUTE_NAMES):
        raise ValueError("exactly 24 named attribute pools required")
    for name in ATTRIBUTE_NAMES:
        values = pools[name]
        if (not isinstance(values, list) or len(values) < 2
                or any(not isinstance(v, str) or not v.strip() for v in values)
                or len(set(values)) != len(values)):
            raise ValueError("each pool needs >=2 distinct nonempty strings: " + name)


def draw_author_attributes(passage_id, pools, *, seed=None):
    """Draw one independent uniform value per attribute.

    seed=None: production SystemRandom; integer seed: reproducible experiment.
    No silent rerolling, topic matching, or quality claims.
    """
    if not isinstance(passage_id, str) or not passage_id.strip():
        raise ValueError("passage_id required")
    validate_pools(pools)
    if seed is not None and (type(seed) is not int or seed < 0):
        raise ValueError("experimental seed must be a nonnegative integer")
    rng = secrets.SystemRandom() if seed is None else random.Random(seed)
    selections = {name: rng.choice(pools[name]) for name in ATTRIBUTE_NAMES}
    canonical_pools = json.dumps(
        {name: pools[name] for name in ATTRIBUTE_NAMES},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    )
    return {
        "passage_id": passage_id,
        "selection_method": "system_csprng_uniform_v1" if seed is None else "python_mt19937_seeded_v1",
        "experimental_seed": seed,
        "selected_at_utc": datetime.now(timezone.utc).isoformat(),
        "candidate_pools_sha256": hashlib.sha256(canonical_pools.encode("utf-8")).hexdigest(),
        "author_attributes_24": selections,
        "attribute_application_log": {
            name: {"status": "PENDING", "reason": None} for name in ATTRIBUTE_NAMES
        },
        "release_approved": False,
    }


def verify_selection(record, pools):
    """Check provenance shape and pool membership, not true RNG provenance."""
    validate_pools(pools)
    selections = record.get("author_attributes_24")
    if not isinstance(selections, dict) or set(selections) != set(ATTRIBUTE_NAMES):
        return False
    if not all(selections[name] in pools[name] for name in ATTRIBUTE_NAMES):
        return False
    canonical_pools = json.dumps(
        {name: pools[name] for name in ATTRIBUTE_NAMES},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    )
    expected_hash = hashlib.sha256(canonical_pools.encode("utf-8")).hexdigest()
    if record.get("candidate_pools_sha256") != expected_hash:
        return False
    seed = record.get("experimental_seed")
    if seed is not None:
        if type(seed) is not int or seed < 0:
            return False
        rng = random.Random(seed)
        return selections == {name: rng.choice(pools[name]) for name in ATTRIBUTE_NAMES}
    return record.get("selection_method") == "system_csprng_uniform_v1"
