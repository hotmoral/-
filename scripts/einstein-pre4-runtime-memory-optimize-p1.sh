#!/usr/bin/env bash
set -euo pipefail
: "${BASE_SHA:?}"; : "${CANDIDATE_BRANCH:?}"; : "${BASE_CLASSES:?}"; : "${CANDIDATE_CLASSES:?}"
test "$(git -C EinsteinGame rev-parse HEAD)" = "$BASE_SHA"
cp -a EinsteinGame Baseline
git -C EinsteinGame switch -c "$CANDIDATE_BRANCH"
cd EinsteinGame
python3 - <<'PY'
from pathlib import Path

def replace_once(path, old, new):
    p=Path(path); s=p.read_text(); n=s.count(old)
    if n != 1: raise SystemExit(f'{path}: expected one match, found {n}: {old[:120]!r}')
    p.write_text(s.replace(old,new,1))

# CP8: replace repeated pending-list rescans with source-path indexed topological traversal.
p='puzzle-authoring/src/main/java/com/example/einsteingame/authoring/pss/aha/StructuralAhaAnalyzer.java'
old='''        Map<String,List<SkillOpportunity>> ops = new TreeMap<>();
        List<PathEdge> pending = new ArrayList<>(paths.edges);
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
        }'''
new='''        Map<String,List<SkillOpportunity>> ops = new TreeMap<>();
        List<PathEdge> orderedEdges = new ArrayList<>(paths.edges);
        orderedEdges.sort(Comparator.comparing((PathEdge e) -> e.sourcePathId).thenComparing(e -> e.targetPathId));
        Map<String,List<PathEdge>> outgoing = new TreeMap<>();
        for (PathEdge edge : orderedEdges) outgoing.computeIfAbsent(edge.sourcePathId, x -> new ArrayList<>()).add(edge);
        ArrayDeque<HumanSolutionPath> ready = new ArrayDeque<>(); ready.add(root);
        Set<String> replayedSources = new HashSet<>(); int replayedEdgeCount = 0;
        // Path identity strictly extends by one Human step, so source-indexed traversal is topological without rescanning unrelated edges.
        while (!ready.isEmpty()) {
            HumanSolutionPath source = ready.removeFirst();
            if (!replayedSources.add(source.pathId)) continue;
            ReasoningState state = states.get(source.terminalStateHash);
            for (PathEdge edge : outgoing.getOrDefault(source.pathId, Collections.emptyList())) {
                SkillOpportunity actual = find(opportunities(state, paths, ops), edge.opportunity.key);
                if (actual == null || !actual.productive() || !actual.equals(edge.opportunity))
                    throw new IllegalArgumentException("edge is not a current CP2 productive opportunity");
                CanonicalTransition.Result next = CanonicalTransition.apply(state, actual);
                if (!next.step.equals(edge.step) || !next.guards.isEmpty())
                    throw new IllegalArgumentException("CP5 public transition mismatch");
                HumanSolutionPath target = source.append(next.step);
                if (!target.pathId.equals(edge.targetPathId)) throw new IllegalArgumentException("CP5 history mismatch");
                states.put(next.state.semanticHash(), next.state);
                HumanSolutionPath prior = histories.put(target.pathId, target);
                if (prior == null) ready.addLast(target);
                else if (!prior.json().equals(target.json())) throw new IllegalArgumentException("conflicting CP5 history identity");
                replayedEdgeCount++;
            }
        }
        if (replayedEdgeCount != paths.edges.size()) throw new IllegalArgumentException("disconnected CP5 edges");'''
replace_once(p,old,new)
replace_once(p,'        Map<String,List<CascadeLocation>> cascadeLocations = cascadeLocations(paths);',
               '        Map<String,List<CascadeLocation>> cascadeLocations = cascadeLocations(paths,outgoing);')
old='''    private static Map<String,List<CascadeLocation>> cascadeLocations(PathExplorerResult paths) {
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
    }'''
