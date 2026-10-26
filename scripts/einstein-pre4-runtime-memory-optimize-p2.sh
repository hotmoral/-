#!/usr/bin/env bash
set -euo pipefail
: "${BASE_SHA:?}"; : "${CANDIDATE_BRANCH:?}"; : "${BASE_CLASSES:?}"; : "${CANDIDATE_CLASSES:?}"
test "$(git -C EinsteinGame rev-parse HEAD)" = "$BASE_SHA"
cp -a EinsteinGame Baseline
git -C EinsteinGame switch -c "$CANDIDATE_BRANCH"
cd EinsteinGame
python3 - <<'PY'
from pathlib import Path
p=Path('puzzle-authoring/src/main/java/com/example/einsteingame/authoring/pss/aha/StructuralAhaAnalyzer.java')
s=p.read_text()
def rep(old,new):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'expected one match, found {n}: {old[:140]!r}')
    s=s.replace(old,new,1)

rep('''        // State deduplication is annotation caching only; every history/occurrence remains in evidence.
        for (ReasoningState state : states.values()) opportunities(state, paths, ops);''','''        // State deduplication is annotation caching only; every history/occurrence remains in evidence.
        for (ReasoningState state : states.values()) opportunities(state, paths, ops);
        EvidenceCache evidenceCache = new EvidenceCache(states,ops);
        PathSupportIndex pathSupportIndex = new PathSupportIndex(histories,evidenceCache);''')
rep('''            Map<String,Object> delta = delta(states.get(trigger.step.beforeStateHash), states.get(trigger.step.afterStateHash));
            Map<String,Object> expansion = expansion(ops.get(trigger.step.beforeStateHash), ops.get(trigger.step.afterStateHash));''','''            Map<String,Object> delta = evidenceCache.delta(trigger.step);
            Map<String,Object> expansion = evidenceCache.expansion(trigger.step);''')
rep('''                    context.add(CanonicalJson.object("step", previous.data(), "compression", delta(states.get(previous.beforeStateHash), states.get(previous.afterStateHash)),
                            "expansion", expansion(ops.get(previous.beforeStateHash), ops.get(previous.afterStateHash))));''','''                    context.add(CanonicalJson.object("step", previous.data(), "compression", evidenceCache.delta(previous),
                            "expansion", evidenceCache.expansion(previous)));''')
rep('''                        "cascadeWitnesses", cascades(occurrence, paths, states, ops, cascadeLocations)));''','''                        "cascadeWitnesses", cascades(occurrence, paths, states, ops, cascadeLocations, evidenceCache)));''')
rep('''                    "pathCoverageCompleteness", paths.completeness.name(), "alternatePathSupport", pathSupport(trigger, paths, histories, states, ops),''','''                    "pathCoverageCompleteness", paths.completeness.name(), "alternatePathSupport", pathSupport(trigger, paths, pathSupportIndex),''')

