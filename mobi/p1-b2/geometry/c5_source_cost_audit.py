from __future__ import annotations

import inspect

import c3_renderer_view_resolved_v4 as view_renderer
import c3_renderers as shared_renderer

SOURCE_AUDIT_VERSION = "P1_C5_SOURCE_COST_AUDIT_V1"


def build_source_audit():
    view_source = inspect.getsource(view_renderer._render_h6)
    partition_source = inspect.getsource(shared_renderer.partition_bounds)

    # These are implementation facts, not architecture requirements. They are
    # intentionally surfaced so C5 can separate prototype overhead from the
    # irreducible cost of the representation family.
    full_base_prerender_for_tail = (
        "base_rendered = render_fixture_v3" in view_source
        and "tail_shapes =" in view_source
    )
    view_sort_present = "_sorted_shapes(shapes)" in view_source
    partition_group_filter_scan = (
        "for group in GROUPS" in partition_source
        and "group_shapes = [shape for shape in shapes" in partition_source
    )

    return {
        "version": SOURCE_AUDIT_VERSION,
        "viewResolved": {
            "prototypeFullBasePrerenderForTail": full_base_prerender_for_tail,
            "viewDepthSortPresent": view_sort_present,
            "fullBasePrerenderIsArchitectureRequired": False,
            "viewDepthSortItemCountBoundedBySmallShapeSet": True,
            "productionOptimizationNote": (
                "Reuse the shared tail primitive directly and precompute yaw/view basis; "
                "do not preserve the prototype full-base prerender as a production requirement."
            ),
        },
        "partitionBounds": {
            "currentImplementationFiltersAllShapesPerSemanticGroup": partition_group_filter_scan,
            "semanticGroupCount": len(shared_renderer.GROUPS),
            "groupCountIsArchitectureBounded": True,
            "productionOptimizationNote": (
                "Group-indexed accumulation/coalesced host updates may remove repeated filter scans "
                "without changing partition semantics."
            ),
        },
    }