new='''    private static Map<String,List<CascadeLocation>> cascadeLocations(PathExplorerResult paths, Map<String,List<PathEdge>> outgoing) {
        Map<String,HumanSolutionPath> leaves = new TreeMap<>();
        for (HumanSolutionPath p : paths.solvedPaths) leaves.put(p.pathId,p);
        for (HumanSolutionPath p : paths.terminalStalledPaths) leaves.put(p.pathId,p);
        for (FrontierWitness f : paths.frontier) leaves.put(f.path.pathId,f.path);
        Set<String> targets = new HashSet<>();
        for (PathEdge edge : paths.edges) targets.add(edge.targetPathId);
        Map<String,List<CascadeLocation>> out = new HashMap<>();
        String rootPathId = HumanSolutionPath.root(paths.initialStateHash).pathId;
        for (HumanSolutionPath leaf : leaves.values()) {
            String prefixPathId = rootPathId; Set<String> indexedForLeaf = new HashSet<>();
            for (int i = 0; i < leaf.steps.size(); i++) {
                PathEdge edge = pathEdge(outgoing,prefixPathId,leaf.steps.get(i)); prefixPathId = edge.targetPathId;
                if (targets.contains(prefixPathId) && indexedForLeaf.add(prefixPathId))
                    out.computeIfAbsent(prefixPathId, x -> new ArrayList<>()).add(new CascadeLocation(leaf,i));
            }
        }
        return out;
    }
    private static PathEdge pathEdge(Map<String,List<PathEdge>> outgoing, String sourcePathId, HumanStep step) {
        for (PathEdge edge : outgoing.getOrDefault(sourcePathId, Collections.emptyList()))
            if (edge.opportunity.key.equals(step.opportunityKey) && edge.step.equals(step)) return edge;
        throw new IllegalArgumentException("retained path is disconnected from CP5 edges");
    }'''
replace_once(p,old,new)

# CP9: state-hash indexed replay processes each edge once instead of rescanning pending edges.
p='puzzle-authoring/src/main/java/com/example/einsteingame/authoring/pss/difficulty/StaticDifficultyAnalyzer.java'
old='''    private static Map<String,ReasoningState> states(PathExplorerResult paths) {
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
    }'''
new='''    private static Map<String,ReasoningState> states(PathExplorerResult paths) {
        Map<String,ReasoningState> out = new TreeMap<>(); out.put(paths.initialStateHash,paths.initialState);
        List<PathEdge> ordered = new ArrayList<>(paths.edges);
        ordered.sort(Comparator.comparing((PathEdge e) -> e.sourcePathId).thenComparing(e -> e.targetPathId));
        Map<String,List<PathEdge>> byBeforeState = new HashMap<>();
        for (PathEdge edge : ordered) byBeforeState.computeIfAbsent(edge.step.beforeStateHash,x->new ArrayList<>()).add(edge);
        ArrayDeque<String> ready = new ArrayDeque<>(); ready.add(paths.initialStateHash);
        Set<String> expanded = new HashSet<>(); int replayed = 0;
        while (!ready.isEmpty()) {
            String beforeHash = ready.removeFirst(); if (!expanded.add(beforeHash)) continue;
            ReasoningState state = out.get(beforeHash);
            for (PathEdge edge : byBeforeState.getOrDefault(beforeHash,Collections.emptyList())) {
                CanonicalTransition.Result next = CanonicalTransition.apply(state,edge.opportunity);
                if (!next.step.equals(edge.step)) throw new IllegalArgumentException("transition provenance mismatch");
                String afterHash = next.state.semanticHash(); ReasoningState prior = out.put(afterHash,next.state);
                if (prior == null) ready.addLast(afterHash); replayed++;
            }
        }
        if (replayed != paths.edges.size()) throw new IllegalArgumentException("disconnected path states");
        return out;
    }'''
replace_once(p,old,new)

# CP10: derive retained prefix identities from already-verified CP5 edges instead of re-hashing every prefix history.
p='puzzle-authoring/src/main/java/com/example/einsteingame/authoring/pss/experience/ExperienceSimulator.java'
old='''        Map<String,SortedSet<String>> continuations = new TreeMap<>();
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
            traces.add(replay(paths,p,timelines.get(p.pathId),ahaByStep,generated,frontiers.getOrDefault(p.pathId,Collections.emptyList()),continuations,opportunityCache));'''