old='''    private static Set<String> effects(SkillOpportunity op) {
        Set<String> out = new TreeSet<>();
        for (CandidateElimination e : op.candidateEliminations) out.add("C:" + e.json());
        for (RelationConsequence r : op.derivedRelations) out.add("R:" + r.fact.json());
        return out;
    }
    private static Set<String> gained(SkillOpportunity after, SkillOpportunity before) {
        Set<String> out = effects(after); if (before != null) out.removeAll(effects(before)); return out;
    }
    private static Map<String,Object> expansion(List<SkillOpportunity> before, List<SkillOpportunity> after) {
        Map<String,SkillOpportunity> b = productive(before), a = productive(after);
        List<Object> created = new ArrayList<>(); List<String> keys = new ArrayList<>(), strengthened = new ArrayList<>(), lost = new ArrayList<>();
        Set<String> previousUnion = new TreeSet<>(); for (SkillOpportunity op : b.values()) previousUnion.addAll(effects(op));
        int novel = 0, atomicNovel = 0;
        for (SkillOpportunity op : a.values()) {
            Set<String> gain = gained(op, b.get(op.key)); if (gain.isEmpty()) continue;
            List<String> previousAlternatives = new ArrayList<>(), previousPartialAlternatives = new ArrayList<>();
            for (SkillOpportunity alternative : b.values()) {
                Set<String> effects = effects(alternative);
                if (effects.containsAll(gain)) previousAlternatives.add(alternative.key);
                if (!Collections.disjoint(effects,gain)) previousPartialAlternatives.add(alternative.key);
            }
            if (previousAlternatives.isEmpty()) novel++;
            Set<String> unavailable = new TreeSet<>(gain); unavailable.removeAll(previousUnion); if (!unavailable.isEmpty()) atomicNovel++;
            if (b.containsKey(op.key)) strengthened.add(op.key); else keys.add(op.key);
            created.add(CanonicalJson.object("opportunity", op.data(), "newConsequences", gain,
                    "change", b.containsKey(op.key) ? "STRENGTHENED" : "NEW_PRODUCTIVE",
                    "previousFullConsequenceAlternativeKeys", previousAlternatives, "previousPartialConsequenceAlternativeKeys",previousPartialAlternatives,
                    "previousConsequenceUnionCoversGain",unavailable.isEmpty(),"newConsequenceAtomsNotPreviouslyAvailable",unavailable));
        }
        for (String key : b.keySet()) if (!a.containsKey(key)) lost.add(key);
        return CanonicalJson.object("newlyAvailableProductiveOpportunityCount", created.size(), "newlyAvailableOpportunityKeys", keys,
                "strengthenedOpportunityKeys", strengthened, "opportunityExpansionEvidence", created,
                "noPreviousSingleOpportunityExplanationCount", novel, "newConsequenceAtomOpportunityCount",atomicNovel,
                "lostOpportunityCount", lost.size(), "lostOpportunityKeys", lost,
                "beforeProductiveOpportunityCount", b.size(), "afterProductiveOpportunityCount", a.size(), "immediateBranchingChange", a.size() - b.size());
    }
    private static Map<String,Object> delta(ReasoningState before, ReasoningState after) {
        int raw = 0, base = 0, display = 0, resolvedBase = 0, resolvedDisplay = 0;
        for (int r = 0; r < before.player.rowCount; r++) for (int s = 0; s < before.player.boardSize; s++) {
            raw += Integer.bitCount(before.player.rawDomain(r,s)) - Integer.bitCount(after.player.rawDomain(r,s));
            int b = Integer.bitCount(before.player.baseEffectiveDomain(r,s)), a = Integer.bitCount(after.player.baseEffectiveDomain(r,s));
            base += b - a; if (b > 1 && a == 1) resolvedBase++;
            b = Integer.bitCount(before.player.displayDomain(r,s)); a = Integer.bitCount(after.player.displayDomain(r,s));
            display += b - a; if (b > 1 && a == 1) resolvedDisplay++;
        }
        return CanonicalJson.object("rawDomainExcessReduction", raw, "baseDomainExcessReduction", base,
                "publicDisplayDomainExcessReduction", display, "resolvedBaseCellCount", resolvedBase,
                "resolvedPublicCellCount", resolvedDisplay, "establishedRelationDelta", after.facts.size() - before.facts.size());
    }
    private static Map<String,Object> pathSupport(PathEdge trigger, PathExplorerResult paths, Map<String,HumanSolutionPath> histories,
                                                   Map<String,ReasoningState> states, Map<String,List<SkillOpportunity>> ops) {
        List<String> used = new ArrayList<>(), exactUsed = new ArrayList<>(), bypass = new ArrayList<>(), sameState = new ArrayList<>(); List<Object> bypassCosts = new ArrayList<>();
        for (HumanSolutionPath path : paths.solvedPaths) {
            if (path.steps.contains(trigger.step)) exactUsed.add(path.pathId);
            if (path.opportunityKeys.contains(trigger.opportunity.key)) used.add(path.pathId);
            else {
                bypass.add(path.pathId); List<Object> steps = new ArrayList<>();
                for (HumanStep step : path.steps) steps.add(CanonicalJson.object("humanStep",step.data(),
                        "compression",delta(states.get(step.beforeStateHash),states.get(step.afterStateHash)),
                        "expansion",expansion(ops.get(step.beforeStateHash),ops.get(step.afterStateHash))));
                bypassCosts.add(CanonicalJson.object("pathId", path.pathId, "rawCost", path.cost.data(),"alternateStructuralSteps",steps));
            }
        }
        for (HumanSolutionPath history : histories.values()) if (history.terminalStateHash.equals(trigger.step.beforeStateHash)) sameState.add(history.pathId);
        Collections.sort(used); Collections.sort(exactUsed); Collections.sort(bypass); Collections.sort(sameState);
        bypassCosts.sort(Comparator.comparing(CanonicalJson::write));
        String uniqueness = !bypass.isEmpty() ? "NOT_UNIQUE_PROVEN" : paths.completeness != PathExplorerResult.Completeness.COMPLETE
                ? "UNKNOWN" : used.isEmpty() ? "NO_SOLVED_PATH" : "ALL_SOLVED_PATHS_USE_KEY_PROVEN";
        return CanonicalJson.object("identityScope", "OPPORTUNITY_KEY_ACROSS_STATES", "solvedPathIdsUsingTrigger", used,
                "exactStateAndStepSolvedPathIds",exactUsed,
                "solvedPathIdsWithoutTrigger", bypass, "bypassRawCosts", bypassCosts, "sameSourceStateHistoryIds", sameState,
                "triggerUniqueness", uniqueness, "coverage", paths.completeness.name());
    }'''
