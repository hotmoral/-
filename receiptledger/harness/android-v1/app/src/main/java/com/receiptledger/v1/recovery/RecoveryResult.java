package com.receiptledger.v1.recovery;
import java.util.*;
public final class RecoveryResult {public final RecognitionCandidate best;public final List<PassDiagnostic> diagnostics;public RecoveryResult(RecognitionCandidate best,List<PassDiagnostic> diagnostics){this.best=best;this.diagnostics=Collections.unmodifiableList(new ArrayList<>(diagnostics));}public int attemptedPasses(){return diagnostics.size();}}