new='''        Map<String,SortedSet<String>> continuations = new TreeMap<>();
        Map<String,Map<String,Map<String,Object>>> historiesAtState = new TreeMap<>();
        Map<String,List<PathEdge>> outgoing = pathEdges(paths);
        Map<String,List<String>> prefixIdsByLeaf = new TreeMap<>();
        String rootPathId = HumanSolutionPath.root(paths.initialStateHash).pathId;
        for (HumanSolutionPath p : leaves.values()) {
            List<String> prefixIds = new ArrayList<>(); prefixIds.add(rootPathId);
            List<String> prefixStepHashes = new ArrayList<>();
            recordHistory(historiesAtState,p.initialStateHash,rootPathId,prefixStepHashes,p.pathId);
            for (HumanStep step : p.steps) {
                String sourcePathId = prefixIds.get(prefixIds.size()-1);
                continuations.computeIfAbsent(sourcePathId,k->new TreeSet<>()).add(step.opportunityKey);
                PathEdge edge = pathEdge(outgoing,sourcePathId,step); prefixIds.add(edge.targetPathId);
                prefixStepHashes.add(step.semanticHash());
                recordHistory(historiesAtState,step.afterStateHash,edge.targetPathId,prefixStepHashes,p.pathId);
            }
            prefixIdsByLeaf.put(p.pathId,Collections.unmodifiableList(prefixIds));
        }
        List<PathExperienceTrace> traces = new ArrayList<>();
        Map<String,List<SkillOpportunity>> opportunityCache = new TreeMap<>();
        for (HumanSolutionPath p : leaves.values()) if (timelines.containsKey(p.pathId))
            traces.add(replay(paths,p,timelines.get(p.pathId),ahaByStep,generated,frontiers.getOrDefault(p.pathId,Collections.emptyList()),continuations,opportunityCache,prefixIdsByLeaf.get(p.pathId)));'''
replace_once(p,old,new)
old='''    private static void recordHistory(Map<String,Map<String,Map<String,Object>>> all,HumanSolutionPath prefix,String leaf) {
        Map<String,Object> h = all.computeIfAbsent(prefix.terminalStateHash,k->new TreeMap<>()).computeIfAbsent(prefix.pathId,k->CanonicalJson.object(
                "prefixPathId",prefix.pathId,"humanDepth",prefix.steps.size(),"orderedStepHashes",stepHashes(prefix.steps),"supportingRetainedPathIds",new TreeSet<String>()));
        @SuppressWarnings("unchecked") Set<String> support = (Set<String>)h.get("supportingRetainedPathIds"); support.add(leaf);
    }
    private static List<String> stepHashes(List<HumanStep> steps) { List<String> out = new ArrayList<>(); for (HumanStep s : steps) out.add(s.semanticHash()); return out; }'''
new='''    private static void recordHistory(Map<String,Map<String,Map<String,Object>>> all,String stateHash,String prefixPathId,List<String> stepHashes,String leaf) {
        Map<String,Object> h = all.computeIfAbsent(stateHash,k->new TreeMap<>()).computeIfAbsent(prefixPathId,k->CanonicalJson.object(
                "prefixPathId",prefixPathId,"humanDepth",stepHashes.size(),"orderedStepHashes",new ArrayList<>(stepHashes),"supportingRetainedPathIds",new TreeSet<String>()));
        @SuppressWarnings("unchecked") Set<String> support = (Set<String>)h.get("supportingRetainedPathIds"); support.add(leaf);
    }
    private static Map<String,List<PathEdge>> pathEdges(PathExplorerResult paths) {
        List<PathEdge> ordered = new ArrayList<>(paths.edges);
        ordered.sort(Comparator.comparing((PathEdge e)->e.sourcePathId).thenComparing(e->e.targetPathId));
        Map<String,List<PathEdge>> out = new TreeMap<>();
        for (PathEdge edge : ordered) out.computeIfAbsent(edge.sourcePathId,k->new ArrayList<>()).add(edge);
        return out;
    }
    private static PathEdge pathEdge(Map<String,List<PathEdge>> outgoing,String sourcePathId,HumanStep step) {
        for (PathEdge edge : outgoing.getOrDefault(sourcePathId,Collections.emptyList()))
            if (edge.opportunity.key.equals(step.opportunityKey) && edge.step.equals(step)) return edge;
        throw new IllegalArgumentException("retained path is disconnected from CP5 edges");
    }'''
