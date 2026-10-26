from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.')

def replace_once(rel, old, new):
    p = ROOT / rel
    s = p.read_text()
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{rel}: expected exactly one match, found {n}')
    p.write_text(s.replace(old, new, 1))

aha = 'puzzle-authoring/src/main/java/com/example/einsteingame/authoring/pss/aha/StructuralAhaAnalyzer.java'
replace_once(aha,
'''        List<PathEdge> pending = new ArrayList<>(paths.edges);
        // Topological replay makes annotations independent of a supplied edge collection's order.
        pending.sort(Comparator.comparing((PathEdge e) -> e.sourcePathId).thenComparing(e -> e.targetPathId));
        while (!pending.isEmpty()) {
            boolean progressed = false;
            for (Iterator<PathEdge> it = pending.iterator(); it.hasNext();) {
                PathEdge edge = it.next(); HumanSolutionPath source = histories.get(edge.sourcePathId);
                if (source == null) continue;
                ReasoningState state = states.get(source.terminalStateHash);
                SkillOpportunity actual = find(opportunities(state, paths, ops), edge.opportunity.key);
                if (actual == null || !actual.productive() || !actual.equals(edge.opportunity))
                    throw new IllegalArgumentException("edge is not a current CP2 productive opportunity");
                CanonicalTransition.Result next = CanonicalTransition.apply(state, actual);
                if (!next.step.equals(edge.step) || !next.guards.isEmpty())
                    throw new IllegalArgumentException("CP5 public transition mismatch");
                HumanSolutionPath target = source.append(next.step);
                if (!target.pathId.equals(edge.targetPathId)) throw new IllegalArgumentException("CP5 history mismatch");
                states.put(next.state.semanticHash(), next.state); histories.put(target.pathId, target);
                it.remove(); progressed = true;
            }
            if (!progressed) throw new IllegalArgumentException("disconnected CP5 edges");
        }
''',
'''        // Indexed topological replay preserves supplied-edge order independence without repeatedly rescanning pending edges.
        Map<String,List<PathEdge>> outgoing = new TreeMap<>();
        for (PathEdge edge : paths.edges) outgoing.computeIfAbsent(edge.sourcePathId, x -> new ArrayList<>()).add(edge);
        for (List<PathEdge> edges : outgoing.values()) edges.sort(Comparator.comparing((PathEdge e) -> e.targetPathId).thenComparing(e -> e.edgeId));
        Deque<String> ready = new ArrayDeque<>(); ready.add(root.pathId); int replayedEdges = 0;
        while (!ready.isEmpty()) {
            String sourceId = ready.removeFirst(); HumanSolutionPath source = histories.get(sourceId);
            List<PathEdge> edges = outgoing.remove(sourceId); if (edges == null) continue;
            for (PathEdge edge : edges) {
                ReasoningState state = states.get(source.terminalStateHash);
                SkillOpportunity actual = find(opportunities(state, paths, ops), edge.opportunity.key);
                if (actual == null || !actual.productive() || !actual.equals(edge.opportunity))
                    throw new IllegalArgumentException("edge is not a current CP2 productive opportunity");
                CanonicalTransition.Result next = CanonicalTransition.apply(state, actual);
                if (!next.step.equals(edge.step) || !next.guards.isEmpty())
                    throw new IllegalArgumentException("CP5 public transition mismatch");
                HumanSolutionPath target = source.append(next.step);
                if (!target.pathId.equals(edge.targetPathId)) throw new IllegalArgumentException("CP5 history mismatch");
                states.put(next.state.semanticHash(), next.state); histories.put(target.pathId, target);
                ready.addLast(target.pathId); replayedEdges++;
            }
        }
        if (replayedEdges != paths.edges.size() || !outgoing.isEmpty()) throw new IllegalArgumentException("disconnected CP5 edges");
''')
replace_once(aha,
'        Map<String,List<CascadeLocation>> cascadeLocations = cascadeLocations(paths);',
'        Map<String,Map<String,String>> transitionTargets = transitionTargets(paths);\n        Map<String,List<CascadeLocation>> cascadeLocations = cascadeLocations(paths,root.pathId,transitionTargets);')
replace_once(aha,
'''    private static void validateHistory(HumanSolutionPath path, Map<String,HumanSolutionPath> histories) {
        HumanSolutionPath generated = histories.get(path.pathId);
        if (generated == null || !generated.terminal(path.terminalKind).json().equals(path.json()))
            throw new IllegalArgumentException("ungenerated CP5 witness history");
    }
''',
'''    private static void validateHistory(HumanSolutionPath path, Map<String,HumanSolutionPath> histories) {
        HumanSolutionPath generated = histories.get(path.pathId);
        if (generated == null || !generated.initialStateHash.equals(path.initialStateHash)
                || !generated.terminalStateHash.equals(path.terminalStateHash) || !generated.pathId.equals(path.pathId)
                || !generated.steps.equals(path.steps) || !generated.opportunityKeys.equals(path.opportunityKeys)
                || !generated.stateHashes.equals(path.stateHashes) || !generated.cost.data().equals(path.cost.data()))
            throw new IllegalArgumentException("ungenerated CP5 witness history");
    }
''')
replace_once(aha,
'''    private static Map<String,List<CascadeLocation>> cascadeLocations(PathExplorerResult paths) {
        Map<String,HumanSolutionPath> leaves = new TreeMap<>();
        for (HumanSolutionPath p : paths.solvedPaths) leaves.put(p.pathId,p);
        for (HumanSolutionPath p : paths.terminalStalledPaths) leaves.put(p.pathId,p);
        for (FrontierWitness f : paths.frontier) leaves.put(f.path.pathId,f.path);
        Set<String> targets = new HashSet<>();
        for (PathEdge edge : paths.edges) targets.add(edge.targetPathId);
        Map<String,List<CascadeLocation>> out = new HashMap<>();
        for (HumanSolutionPath leaf : leaves.values()) {
            HumanSolutionPath prefix = HumanSolutionPath.root(leaf.initialStateHash);
            Set<String> indexedForLeaf = new HashSet<>();
            for (int i = 0; i < leaf.steps.size(); i++) {
                prefix = prefix.append(leaf.steps.get(i));
                if (targets.contains(prefix.pathId) && indexedForLeaf.add(prefix.pathId))
                    out.computeIfAbsent(prefix.pathId, x -> new ArrayList<>()).add(new CascadeLocation(leaf,i));
            }
        }
        return out;
    }
''',
'''    private static Map<String,Map<String,String>> transitionTargets(PathExplorerResult paths) {
        Map<String,Map<String,String>> out = new TreeMap<>();
        for (PathEdge edge : paths.edges) {
            Map<String,String> byStep = out.computeIfAbsent(edge.sourcePathId, x -> new TreeMap<>());
            String stepId = edge.step.semanticHash(), prior = byStep.put(stepId,edge.targetPathId);
            if (prior != null && !prior.equals(edge.targetPathId)) throw new IllegalArgumentException("ambiguous CP5 path transition");
        }
        return out;
    }
    private static Map<String,List<CascadeLocation>> cascadeLocations(PathExplorerResult paths,String rootPathId,Map<String,Map<String,String>> transitions) {
        Map<String,HumanSolutionPath> leaves = new TreeMap<>();
        for (HumanSolutionPath p : paths.solvedPaths) leaves.put(p.pathId,p);
        for (HumanSolutionPath p : paths.terminalStalledPaths) leaves.put(p.pathId,p);
        for (FrontierWitness f : paths.frontier) leaves.put(f.path.pathId,f.path);
        Map<String,List<CascadeLocation>> out = new HashMap<>();
        for (HumanSolutionPath leaf : leaves.values()) {
            String prefixId = rootPathId;
            for (int i = 0; i < leaf.steps.size(); i++) {
                Map<String,String> byStep = transitions.get(prefixId);
                String targetId = byStep == null ? null : byStep.get(leaf.steps.get(i).semanticHash());
                if (targetId == null) throw new IllegalArgumentException("missing CP5 prefix transition");
                prefixId = targetId; out.computeIfAbsent(prefixId, x -> new ArrayList<>()).add(new CascadeLocation(leaf,i));
            }
            if (!prefixId.equals(leaf.pathId)) throw new IllegalArgumentException("retained leaf path identity mismatch");
        }
        return out;
    }
''')