new='''    private static Set<String> computeEffects(SkillOpportunity op) {
        Set<String> out = new TreeSet<>();
        for (CandidateElimination e : op.candidateEliminations) out.add("C:" + e.json());
        for (RelationConsequence r : op.derivedRelations) out.add("R:" + r.fact.json());
        return Collections.unmodifiableSet(out);
    }
    private static Map<String,Object> computeExpansion(String beforeHash, String afterHash, EvidenceCache cache) {
        Map<String,SkillOpportunity> b = cache.productive(beforeHash), a = cache.productive(afterHash);
        List<Object> created = new ArrayList<>(); List<String> keys = new ArrayList<>(), strengthened = new ArrayList<>(), lost = new ArrayList<>();
        Set<String> previousUnion = new TreeSet<>(); for (SkillOpportunity op : b.values()) previousUnion.addAll(cache.effects(op));
        int novel = 0, atomicNovel = 0;
        for (SkillOpportunity op : a.values()) {
            Set<String> gain = cache.gained(op, b.get(op.key)); if (gain.isEmpty()) continue;
            List<String> previousAlternatives = new ArrayList<>(), previousPartialAlternatives = new ArrayList<>();
            for (SkillOpportunity alternative : b.values()) {
                Set<String> effects = cache.effects(alternative);
                if (effects.containsAll(gain)) previousAlternatives.add(alternative.key);
                if (!Collections.disjoint(effects,gain)) previousPartialAlternatives.add(alternative.key);
            }
            if (previousAlternatives.isEmpty()) novel++;
            Set<String> unavailable = new TreeSet<>(gain); unavailable.removeAll(previousUnion); if (!unavailable.isEmpty()) atomicNovel++;
            if (b.containsKey(op.key)) strengthened.add(op.key); else keys.add(op.key);
            created.add(CanonicalJson.object("opportunity", op.data(), "newConsequences", gain,
                    "change", b.containsKey(op.key) ? "STRENGTHENED" : "NEW_PRODUCTIVE",
                    "previousFullConsequenceAlternativeKeys", previousAlternatives, "previousPartialConsequenceAlternativeKeys",previousPartialAlternatives,
                    "previousConsequenceUnionCoversGain",unavailable.isEmpty(),"newConsequenceAtomsNotPreviouslyAvailable",unavailable));
        }
        for (String key : b.keySet()) if (!a.containsKey(key)) lost.add(key);
        return CanonicalJson.object("newlyAvailableProductiveOpportunityCount", created.size(), "newlyAvailableOpportunityKeys", keys,
                "strengthenedOpportunityKeys", strengthened, "opportunityExpansionEvidence", created,
                "noPreviousSingleOpportunityExplanationCount", novel, "newConsequenceAtomOpportunityCount",atomicNovel,
                "lostOpportunityCount", lost.size(), "lostOpportunityKeys", lost,
                "beforeProductiveOpportunityCount", b.size(), "afterProductiveOpportunityCount", a.size(), "immediateBranchingChange", a.size() - b.size());
    }
    private static Map<String,Object> computeDelta(ReasoningState before, ReasoningState after) {
        int raw = 0, base = 0, display = 0, resolvedBase = 0, resolvedDisplay = 0;
        for (int r = 0; r < before.player.rowCount; r++) for (int s = 0; s < before.player.boardSize; s++) {
            raw += Integer.bitCount(before.player.rawDomain(r,s)) - Integer.bitCount(after.player.rawDomain(r,s));
            int b = Integer.bitCount(before.player.baseEffectiveDomain(r,s)), a = Integer.bitCount(after.player.baseEffectiveDomain(r,s));
            base += b - a; if (b > 1 && a == 1) resolvedBase++;
            b = Integer.bitCount(before.player.displayDomain(r,s)); a = Integer.bitCount(after.player.displayDomain(r,s));
            display += b - a; if (b > 1 && a == 1) resolvedDisplay++;
        }
        return CanonicalJson.object("rawDomainExcessReduction", raw, "baseDomainExcessReduction", base,
                "publicDisplayDomainExcessReduction", display, "resolvedBaseCellCount", resolvedBase,
                "resolvedPublicCellCount", resolvedDisplay, "establishedRelationDelta", after.facts.size() - before.facts.size());
    }
    private static final class EvidenceCache {
        final Map<String,ReasoningState> states; final Map<String,List<SkillOpportunity>> ops;
        final Map<String,Map<String,Object>> deltas = new HashMap<>(), expansions = new HashMap<>();
        final Map<String,Map<String,SkillOpportunity>> productiveByState = new HashMap<>();
        final IdentityHashMap<SkillOpportunity,Set<String>> effectsByOpportunity = new IdentityHashMap<>();
        EvidenceCache(Map<String,ReasoningState> states, Map<String,List<SkillOpportunity>> ops) { this.states=states; this.ops=ops; }
        String key(HumanStep step) { return step.beforeStateHash+">"+step.afterStateHash; }
        Map<String,Object> delta(HumanStep step) { return deltas.computeIfAbsent(key(step),k->computeDelta(states.get(step.beforeStateHash),states.get(step.afterStateHash))); }
        Map<String,Object> expansion(HumanStep step) { return expansions.computeIfAbsent(key(step),k->computeExpansion(step.beforeStateHash,step.afterStateHash,this)); }
        Map<String,SkillOpportunity> productive(String stateHash) { return productiveByState.computeIfAbsent(stateHash,k->Collections.unmodifiableMap(productive(ops.get(k)))); }
        Set<String> effects(SkillOpportunity op) { return effectsByOpportunity.computeIfAbsent(op,StructuralAhaAnalyzer::computeEffects); }
        Set<String> gained(SkillOpportunity after, SkillOpportunity before) { Set<String> out=new TreeSet<>(effects(after)); if(before!=null)out.removeAll(effects(before)); return out; }
    }
    private static final class PathSupportIndex {
        final Map<String,List<String>> historiesByState = new HashMap<>();
        final Map<String,Set<String>> opportunityKeysByPath = new HashMap<>();
        final Map<String,Map<String,Object>> bypassByPath = new HashMap<>();
        final EvidenceCache cache;
        PathSupportIndex(Map<String,HumanSolutionPath> histories, EvidenceCache cache) {
            this.cache=cache;
            for(HumanSolutionPath history:histories.values()) historiesByState.computeIfAbsent(history.terminalStateHash,k->new ArrayList<>()).add(history.pathId);
            for(List<String> ids:historiesByState.values()) Collections.sort(ids);
        }
        boolean uses(HumanSolutionPath path,String opportunityKey) {
            return opportunityKeysByPath.computeIfAbsent(path.pathId,k->new HashSet<>(path.opportunityKeys)).contains(opportunityKey);
        }
        Map<String,Object> bypass(HumanSolutionPath path) {
            return bypassByPath.computeIfAbsent(path.pathId,k->{
                List<Object> steps=new ArrayList<>();
                for(HumanStep step:path.steps) steps.add(CanonicalJson.object("humanStep",step.data(),"compression",cache.delta(step),"expansion",cache.expansion(step)));
                return CanonicalJson.object("pathId",path.pathId,"rawCost",path.cost.data(),"alternateStructuralSteps",steps);
            });
        }
    }
    private static Map<String,Object> pathSupport(PathEdge trigger, PathExplorerResult paths, PathSupportIndex index) {
        List<String> used = new ArrayList<>(), exactUsed = new ArrayList<>(), bypass = new ArrayList<>(); List<Object> bypassCosts = new ArrayList<>();
        for (HumanSolutionPath path : paths.solvedPaths) {
            if (path.steps.contains(trigger.step)) exactUsed.add(path.pathId);
            if (index.uses(path,trigger.opportunity.key)) used.add(path.pathId);
            else { bypass.add(path.pathId); bypassCosts.add(index.bypass(path)); }
        }
        List<String> sameState = new ArrayList<>(index.historiesByState.getOrDefault(trigger.step.beforeStateHash,Collections.emptyList()));
        Collections.sort(used); Collections.sort(exactUsed); Collections.sort(bypass);
        bypassCosts.sort(Comparator.comparing(CanonicalJson::write));
        String uniqueness = !bypass.isEmpty() ? "NOT_UNIQUE_PROVEN" : paths.completeness != PathExplorerResult.Completeness.COMPLETE
                ? "UNKNOWN" : used.isEmpty() ? "NO_SOLVED_PATH" : "ALL_SOLVED_PATHS_USE_KEY_PROVEN";
        return CanonicalJson.object("identityScope", "OPPORTUNITY_KEY_ACROSS_STATES", "solvedPathIdsUsingTrigger", used,
                "exactStateAndStepSolvedPathIds",exactUsed,
                "solvedPathIdsWithoutTrigger", bypass, "bypassRawCosts", bypassCosts, "sameSourceStateHistoryIds", sameState,
                "triggerUniqueness", uniqueness, "coverage", paths.completeness.name());
    }'''