replace_once(p,old,new)
replace_once(p,'            Map<String,SkillOpportunity> generated,List<FrontierWitness> frontier,Map<String,SortedSet<String>> continuations,Map<String,List<SkillOpportunity>> cache) {\n        ReasoningState current = paths.initialState; HumanSolutionPath prefix = HumanSolutionPath.root(path.initialStateHash);',
               '            Map<String,SkillOpportunity> generated,List<FrontierWitness> frontier,Map<String,SortedSet<String>> continuations,Map<String,List<SkillOpportunity>> cache,List<String> prefixIds) {\n        ReasoningState current = paths.initialState;\n        if (prefixIds == null || prefixIds.size() != path.steps.size()+1) throw new IllegalArgumentException("invalid retained prefix index");')
replace_once(p,'"observedContinuationKeysAtHistory",continuations.getOrDefault(prefix.pathId,new TreeSet<>()),',
               '"observedContinuationKeysAtHistory",continuations.getOrDefault(prefixIds.get(i),new TreeSet<>()),')
replace_once(p,'frames.add(CanonicalJson.object("humanFrameIndex",i,"humanStep",step.data(),"humanStepHash",step.semanticHash(),"sourceHistoryId",prefix.pathId,',
               'frames.add(CanonicalJson.object("humanFrameIndex",i,"humanStep",step.data(),"humanStepHash",step.semanticHash(),"sourceHistoryId",prefixIds.get(i),')
replace_once(p,'for (Object occurrence : list(a.get("occurrences"))) if (map(occurrence).get("sourcePathId").equals(prefix.pathId)) {',
               'for (Object occurrence : list(a.get("occurrences"))) if (map(occurrence).get("sourcePathId").equals(prefixIds.get(i))) {')
replace_once(p,'            progress.add(cadence); prefix = prefix.append(step); current = next.state;',
               '            progress.add(cadence); current = next.state;')
PY

git diff --check
git diff --stat
test -z "$(git diff --name-only "$BASE_SHA" -- puzzle-authoring/src/main/java/com/example/einsteingame/authoring/pss/acquisition)"
mapfile -t delta < <(git diff --name-only "$BASE_SHA" | sort)
test "${#delta[@]}" -eq 3

cd ..
compile_repo(){ repo="$1" out="$2" src="/tmp/$(basename "$out")-sources.txt"; rm -rf "$out" "$src"; mkdir -p "$out"; find "$repo/puzzle-core/src/main/java" "$repo/puzzle-authoring/src/main/java" -type f -name '*.java' -print | sort > "$src"; find "$repo/puzzle-authoring/src/test/java/com/example/einsteingame/authoring/pss" -type f -name '*.java' -print | sort >> "$src"; java -Xmx2g -m jdk.compiler/com.sun.tools.javac.Main -encoding UTF-8 --release 8 -d "$out" "@$src"; }
compile_repo Baseline "$BASE_CLASSES"
compile_repo EinsteinGame "$CANDIDATE_CLASSES"
python3 - <<'PY'
from pathlib import Path
import struct
for root in ['/tmp/einstein-pre4-p1-base-classes','/tmp/einstein-pre4-p1-candidate-classes']:
 files=list(Path(root).rglob('*.class')); assert files
 assert all(struct.unpack('>IHH',p.read_bytes()[:8])==(0xCAFEBABE,0,52) for p in files)
 print('JAVA8_CLASSFILE_TARGET=PASS root='+root+' count='+str(len(files)))
