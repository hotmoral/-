package com.receiptledger.v1.recovery;
import java.util.*;
public final class RecoveryResult {public final RecognitionCandidate best;public final List<PassDiagnostic> diagnostics;public RecoveryResult(RecognitionCandidate best,List<PassDiagnostic> diagnostics){this.best=best;this.diagnostics=Collections.unmodifiableList(new ArrayList<>(diagnostics));}public int attemptedPasses(){int n=0;for(PassDiagnostic d:diagnostics)if(d.pass!=RecognitionPass.MERGED)n++;return n;}public int derivedCandidates(){int n=0;for(PassDiagnostic d:diagnostics)if(d.pass==RecognitionPass.MERGED)n++;return n;}}