if old not in s: raise SystemExit('core evidence block anchor mismatch')
s=s.replace(old,new,1)

rep('''    private static void activate(Map<String,Activation> active, List<SkillOpportunity> before, List<SkillOpportunity> after, int depth, String parent) {
        Map<String,SkillOpportunity> b = productive(before), a = productive(after);
        active.keySet().retainAll(a.keySet());
        for (SkillOpportunity op : a.values()) {
            Set<String> gain = gained(op,b.get(op.key)); if (!gain.isEmpty()) {
                Activation old = active.get(op.key);
                if (old != null) { gain.addAll(old.effects); active.put(op.key,new Activation(gain,Math.min(depth,old.depth),old.parent)); }
                else active.put(op.key,new Activation(gain,depth,parent));
            }
        }
    }''','''    private static void activate(Map<String,Activation> active, String beforeHash, String afterHash, int depth, String parent, EvidenceCache cache) {
        Map<String,SkillOpportunity> b = cache.productive(beforeHash), a = cache.productive(afterHash);
        active.keySet().retainAll(a.keySet());
        for (SkillOpportunity op : a.values()) {
            Set<String> gain = cache.gained(op,b.get(op.key)); if (!gain.isEmpty()) {
                Activation old = active.get(op.key);
                if (old != null) { gain.addAll(old.effects); active.put(op.key,new Activation(gain,Math.min(depth,old.depth),old.parent)); }
                else active.put(op.key,new Activation(gain,depth,parent));
            }
        }
    }''')
