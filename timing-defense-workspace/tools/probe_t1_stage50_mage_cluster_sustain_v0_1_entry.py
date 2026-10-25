#!/usr/bin/env python3
"""Entry shim for v0.1 Mage sustain probe.

The probe uses stage_static from the class-rotation shape helper. The initial
probe module referenced it through the integration module, which does not
export that symbol. Bind the already-existing helper explicitly and execute
exactly the same diagnostic logic; no simulation semantics change.
"""
import probe_t1_stage49_50_class_rotation_shape_v0_1 as shape
import probe_t1_stage50_mage_cluster_sustain_v0_1 as probe

probe.integration.shape = shape

if __name__ == "__main__":
    probe.main()
