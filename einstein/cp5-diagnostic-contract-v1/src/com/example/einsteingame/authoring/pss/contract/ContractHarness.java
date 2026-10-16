package com.example.einsteingame.authoring.pss.contract;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

public final class ContractHarness {
    private static Map<String,Object> map(Object value) {
        if(!(value instanceof Map)) throw new IllegalArgumentException("expected object");
        @SuppressWarnings("unchecked") Map<String,Object> m=(Map<String,Object>)value;
        return m;
    }
    private static int integer(Map<String,Object> m,String key) {
        Object value=m.get(key);
        if(!(value instanceof Integer)) throw new IllegalArgumentException("expected int: "+key);
        return (Integer)value;
    }
    private static void check(boolean value,String message) {
        if(!value) throw new IllegalArgumentException(message);
    }
    private static void assertNoFloat(Object value) {
        if(value==null || value instanceof String || value instanceof Boolean || value instanceof Integer || value instanceof Long) return;
        if(value instanceof Float || value instanceof Double) throw new IllegalArgumentException("floating canonical value");
        if(value instanceof Map) {
            for(Map.Entry<?,?> e:((Map<?,?>)value).entrySet()) {
                check(e.getKey() instanceof String,"non-string key");
                assertNoFloat(e.getValue());
            }
            return;
        }
        if(value instanceof Collection) {
            for(Object x:(Collection<?>)value) assertNoFloat(x);
            return;
        }
        throw new IllegalArgumentException("unsupported canonical type: "+value.getClass().getName());
    }
    private static Object read(Path path) throws Exception {
        return CanonicalJson.read(Files.readString(path));
    }
    private static void validateEnvelope(Path path) throws Exception {
        Object parsed=read(path);
        assertNoFloat(parsed);
        Map<String,Object> root=map(parsed);
        Map<String,Object> counts=map(root.get("baselineCounts"));
        check(!counts.containsKey("maxDepthReached"),"depth must not be read from top-level baselineCounts");
        Map<String,Object> budget=map(counts.get("budgetConsumed"));
        int expanded=integer(budget,"expandedNodes");
        int generated=integer(budget,"generatedEdges");
        int depth=integer(budget,"maxDepthReached");
        check(integer(counts,"expandedNodeCount")==expanded,"expanded count mismatch");
        check(integer(counts,"generatedEdgeCount")==generated,"generated count mismatch");
        check(depth>=0,"negative depth");
        String canonical=CanonicalJson.write(parsed);
        System.out.println("CANONICAL="+canonical);
        System.out.println("HASH="+CanonicalJson.hash(parsed));
    }
    private static void writeCheckpoint() {
        Map<String,Object> cp5=CanonicalJson.object(
                "outcome","NO_SOLVED_PATH",
                "completeness","BUDGET_EXHAUSTED",
                "conclusion","UNKNOWN",
                "error",null,
                "expandedNodeCount",17,
                "generatedEdgeCount",41,
                "distinctStateCount",23,
                "budgetConsumed",CanonicalJson.object("expandedNodes",17,"generatedEdges",41,"maxDepthReached",4),
                "frontierCount",9,
                "cutoffKindDistribution",CanonicalJson.object("EDGE_LIMIT",1,"UNVISITED_AFTER_EDGE_LIMIT",8),
                "solvedPathCount",0,
                "solvedHumanStepMinimum",null,
                "solvedHumanStepMaximum",null,
                "invalidTerminalCount",0,
                "stalledPathCount",0);
        Map<String,Object> checkpoint=CanonicalJson.object(
                "phase","CP5_RETURNED",
                "request",CanonicalJson.object("kind","SYNTHETIC","ordinal",1),
                "explorerConfig",CanonicalJson.object("maxExpandedNodes",1000,"maxGeneratedEdges",6000,"maxDepth",100),
                "CP5",cp5,
                "bindingCutoff","EDGE_LIMIT");
        assertNoFloat(checkpoint);
        String json=CanonicalJson.write(checkpoint);
        Object reparsed=CanonicalJson.read(json);
        check(json.equals(CanonicalJson.write(reparsed)),"checkpoint roundtrip mismatch");
        System.out.println("CHECKPOINT="+json);
        System.out.println("CHECKPOINT_HASH="+CanonicalJson.hash(checkpoint));
    }
    private static void rejectDouble() {
        try {
            CanonicalJson.write(CanonicalJson.object("ratio",Double.valueOf(1.25d)));
            throw new IllegalStateException("Double unexpectedly accepted");
        } catch(IllegalArgumentException expected) {
            System.out.println("REJECT_DOUBLE=PASS");
        }
    }
    private static void rejectFloat() {
        try {
            CanonicalJson.write(CanonicalJson.object("ratio",Float.valueOf(1.25f)));
            throw new IllegalStateException("Float unexpectedly accepted");
        } catch(IllegalArgumentException expected) {
            System.out.println("REJECT_FLOAT=PASS");
        }
    }
    private static void rejectDecimal(Path path) throws Exception {
        try {
            read(path);
            throw new IllegalStateException("decimal JSON unexpectedly accepted");
        } catch(IllegalArgumentException expected) {
            System.out.println("REJECT_DECIMAL=PASS");
        }
    }
    public static void main(String[] args) throws Exception {
        if(args.length<1) throw new IllegalArgumentException("mode required");
        switch(args[0]) {
            case "validate-envelope":
                check(args.length==2,"path required"); validateEnvelope(Path.of(args[1])); break;
            case "write-checkpoint": writeCheckpoint(); break;
            case "reject-double": rejectDouble(); break;
            case "reject-float": rejectFloat(); break;
            case "reject-decimal":
                check(args.length==2,"path required"); rejectDecimal(Path.of(args[1])); break;
            default: throw new IllegalArgumentException("unknown mode: "+args[0]);
        }
    }
}