rep('''    private static List<Object> cascades(PathEdge trigger, PathExplorerResult paths, Map<String,ReasoningState> states,
                                          Map<String,List<SkillOpportunity>> ops, Map<String,List<CascadeLocation>> cascadeLocations) {''','''    private static List<Object> cascades(PathEdge trigger, PathExplorerResult paths, Map<String,ReasoningState> states,
                                          Map<String,List<SkillOpportunity>> ops, Map<String,List<CascadeLocation>> cascadeLocations, EvidenceCache cache) {''')
rep('''            activate(active,ops.get(trigger.step.beforeStateHash),ops.get(trigger.step.afterStateHash),1,trigger.edgeId);''','''            activate(active,trigger.step.beforeStateHash,trigger.step.afterStateHash,1,trigger.edgeId,cache);''')
rep('''                Set<String> intersection = effects(selected); if (activation != null) intersection.retainAll(activation.effects);''','''                Set<String> intersection = new TreeSet<>(cache.effects(selected)); if (activation != null) intersection.retainAll(activation.effects);''')
rep('''                    active.keySet().retainAll(productive(ops.get(step.afterStateHash)).keySet()); continue;''','''                    active.keySet().retainAll(cache.productive(step.afterStateHash).keySet()); continue;''')
rep('''                        "compression",delta(states.get(step.beforeStateHash),states.get(step.afterStateHash))));''','''                        "compression",cache.delta(step)));''')
rep('''                activate(active,ops.get(step.beforeStateHash),ops.get(step.afterStateHash),activation.depth+1,step.semanticHash());''','''                activate(active,step.beforeStateHash,step.afterStateHash,activation.depth+1,step.semanticHash(),cache);''')

