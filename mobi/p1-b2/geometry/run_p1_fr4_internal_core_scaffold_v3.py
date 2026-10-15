from __future__ import annotations

import hashlib

from e_v0_fixture_adapter import H6N, H7, iter_invariant_fixtures
import p1_fr3_feline_core_topology_v5 as fr3_v5
import p1_fr4_internal_core_scaffold_v3 as fr4
import run_p1_fr4_internal_core_scaffold as base


RUN_VERSION = "P1_FR4_INTERNAL_CORE_SCAFFOLD_EVIDENCE_V3_SEED_RADIAL"
PRIMARY_SIZE_DP = 80


def run_matrix():
    records = []
    external_topology = set()
    scaffold_signatures = set()
    patch_id_orders = set()
    patch_vertex_count_sets = set()
    semantic_mutations = 0
    max_paw_pin_error = 0.0
    external_self_intersections = 0
    patch_self_intersections = 0
    patch_outside_vertices = 0
    correction_uses = 0
    mesh_domain_counts = set()
    external_core_mismatches = 0
    appendage_mismatches = 0
    stress_fr3_crossings = 0
    stress_fr4_crossings = 0
    stress_records = 0

    for case_id, morphology, size_dp, direction, fixture in iter_invariant_fixtures():
        result = fr4.build_probe(fixture, direction)
        probe = result.base
        control = fr3_v5.build_probe(fixture, direction)
        records.append(base._round_value(fr4.result_dict(result)))
        external_topology.add(probe.topology_signature)
        scaffold_signatures.add(result.scaffold_signature)
        patch_id_orders.add(tuple(patch.id for patch in result.internal_patches))
        patch_vertex_count_sets.add(tuple(len(patch.vertices) for patch in result.internal_patches))
        if probe.semantic_anchor_hash_before != probe.semantic_anchor_hash_after:
            semantic_mutations += 1
        max_paw_pin_error = max(max_paw_pin_error, probe.paw_pin_error_max)
        external_self_intersections += probe.core_self_intersections
        patch_self_intersections += result.patch_self_intersections
        patch_outside_vertices += result.patch_outside_vertex_count
        correction_uses += len(probe.correction_families)
        mesh_domain_counts.add(1 + len(probe.limb_meshes) + 1)
        if probe.core_vertices != control.core_vertices:
            external_core_mismatches += 1
        if (
            probe.ear_shapes != control.ear_shapes
            or probe.limb_meshes != control.limb_meshes
            or probe.tail_mesh != control.tail_mesh
        ):
            appendage_mismatches += 1
        if size_dp == PRIMARY_SIZE_DP and case_id in (H6N, H7):
            stress_fr3_crossings += fr3_v5.limb_crossing_count(control.limb_meshes)
            stress_fr4_crossings += fr3_v5.limb_crossing_count(probe.limb_meshes)
            stress_records += 1

    records.sort(key=lambda r: (r["caseId"], r["morphologyId"], r["sizeDp"], r["direction"], r["t"]))
    record_hash = hashlib.sha256(base.canonical_bytes(records)).hexdigest()
    structural_pass = (
        len(records) == 1770
        and external_topology == {fr3_v5.topology_signature()}
        and len(scaffold_signatures) == 1
        and patch_id_orders == {fr4.PATCH_IDS}
        and patch_vertex_count_sets == {(8, 6, 8)}
        and semantic_mutations == 0
        and max_paw_pin_error <= 1e-9
        and external_self_intersections == 0
        and patch_self_intersections == 0
        and patch_outside_vertices == 0
        and correction_uses == 0
        and mesh_domain_counts == {6}
        and external_core_mismatches == 0
        and appendage_mismatches == 0
    )
    summary = {
        "version": RUN_VERSION,
        "prototypeVersion": fr4.PROTOTYPE_VERSION,
        "recordCount": len(records),
        "externalTopologySignatureCount": len(external_topology),
        "externalTopologySignatures": sorted(external_topology),
        "scaffoldSignatureCount": len(scaffold_signatures),
        "scaffoldSignatures": sorted(scaffold_signatures),
        "patchIdOrders": [list(v) for v in sorted(patch_id_orders)],
        "patchVertexCountSets": [list(v) for v in sorted(patch_vertex_count_sets)],
        "semanticMutationCount": semantic_mutations,
        "maxPawPinError": max_paw_pin_error,
        "externalCoreSelfIntersectionCount": external_self_intersections,
        "patchSelfIntersectionCount": patch_self_intersections,
        "patchOutsideVertexCount": patch_outside_vertices,
        "correctionUseCount": correction_uses,
        "meshDomainCounts": sorted(mesh_domain_counts),
        "externalCoreMismatchVsFr3V5Count": external_core_mismatches,
        "appendageMismatchVsFr3V5Count": appendage_mismatches,
        "stressCrossingRecordCount": stress_records,
        "fr3V5StressLimbCrossingCount": stress_fr3_crossings,
        "fr4StressLimbCrossingCount": stress_fr4_crossings,
        "stressLimbCrossingDeltaVsFr3V5": stress_fr4_crossings - stress_fr3_crossings,
        "recordContentSha256": record_hash,
        "structuralPass": structural_pass,
        "perceptualDisposition": "REQUIRES_DIRECT_REVIEW",
    }
    return records, summary


base.fr4 = fr4
base.RUN_VERSION = RUN_VERSION
base.run_matrix = run_matrix


if __name__ == "__main__":
    base.main()
