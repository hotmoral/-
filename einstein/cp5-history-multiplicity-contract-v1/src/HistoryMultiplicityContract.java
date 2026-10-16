import java.util.*;

public final class HistoryMultiplicityContract {
    static final class Edge {
        final String sourceHistory, targetHistory, beforeState, afterState, skill;
        final int depth, cost;
        Edge(String sourceHistory, String targetHistory, String beforeState, String afterState,
             int depth, int cost, String skill) {
            this.sourceHistory = sourceHistory;
            this.targetHistory = targetHistory;
            this.beforeState = beforeState;
            this.afterState = afterState;
            this.depth = depth;
            this.cost = cost;
            this.skill = skill;
        }
    }

    static final class Frontier {
        final String historyId, stateId;
        final int depth;
        Frontier(String historyId, String stateId, int depth) {
            this.historyId = historyId;
            this.stateId = stateId;
            this.depth = depth;
        }
    }

    private static final class StateStats {
        int inboundCount = 0;
        int minDepth = Integer.MAX_VALUE, maxDepth = Integer.MIN_VALUE;
        int minCost = Integer.MAX_VALUE, maxCost = Integer.MIN_VALUE;
        final Set<Integer> depths = new TreeSet<>();
        final Set<String> histories = new TreeSet<>();
        void add(Edge e) {
            inboundCount++;
            minDepth = Math.min(minDepth, e.depth);
            maxDepth = Math.max(maxDepth, e.depth);
            minCost = Math.min(minCost, e.cost);
            maxCost = Math.max(maxCost, e.cost);
            depths.add(e.depth);
            histories.add(e.targetHistory);
        }
    }

