#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

MASK32 = 0xFFFFFFFF
ZERO_SEED_FALLBACK = 0x6D2B79F5
JUDGMENTS = ("PERFECT", "GOOD", "NORMAL")


def xorshift32(x: int) -> int:
    x &= MASK32
    if x == 0:
        x = ZERO_SEED_FALLBACK
    x ^= (x << 13) & MASK32
    x ^= (x >> 17) & MASK32
    x ^= (x << 5) & MASK32
    return x & MASK32


class RNG:
    def __init__(self, seed: int):
        self.x = seed & MASK32 or ZERO_SEED_FALLBACK

    def unit(self) -> float:
        self.x = xorshift32(self.x)
        return self.x / 2**32


def choose(dist: dict[str, float], u: float) -> str:
    acc = 0.0
    last = None
    for key, value in dist.items():
        last = key
        acc += float(value)
        if u < acc:
            return key
    if last is None:
        raise ValueError("empty distribution")
    return last


def build_stream(cfg: dict, seed: int, count: int) -> tuple[list[str], list[str]]:
    model = cfg["model"]
    rng = RNG(seed)
    state = choose(model["initialState"], rng.unit())
    judgments: list[str] = []
    states: list[str] = []
    for _ in range(count):
        s = model["states"][state]
        states.append(state)
        judgments.append(choose(s["judgmentDistribution"], rng.unit()))
        state = choose(s["transitionAfterJudgment"], rng.unit())
    return judgments, states


def max_perfect_streak(seq: list[str]) -> int:
    best = 0
    cur = 0
    for j in seq:
        if j == "PERFECT":
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


def check_distribution(name: str, dist: dict[str, float], errors: list[str]) -> None:
    total = sum(float(v) for v in dist.values())
    if abs(total - 1.0) > 1e-9:
        errors.append(f"{name} sums to {total}, expected 1.0")
    for key, value in dist.items():
        if float(value) < 0:
            errors.append(f"{name}.{key} is negative")


def stationary_focus(model: dict) -> float:
    f_to_b = float(model["states"]["FOCUS"]["transitionAfterJudgment"]["BASE"])
    b_to_f = float(model["states"]["BASE"]["transitionAfterJudgment"]["FOCUS"])
    denom = f_to_b + b_to_f
    if denom <= 0:
        raise ValueError("state chain is not ergodic")
    return b_to_f / denom


def implied_marginal(model: dict) -> dict[str, float]:
    pf = stationary_focus(model)
    pb = 1.0 - pf
    out = {}
    for j in JUDGMENTS:
        out[j] = (
            pf * float(model["states"]["FOCUS"]["judgmentDistribution"].get(j, 0.0))
            + pb * float(model["states"]["BASE"]["judgmentDistribution"].get(j, 0.0))
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config",
        nargs="?",
        default="timing-defense-workspace/legacy-game-structure/data/skilled_v2_central_sequence_candidate_v0_1.yaml",
    )
    parser.add_argument("--long-run-seeds", type=int, default=100)
    parser.add_argument("--long-run-count", type=int, default=10000)
    parser.add_argument("--combo-seeds", type=int, default=5000)
    parser.add_argument("--combo-window", type=int, default=100)
    args = parser.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    errors: list[str] = []
    model = cfg.get("model", {})

    if cfg.get("status") == "PRODUCTION_FROZEN":
        errors.append("candidate must not be marked PRODUCTION_FROZEN")
    if model.get("type") != "TWO_STATE_MARKOV_WITH_DETERMINISTIC_PRNG":
        errors.append("unexpected model type")
    if model.get("rng") != "XORSHIFT32":
        errors.append("unexpected RNG")

    check_distribution("initialState", model["initialState"], errors)
    for state_name in ("FOCUS", "BASE"):
        state = model["states"][state_name]
        check_distribution(f"{state_name}.judgmentDistribution", state["judgmentDistribution"], errors)
        check_distribution(f"{state_name}.transitionAfterJudgment", state["transitionAfterJudgment"], errors)

    prior = cfg["authority"]["marginalDesignPrior"]
    implied = implied_marginal(model)
    for j in JUDGMENTS:
        target = float(prior[j])
        if abs(implied[j] - target) > 1e-9:
            errors.append(f"implied {j}={implied[j]:.12f}, target={target:.12f}")

    focus_leave = float(model["states"]["FOCUS"]["transitionAfterJudgment"]["BASE"])
    mean_focus_run = 1.0 / focus_leave if focus_leave > 0 else float("inf")
    if mean_focus_run < 40.0:
        errors.append(f"mean FOCUS run {mean_focus_run:.3f} is below combo40 structural anchor")

    # Exact deterministic replay check.
    a, sa = build_stream(cfg, 123456789, 1000)
    b, sb = build_stream(cfg, 123456789, 1000)
    if a != b or sa != sb:
        errors.append("same-seed replay is not deterministic")

    # Long-run empirical sanity probe. This is validation of the implementation,
    # not a population-fit claim.
    counts = Counter()
    state_counts = Counter()
    for seed in range(1, args.long_run_seeds + 1):
        js, ss = build_stream(cfg, seed, args.long_run_count)
        counts.update(js)
        state_counts.update(ss)
    total = sum(counts.values())
    observed = {j: counts[j] / total for j in JUDGMENTS}
    focus_share = state_counts["FOCUS"] / total
    for j in JUDGMENTS:
        if abs(observed[j] - float(prior[j])) > 0.005:
            errors.append(f"long-run {j} drift too large: {observed[j]:.6f}")

    combo_peaks: list[int] = []
    for seed in range(1, args.combo_seeds + 1):
        js, _ = build_stream(cfg, seed, args.combo_window)
        combo_peaks.append(max_perfect_streak(js))
    combo40_reach = sum(1 for x in combo_peaks if x >= 40) / len(combo_peaks)
    if max(combo_peaks, default=0) < 40:
        errors.append("combo40 never appears in diagnostic seed set")

    summary = {
        "ok": not errors,
        "version": cfg.get("version"),
        "stationaryFocusShare": stationary_focus(model),
        "impliedMarginal": implied,
        "meanFocusRunJudgments": mean_focus_run,
        "longRunProbe": {
            "seeds": args.long_run_seeds,
            "judgmentsPerSeed": args.long_run_count,
            "observed": observed,
            "focusShare": focus_share,
        },
        "comboProbe": {
            "seeds": args.combo_seeds,
            "windowJudgments": args.combo_window,
            "combo40ReachRate": combo40_reach,
            "medianPeak": sorted(combo_peaks)[len(combo_peaks) // 2] if combo_peaks else None,
            "maxPeak": max(combo_peaks) if combo_peaks else None,
            "note": "diagnostic only; not a frozen production target",
        },
        "errors": errors,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