diff = 'puzzle-authoring/src/main/java/com/example/einsteingame/authoring/pss/difficulty/StaticDifficultyAnalyzer.java'
replace_once(diff,
'''    private static Map<String,ReasoningState> states(PathExplorerResult paths) {
        Map<String,ReasoningState> out = new TreeMap<>(); out.put(paths.initialStateHash,paths.initialState);
        List<PathEdge> pending = new ArrayList<>(paths.edges);
        while (!pending.isEmpty()) {
            boolean progress = false;
            for (Iterator<PathEdge> it = pending.iterator(); it.hasNext();) {
                PathEdge edge = it.next(); ReasoningState state = out.get(edge.step.beforeStateHash); if (state == null) continue;
                CanonicalTransition.Result next = CanonicalTransition.apply(state,edge.opportunity);
                if (!next.step.equals(edge.step)) throw new IllegalArgumentException("transition provenance mismatch");
                out.put(next.state.semanticHash(),next.state); it.remove(); progress = true;
            }
            if (!progress) throw new IllegalArgumentException("disconnected path states");
        }
        return out;
    }
''',
'''    private static Map<String,ReasoningState> states(PathExplorerResult paths) {
        Map<String,ReasoningState> out = new TreeMap<>(); out.put(paths.initialStateHash,paths.initialState);
        Map<String,List<PathEdge>> outgoing = new TreeMap<>();
        for (PathEdge edge : paths.edges) outgoing.computeIfAbsent(edge.step.beforeStateHash,x->new ArrayList<>()).add(edge);
        for (List<PathEdge> edges : outgoing.values()) edges.sort(Comparator.comparing((PathEdge e)->e.sourcePathId).thenComparing(e->e.targetPathId));
        Deque<String> ready = new ArrayDeque<>(); ready.add(paths.initialStateHash); Set<String> expanded = new HashSet<>(); int replayed = 0;
        while (!ready.isEmpty()) {
            String sourceHash = ready.removeFirst(); if (!expanded.add(sourceHash)) continue;
            ReasoningState state = out.get(sourceHash); List<PathEdge> edges = outgoing.remove(sourceHash); if (edges == null) continue;
            for (PathEdge edge : edges) {
                CanonicalTransition.Result next = CanonicalTransition.apply(state,edge.opportunity);
                if (!next.step.equals(edge.step)) throw new IllegalArgumentException("transition provenance mismatch");
                String nextHash = next.state.semanticHash(); if (!out.containsKey(nextHash)) { out.put(nextHash,next.state); ready.addLast(nextHash); }
                replayed++;
            }
        }
        if (replayed != paths.edges.size() || !outgoing.isEmpty()) throw new IllegalArgumentException("disconnected path states");
        return out;
    }
''')