    static Map<String,Object> aggregate(String rootState, String rootHistory,
                                        List<Edge> edges, List<Frontier> frontier) {
        text(rootState, "rootState");
        text(rootHistory, "rootHistory");
        Objects.requireNonNull(edges, "edges");
        Objects.requireNonNull(frontier, "frontier");

        Set<String> targetHistories = new HashSet<>();
        Map<String,StateStats> stats = new TreeMap<>();
        Map<Integer,Integer> depthOccurrences = new TreeMap<>();
        Map<Integer,Set<String>> depthStates = new TreeMap<>();
        Map<String,Integer> arrivalsBySkill = new TreeMap<>();

        for (Edge e : edges) {
            text(e.sourceHistory, "sourceHistory");
            text(e.targetHistory, "targetHistory");
            text(e.beforeState, "beforeState");
            text(e.afterState, "afterState");
            text(e.skill, "skill");
            if (e.depth < 1) throw new IllegalArgumentException("depth must be >= 1");
            if (e.cost < 0) throw new IllegalArgumentException("cost must be >= 0");
            if (rootState.equals(e.afterState)) throw new IllegalArgumentException("root-state arrival is forbidden");
            if (!targetHistories.add(e.targetHistory)) throw new IllegalArgumentException("duplicate target history: " + e.targetHistory);
            stats.computeIfAbsent(e.afterState, k -> new StateStats()).add(e);
            depthOccurrences.put(e.depth, depthOccurrences.getOrDefault(e.depth, 0) + 1);
            depthStates.computeIfAbsent(e.depth, k -> new TreeSet<>()).add(e.afterState);
        }

        Set<String> knownStates = new HashSet<>();
        knownStates.add(rootState);
        knownStates.addAll(stats.keySet());
        Set<String> knownHistories = new HashSet<>();
        knownHistories.add(rootHistory);
        knownHistories.addAll(targetHistories);
        for (Edge e : edges) {
            if (!knownStates.contains(e.beforeState)) throw new IllegalArgumentException("unknown before state: " + e.beforeState);
            if (!knownHistories.contains(e.sourceHistory)) throw new IllegalArgumentException("unknown source history: " + e.sourceHistory);
        }

        Map<String,Integer> histogram = new TreeMap<>();
        int maxMultiplicity = 0;
        for (StateStats s : stats.values()) {
            String key = Integer.toString(s.inboundCount);
            histogram.put(key, histogram.getOrDefault(key, 0) + 1);
            maxMultiplicity = Math.max(maxMultiplicity, s.inboundCount);
        }

        List<Map<String,Object>> top = new ArrayList<>();
        List<String> stateIds = new ArrayList<>(stats.keySet());
        stateIds.sort((a,b) -> {
            int c = Integer.compare(stats.get(b).inboundCount, stats.get(a).inboundCount);
            return c != 0 ? c : a.compareTo(b);
        });
        for (String stateId : stateIds) {
            StateStats s = stats.get(stateId);
            if (s.inboundCount <= 1) continue;
            top.add(obj(
                    "stateId", stateId,
                    "inboundHistoryCount", s.inboundCount,
                    "distinctHistoryCount", s.histories.size(),
                    "minDepth", s.minDepth,
                    "maxDepth", s.maxDepth,
                    "minCost", s.minCost,
                    "maxCost", s.maxCost));
            for (Edge e : edges) if (stateId.equals(e.afterState))
                arrivalsBySkill.put(e.skill, arrivalsBySkill.getOrDefault(e.skill, 0) + 1);
        }

        List<Map<String,Object>> depthRows = new ArrayList<>();
        for (Integer depth : depthOccurrences.keySet()) {
            int globallyNew = 0;
            for (Map.Entry<String,StateStats> entry : stats.entrySet())
                if (entry.getValue().minDepth == depth) globallyNew++;
            int occurrences = depthOccurrences.get(depth);
            depthRows.add(obj(
                    "depth", depth,
                    "arrivalOccurrences", occurrences,
                    "distinctArrivalStates", depthStates.get(depth).size(),
                    "globallyNewStates", globallyNew,
                    "repeatPressureOccurrences", occurrences - globallyNew));
        }

        List<Map<String,Object>> crossDepth = new ArrayList<>();
        for (Map.Entry<String,StateStats> entry : stats.entrySet()) {
            if (entry.getValue().depths.size() > 1)
                crossDepth.add(obj("stateId", entry.getKey(), "depths", new ArrayList<>(entry.getValue().depths)));
        }

        Map<String,Integer> frontierCounts = new TreeMap<>();
        Set<String> frontierHistories = new HashSet<>();
        for (Frontier f : frontier) {
            text(f.historyId, "frontier historyId");
            text(f.stateId, "frontier stateId");
            if (f.depth < 0) throw new IllegalArgumentException("frontier depth must be >= 0");
            if (!frontierHistories.add(f.historyId)) throw new IllegalArgumentException("duplicate frontier history: " + f.historyId);
            if (!knownHistories.contains(f.historyId)) throw new IllegalArgumentException("unknown frontier history: " + f.historyId);
            if (!knownStates.contains(f.stateId)) throw new IllegalArgumentException("unknown frontier state: " + f.stateId);
            frontierCounts.put(f.stateId, frontierCounts.getOrDefault(f.stateId, 0) + 1);
        }
        int frontierMax = 0;
        Map<String,Integer> frontierHistogram = new TreeMap<>();
        List<Map<String,Object>> frontierTop = new ArrayList<>();
        List<String> frontierStates = new ArrayList<>(frontierCounts.keySet());
        frontierStates.sort((a,b) -> {
            int c = Integer.compare(frontierCounts.get(b), frontierCounts.get(a));
            return c != 0 ? c : a.compareTo(b);
        });
        for (String stateId : frontierStates) {
            int count = frontierCounts.get(stateId);
            frontierMax = Math.max(frontierMax, count);
            String key = Integer.toString(count);
            frontierHistogram.put(key, frontierHistogram.getOrDefault(key, 0) + 1);
            frontierTop.add(obj("stateId", stateId, "historyCount", count));
        }

        int uniqueArrivals = stats.size();
        return obj(
                "recordType", "SyntheticHistoryMultiplicityContract",
                "contractVersion", "1.0.0",
                "generatedEdgeCount", edges.size(),
                "uniqueArrivalStateCount", uniqueArrivals,
                "distinctStateCount", 1 + uniqueArrivals,
                "repeatedArrivalCount", edges.size() - uniqueArrivals,
                "repeatedArrivalBasis", "EDGE_OCCURRENCES_MINUS_UNIQUE_ARRIVAL_STATES",
                "maxInboundHistoryMultiplicity", maxMultiplicity,
                "stateMultiplicityHistogram", histogram,
                "topReconvergedStates", top,
                "crossDepthStates", crossDepth,
                "depthBreakdown", depthRows,
                "reconvergedTargetArrivalBySyntheticSkill", arrivalsBySkill,
                "frontier", obj(
                        "historyOccurrenceCount", frontier.size(),
                        "uniqueStateCount", frontierCounts.size(),
                        "maxHistoryMultiplicity", frontierMax,
                        "stateMultiplicityHistogram", frontierHistogram,
                        "states", frontierTop));
    }

