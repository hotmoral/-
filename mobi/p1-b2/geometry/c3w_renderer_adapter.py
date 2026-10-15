from __future__ import annotations

from c3_renderer_authored_view_basis_v5 import _render_h6 as render_authored_basis_h6
from c3_renderer_minimal_v3 import render_fixture as render_generic_v3
from c3_renderer_view_resolved_v4 import _render_h6 as render_view_resolved_h6
from c3w_h6n_fixture_adapter import H6N_CASE_ID

STRATEGY_GENERIC = "C3_V3_GENERIC"
STRATEGY_VIEW_RESOLVED = "C3R_VIEW_RESOLVED"
STRATEGY_AUTHORED_BASIS = "C3V_AUTHORED_BASIS"
STRATEGIES = (
    STRATEGY_GENERIC,
    STRATEGY_VIEW_RESOLVED,
    STRATEGY_AUTHORED_BASIS,
)
VARIANTS = ("RF_B", "RF_C")
ADAPTER_VERSION = "P1_C3W_H6N_RENDERER_REPLAY_V1"


def render_h6n(fixture, strategy: str, variant: str):
    if fixture.case_id != H6N_CASE_ID:
        raise ValueError(f"C3W adapter accepts H6N V2 only: {fixture.case_id}")
    if strategy not in STRATEGIES:
        raise ValueError(strategy)
    if variant not in VARIANTS:
        raise ValueError(variant)

    if strategy == STRATEGY_GENERIC:
        rendered = render_generic_v3(fixture, variant)
    elif strategy == STRATEGY_VIEW_RESOLVED:
        rendered = render_view_resolved_h6(fixture, variant)
    else:
        rendered = render_authored_basis_h6(fixture, variant)

    if rendered["semanticHash"] != fixture.semantic_hash:
        raise RuntimeError(
            f"semantic hash mismatch strategy={strategy} variant={variant} "
            f"fixture={fixture.semantic_hash} rendered={rendered['semanticHash']}"
        )
    corrections = tuple(rendered.get("corrections", ()))
    if corrections:
        raise RuntimeError(
            f"C3W forbids new H6N correction families: strategy={strategy} "
            f"variant={variant} corrections={corrections}"
        )

    return {
        **rendered,
        "strategy": strategy,
        "c3wAdapterVersion": ADAPTER_VERSION,
        "corrections": corrections,
    }