exp = 'puzzle-authoring/src/main/java/com/example/einsteingame/authoring/pss/experience/ExperienceSimulator.java'
replace_once(exp,
'''        Map<String,SkillOpportunity> generated = new TreeMap<>();
        for (PathEdge e : paths.edges) generated.put(e.step.semanticHash(),e.opportunity);
        Map<String,SortedSet<String>> continuations = new TreeMap<>();
        Map<String,Map<String,Map<String,Object>>> historiesAtState = new TreeMap<>();
        for (HumanSolutionPath p : leaves.values()) {
            HumanSolutionPath prefix = HumanSolutionPath.root(p.initialStateHash);
            recordHistory(historiesAtState,prefix,p.pathId);
            for (HumanStep step : p.steps) {
                continuations.computeIfAbsent(prefix.pathId,k->new TreeSet<>()).add(step.opportunityKey);
                prefix = prefix.append(step); recordHistory(historiesAtState,prefix,p.pathId);
            }
        }
        List<PathExperienceTrace> traces = new ArrayList<>();
        Map<String,List<SkillOpportunity>> opportunityCache = new TreeMap<>();
        for (HumanSolutionPath p : leaves.values()) if (timelines.containsKey(p.pathId))
            traces.add(replay(paths,p,timelines.get(p.pathId),ahaByStep,generated,frontiers.getOrDefault(p.pathId,Collections.emptyList()),continuations,opportunityCache));
''',
'''        Map<String,SkillOpportunity> generated = new TreeMap<>();
        for (PathEdge e : paths.edges) generated.put(e.step.semanticHash(),e.opportunity);
        Map<String,Map<String,String>> transitions = transitionTargets(paths); String rootPathId = HumanSolutionPath.root(paths.initialStateHash).pathId;
        Map<String,List<String>> prefixIdsByPath = new TreeMap<>();
        Map<String,SortedSet<String>> continuations = new TreeMap<>();
        Map<String,Map<String,Map<String,Object>>> historiesAtState = new TreeMap<>();
        for (HumanSolutionPath p : leaves.values()) {
            List<String> prefixIds = prefixPathIds(p,rootPathId,transitions); prefixIdsByPath.put(p.pathId,prefixIds);
            List<String> orderedStepHashes = new ArrayList<>(); recordHistory(historiesAtState,p.initialStateHash,rootPathId,0,orderedStepHashes,p.pathId);
            for (int i = 0; i < p.steps.size(); i++) {
                HumanStep step = p.steps.get(i); String sourceId = prefixIds.get(i), targetId = prefixIds.get(i+1);
                continuations.computeIfAbsent(sourceId,k->new TreeSet<>()).add(step.opportunityKey);
                orderedStepHashes.add(step.semanticHash()); recordHistory(historiesAtState,step.afterStateHash,targetId,i+1,orderedStepHashes,p.pathId);
            }
        }
        List<PathExperienceTrace> traces = new ArrayList<>();
        Map<String,List<SkillOpportunity>> opportunityCache = new TreeMap<>();
        for (HumanSolutionPath p : leaves.values()) if (timelines.containsKey(p.pathId))
            traces.add(replay(paths,p,timelines.get(p.pathId),ahaByStep,generated,prefixIdsByPath.get(p.pathId),frontiers.getOrDefault(p.pathId,Collections.emptyList()),continuations,opportunityCache));
''')
replace_once(exp,
'''    private static void recordHistory(Map<String,Map<String,Map<String,Object>>> all,HumanSolutionPath prefix,String leaf) {
        Map<String,Object> h = all.computeIfAbsent(prefix.terminalStateHash,k->new TreeMap<>()).computeIfAbsent(prefix.pathId,k->CanonicalJson.object(
                "prefixPathId",prefix.pathId,"humanDepth",prefix.steps.size(),"orderedStepHashes",stepHashes(prefix.steps),"supportingRetainedPathIds",new TreeSet<String>()));
        @SuppressWarnings("unchecked") Set<String> support = (Set<String>)h.get("supportingRetainedPathIds"); support.add(leaf);
    }
    private static List<String> stepHashes(List<HumanStep> steps) { List<String> out = new ArrayList<>(); for (HumanStep s : steps) out.add(s.semanticHash()); return out; }
''',
'''    private static Map<String,Map<String,String>> transitionTargets(PathExplorerResult paths) {
        Map<String,Map<String,String>> out = new TreeMap<>();
        for (PathEdge edge : paths.edges) {
            Map<String,String> byStep = out.computeIfAbsent(edge.sourcePathId,x->new TreeMap<>());
            String stepId = edge.step.semanticHash(), prior = byStep.put(stepId,edge.targetPathId);
            if (prior != null && !prior.equals(edge.targetPathId)) throw new IllegalArgumentException("ambiguous Human path transition");
        }
        return out;
    }
    private static List<String> prefixPathIds(HumanSolutionPath path,String rootPathId,Map<String,Map<String,String>> transitions) {
        List<String> out = new ArrayList<>(); String prefixId = rootPathId; out.add(prefixId);
        for (HumanStep step : path.steps) {
            Map<String,String> byStep = transitions.get(prefixId); String targetId = byStep == null ? null : byStep.get(step.semanticHash());
            if (targetId == null) throw new IllegalArgumentException("missing Human prefix transition");
            prefixId = targetId; out.add(prefixId);
        }
        if (!prefixId.equals(path.pathId)) throw new IllegalArgumentException("retained Human path identity mismatch");
        return Collections.unmodifiableList(out);
    }
    private static void recordHistory(Map<String,Map<String,Map<String,Object>>> all,String stateHash,String prefixId,int depth,List<String> orderedStepHashes,String leaf) {
        Map<String,Object> h = all.computeIfAbsent(stateHash,k->new TreeMap<>()).computeIfAbsent(prefixId,k->CanonicalJson.object(
                "prefixPathId",prefixId,"humanDepth",depth,"orderedStepHashes",new ArrayList<>(orderedStepHashes),"supportingRetainedPathIds",new TreeSet<String>()));
        @SuppressWarnings("unchecked") Set<String> support = (Set<String>)h.get("supportingRetainedPathIds"); support.add(leaf);
    }
''')
replace_once(exp,
'''            Map<String,SkillOpportunity> generated,List<FrontierWitness> frontier,Map<String,SortedSet<String>> continuations,Map<String,List<SkillOpportunity>> cache) {
        ReasoningState current = paths.initialState; HumanSolutionPath prefix = HumanSolutionPath.root(path.initialStateHash);
''',
'''            Map<String,SkillOpportunity> generated,List<String> prefixIds,List<FrontierWitness> frontier,Map<String,SortedSet<String>> continuations,Map<String,List<SkillOpportunity>> cache) {
        ReasoningState current = paths.initialState;
''')
replace_once(exp,
'''        for (int i = 0; i < path.steps.size(); i++) {
            HumanStep step = path.steps.get(i); SkillOpportunity op = generated.get(step.semanticHash());
''',
'''        for (int i = 0; i < path.steps.size(); i++) {
            String prefixId = prefixIds.get(i); HumanStep step = path.steps.get(i); SkillOpportunity op = generated.get(step.semanticHash());
''')
p = ROOT / exp
s = p.read_text()
if s.count('prefix.pathId') != 3:
    raise SystemExit(f'{exp}: expected 3 prefix.pathId uses, found {s.count("prefix.pathId")}')
s = s.replace('prefix.pathId','prefixId')
s = s.replace('            progress.add(cadence); prefix = prefix.append(step); current = next.state;',
              '            progress.add(cadence); current = next.state;')
p.write_text(s)

print('P1_PATCH_APPLIED=PASS')