    private static void text(String value, String label) {
        if (value == null || value.trim().isEmpty()) throw new IllegalArgumentException(label + " is blank");
    }

    private static Map<String,Object> obj(Object... pairs) {
        if ((pairs.length & 1) != 0) throw new IllegalArgumentException("odd object pair count");
        Map<String,Object> out = new TreeMap<>();
        for (int i = 0; i < pairs.length; i += 2) out.put((String)pairs[i], pairs[i+1]);
        return out;
    }

    static String json(Object value) {
        if (value == null) return "null";
        if (value instanceof String) return "\"" + escape((String)value) + "\"";
        if (value instanceof Integer || value instanceof Long || value instanceof Boolean) return value.toString();
        if (value instanceof Map) {
            StringBuilder b = new StringBuilder("{");
            boolean first = true;
            for (Object raw : ((Map<?,?>)value).entrySet()) {
                Map.Entry<?,?> e = (Map.Entry<?,?>)raw;
                if (!first) b.append(','); first = false;
                b.append(json((String)e.getKey())).append(':').append(json(e.getValue()));
            }
            return b.append('}').toString();
        }
        if (value instanceof Collection) {
            StringBuilder b = new StringBuilder("[");
            boolean first = true;
            for (Object v : (Collection<?>)value) {
                if (!first) b.append(','); first = false;
                b.append(json(v));
            }
            return b.append(']').toString();
        }
        throw new IllegalArgumentException("unsupported JSON type: " + value.getClass().getName());
    }

    private static String escape(String s) {
        StringBuilder b = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '\\': b.append("\\\\"); break;
                case '"': b.append("\\\""); break;
                case '\n': b.append("\\n"); break;
                case '\r': b.append("\\r"); break;
                case '\t': b.append("\\t"); break;
                default:
                    if (c < 0x20) b.append(String.format("\\u%04x", (int)c));
                    else b.append(c);
            }
        }
        return b.toString();
    }

    static List<Edge> fixtureEdges() {
        return Arrays.asList(
                new Edge("H0","H1","S0","S1",1,1,"SYNTH_A"),
                new Edge("H0","H2","S0","S2",1,2,"SYNTH_B"),
                new Edge("H0","H3","S0","S1",1,3,"SYNTH_C"),
                new Edge("H1","H4","S1","S3",2,3,"SYNTH_A"),
                new Edge("H2","H5","S2","S3",2,4,"SYNTH_B"),
                new Edge("H3","H6","S1","S4",2,5,"SYNTH_C"),
                new Edge("H4","H7","S3","S5",3,6,"SYNTH_A"),
                new Edge("H5","H8","S3","S5",3,7,"SYNTH_B"),
                new Edge("H6","H9","S4","S3",3,8,"SYNTH_C"));
    }

    static List<Frontier> fixtureFrontier() {
        return Arrays.asList(
                new Frontier("H7","S5",3),
                new Frontier("H8","S5",3),
                new Frontier("H9","S3",3),
                new Frontier("H6","S4",2));
    }

    public static void main(String[] args) {
        String mode = args.length == 0 ? "fixture" : args[0];
        List<Edge> edges = new ArrayList<>(fixtureEdges());
        List<Frontier> frontier = new ArrayList<>(fixtureFrontier());
        if ("shuffled".equals(mode)) {
            Collections.reverse(edges);
            Collections.rotate(frontier, 1);
        } else if ("invalid-duplicate-history".equals(mode)) {
            edges.add(new Edge("H9","H1","S3","S6",4,9,"SYNTH_D"));
        } else if (!"fixture".equals(mode)) {
            throw new IllegalArgumentException("unknown mode: " + mode);
        }
        System.out.println(json(aggregate("S0", "H0", edges, frontier)));
    }
}