PY
run_suite(){ repo="$1" cp="$2" tag="$3"; rm -rf "$repo/build/pss-logical-core"; (cd "$repo" && /usr/bin/time -f '%e' -o "/tmp/${tag}-aha.time" java -Xmx2g -cp "$cp" com.example.einsteingame.authoring.pss.PssAhaTest > "/tmp/${tag}-aha.log"); (cd "$repo" && /usr/bin/time -f '%e' -o "/tmp/${tag}-difficulty.time" java -Xmx2g -cp "$cp" com.example.einsteingame.authoring.pss.PssDifficultyTest > "/tmp/${tag}-difficulty.log"); (cd "$repo" && /usr/bin/time -f '%e' -o "/tmp/${tag}-experience.time" java -Xmx2g -cp "$cp" com.example.einsteingame.authoring.pss.PssExperienceTest > "/tmp/${tag}-experience.log"); }
run_suite Baseline "$BASE_CLASSES" base
run_suite EinsteinGame "$CANDIDATE_CLASSES" candidate
diff -u /tmp/base-aha.log /tmp/candidate-aha.log
diff -u /tmp/base-difficulty.log /tmp/candidate-difficulty.log
diff -u /tmp/base-experience.log /tmp/candidate-experience.log
diff -qr Baseline/build/pss-logical-core EinsteinGame/build/pss-logical-core
printf 'P1_BASE_AHA_SECONDS=%s\n' "$(cat /tmp/base-aha.time)"; printf 'P1_CANDIDATE_AHA_SECONDS=%s\n' "$(cat /tmp/candidate-aha.time)"; printf 'P1_BASE_DIFFICULTY_SECONDS=%s\n' "$(cat /tmp/base-difficulty.time)"; printf 'P1_CANDIDATE_DIFFICULTY_SECONDS=%s\n' "$(cat /tmp/candidate-difficulty.time)"; printf 'P1_BASE_EXPERIENCE_SECONDS=%s\n' "$(cat /tmp/base-experience.time)"; printf 'P1_CANDIDATE_EXPERIENCE_SECONDS=%s\n' "$(cat /tmp/candidate-experience.time)"
cd EinsteinGame
java -Xmx2g -cp "$CANDIDATE_CLASSES" com.example.einsteingame.authoring.pss.PssPathExplorerTest | tee /tmp/pre4-p1-path.log
cd puzzle-authoring
java -Xmx2g -cp "$CANDIDATE_CLASSES" com.example.einsteingame.authoring.pss.acquisition.IntentAcquisitionTest | tee /tmp/pre4-p1-ia1.log
java -Xmx2g -cp "$CANDIDATE_CLASSES" com.example.einsteingame.authoring.pss.acquisition.IntentAcquisitionIA2Test | tee /tmp/pre4-p1-ia2.log
java -Xmx2g -cp "$CANDIDATE_CLASSES" com.example.einsteingame.authoring.pss.acquisition.IntentAcquisitionIA3Test | tee /tmp/pre4-p1-ia3.log
java -Xmx2g -cp "$CANDIDATE_CLASSES" com.example.einsteingame.authoring.pss.acquisition.IntentAcquisitionCheckpointTest | tee /tmp/pre4-p1-checkpoint.log
grep -F 'IntentAcquisitionTest PASS assertions=22' /tmp/pre4-p1-ia1.log
grep -F 'IntentAcquisitionIA2Test PASS assertions=33' /tmp/pre4-p1-ia2.log
grep -F 'IntentAcquisitionIA3Test PASS assertions=43' /tmp/pre4-p1-ia3.log
grep -F 'IntentAcquisitionCheckpointTest PASS assertions=12' /tmp/pre4-p1-checkpoint.log
cd ..
git config user.name 'Einstein Zero-Draw Optimization'
git config user.email 'noreply@localhost'
git add puzzle-authoring/src/main/java
mapfile -t changed < <(git diff --cached --name-only | sort); printf '%s\n' "${changed[@]}"; test "${#changed[@]}" -eq 3
git commit -m 'perf: index retained path replay and prefix identities'
CANDIDATE_SHA="$(git rev-parse HEAD)"; test "$(git rev-parse HEAD^)" = "$BASE_SHA"
git push origin "HEAD:refs/heads/$CANDIDATE_BRANCH"
test "$(git ls-remote origin "refs/heads/$CANDIDATE_BRANCH" | cut -f1)" = "$CANDIDATE_SHA"
printf 'P1_CANDIDATE_SHA=%s\n' "$CANDIDATE_SHA"
echo 'formalAcquisitionInvocation=0'; echo 'privateEvidenceWrite=0'; echo 'EINSTEIN_PRE4_P1_TRAVERSAL_OPTIMIZATION_ZERO_DRAW=PASS'