p.write_text(s)
PY

git diff --check
git diff --stat
mapfile -t delta < <(git diff --name-only "$BASE_SHA" | sort)
test "${#delta[@]}" -eq 1
test "${delta[0]}" = 'puzzle-authoring/src/main/java/com/example/einsteingame/authoring/pss/aha/StructuralAhaAnalyzer.java'
cd ..
compile_repo(){ repo="$1" out="$2" src="/tmp/$(basename "$out")-sources.txt"; rm -rf "$out" "$src"; mkdir -p "$out"; find "$repo/puzzle-core/src/main/java" "$repo/puzzle-authoring/src/main/java" -type f -name '*.java' -print | sort > "$src"; find "$repo/puzzle-authoring/src/test/java/com/example/einsteingame/authoring/pss" -type f -name '*.java' -print | sort >> "$src"; java -Xmx2g -m jdk.compiler/com.sun.tools.javac.Main -encoding UTF-8 --release 8 -d "$out" "@$src"; }
compile_repo Baseline "$BASE_CLASSES"; compile_repo EinsteinGame "$CANDIDATE_CLASSES"
python3 - <<'PY'
from pathlib import Path
import struct
for root in ['/tmp/einstein-pre4-p2-base-classes','/tmp/einstein-pre4-p2-candidate-classes']:
 files=list(Path(root).rglob('*.class')); assert files
 assert all(struct.unpack('>IHH',p.read_bytes()[:8])==(0xCAFEBABE,0,52) for p in files)
 print('JAVA8_CLASSFILE_TARGET=PASS root='+root+' count='+str(len(files)))
