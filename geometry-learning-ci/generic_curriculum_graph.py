"""Public-safe generic directed-learning-graph validator; synthetic data only.

This module knows nothing about GeometryLearningProgram problem IDs, bank,
learner profiles, proprietary lesson content or stage names.
"""


def verify_graph(*, nodes, observation_nodes, actual_mandatory, proposed_mandatory,
                 optional_bridges):
    nodes=set(nodes)
    obs=set(observation_nodes)
    vertices=nodes|obs
    actual=set(actual_mandatory)
    proposed=list(proposed_mandatory)
    bridges=list(optional_bridges)
    if not nodes or not obs:
        raise ValueError("Missing synthetic nodes")
    if len(proposed)!=len(set(proposed)) or set(proposed)!=actual:
        raise ValueError("Mandatory edge inventory mismatch")
    if len(bridges)!=len(set(bridges)):
        raise ValueError("Duplicate advisory edge")
    if set(bridges)&actual:
        raise ValueError("Advisory bridge must not duplicate a mandatory edge")
    all_edges=actual|set(bridges)
    incoming={n:0 for n in vertices}
    children={n:[] for n in vertices}
    for src,dst in all_edges:
        if src not in vertices or dst not in nodes or src==dst:
            raise ValueError("Graph endpoint invalid")
        children[src].append(dst)
        incoming[dst]+=1
    q=[n for n in vertices if incoming[n]==0]
    visited=0
    while q:
        n=q.pop()
        visited+=1
        for child in children[n]:
            incoming[child]-=1
            if incoming[child]==0:
                q.append(child)
    if visited!=len(vertices):
        raise ValueError("Cycle in proposed educational graph")
    return {"status":"PASS_PUBLIC_SYNTHETIC_DAG_RULES_ONLY",
            "nodes":len(nodes),"mandatory":len(actual),"advice":len(bridges),
            "observation":len(obs)}