PY
run_suite(){ repo="$1" cp="$2" tag="$3"; rm -rf "$repo/build/pss-logical-core"; (cd "$repo" && /usr/bin/time -f '%e' -o "/tmp/${tag}-aha.time" java -Xmx2g -cp "$cp" com.example.einsteingame.authoring.pss.PssAhaTest > "/tmp/${tag}-aha.log"); (cd "$repo" && /usr/bin/time -f '%e' -o "/tmp/${tag}-difficulty.time" java -Xmx2g -cp "$cp" com.example.einsteingame.authoring.pss.PssDifficultyTest > "/tmp/${tag}-difficulty.log"); (cd "$repo" && /usr/bin/time -f '%e' -o "/tmp/${tag}-experience.time" java -Xmx2g -cp "$cp" com.example.einsteingame.authoring.pss.PssExperienceTest > "/tmp/${tag}-experience.log"); }
run_suite Baseline "$BASE_CLASSES" base; run_suite EinsteinGame "$CANDIDATE_CLASSES" candidate
diff -u /tmp/base-aha.log /tmp/candidate-aha.log; diff -u /tmp/base-difficulty.log /tmp/candidate-difficulty.log; diff -u /tmp/base-experience.log /tmp/candidate-experience.log; diff -qr Baseline/build/pss-logical-core EinsteinGame/build/pss-logical-core
printf 'P2_BASE_AHA_SECONDS=%s\n' "$(cat /tmp/base-aha.time)"; printf 'P2_CANDIDATE_AHA_SECONDS=%s\n' "$(cat /tmp/candidate-aha.time)"; printf 'P2_BASE_DIFFICULTY_SECONDS=%s\n' "$(cat /tmp/base-difficulty.time)"; printf 'P2_CANDIDATE_DIFFICULTY_SECONDS=%s\n' "$(cat /tmp/candidate-difficulty.time)"; printf 'P2_BASE_EXPERIENCE_SECONDS=%s\n' "$(cat /tmp/base-experience.time)"; printf 'P2_CANDIDATE_EXPERIENCE_SECONDS=%s\n' "$(cat /tmp/candidate-experience.time)"
cd EinsteinGame
java -Xmx512m -cp "$CANDIDATE_CLASSES" com.example.einsteingame.authoring.pss.PssAhaTest | tee /tmp/pre4-p2-aha-lowheap.log
java -Xmx512m -cp "$CANDIDATE_CLASSES" com.example.einsteingame.authoring.pss.PssDifficultyTest | tee /tmp/pre4-p2-difficulty-lowheap.log
java -Xmx512m -cp "$CANDIDATE_CLASSES" com.example.einsteingame.authoring.pss.PssExperienceTest | tee /tmp/pre4-p2-experience-lowheap.log
java -Xmx2g -cp "$CANDIDATE_CLASSES" com.example.einsteingame.authoring.pss.PssPathExplorerTest | tee /tmp/pre4-p2-path.log
cd puzzle-authoring
java -Xmx2g -cp "$CANDIDATE_CLASSES" com.example.einsteingame.authoring.pss.acquisition.IntentAcquisitionTest | tee /tmp/pre4-p2-ia1.log
java -Xmx2g -cp "$CANDIDATE_CLASSES" com.example.einsteingame.authoring.pss.acquisition.IntentAcquisitionIA2Test | tee /tmp/pre4-p2-ia2.log
java -Xmx2g -cp "$CANDIDATE_CLASSES" com.example.einsteingame.authoring.pss.acquisition.IntentAcquisitionIA3Test | tee /tmp/pre4-p2-ia3.log
java -Xmx2g -cp "$CANDIDATE_CLASSES" com.example.einsteingame.authoring.pss.acquisition.IntentAcquisitionCheckpointTest | tee /tmp/pre4-p2-checkpoint.log
grep -F 'IntentAcquisitionTest PASS assertions=22' /tmp/pre4-p2-ia1.log; grep -F 'IntentAcquisitionIA2Test PASS assertions=33' /tmp/pre4-p2-ia2.log; grep -F 'IntentAcquisitionIA3Test PASS assertions=43' /tmp/pre4-p2-ia3.log; grep -F 'IntentAcquisitionCheckpointTest PASS assertions=12' /tmp/pre4-p2-checkpoint.log
cd ..
git config user.name 'Einstein Zero-Draw Optimization'; git config user.email 'noreply@localhost'; git add puzzle-authoring/src/main/java
mapfile -t changed < <(git diff --cached --name-only | sort); printf '%s\n' "${changed[@]}"; test "${#changed[@]}" -eq 1
git commit -m 'perf: memoize CP8 transition evidence within analysis'
CANDIDATE_SHA="$(git rev-parse HEAD)"; test "$(git rev-parse HEAD^)" = "$BASE_SHA"; git push origin "HEAD:refs/heads/$CANDIDATE_BRANCH"; test "$(git ls-remote origin "refs/heads/$CANDIDATE_BRANCH" | cut -f1)" = "$CANDIDATE_SHA"
printf 'P2_CANDIDATE_SHA=%s\n' "$CANDIDATE_SHA"; echo 'formalAcquisitionInvocation=0'; echo 'privateEvidenceWrite=0'; echo 'EINSTEIN_PRE4_P2_EVIDENCE_MEMOIZATION_ZERO_DRAW=PASS'
