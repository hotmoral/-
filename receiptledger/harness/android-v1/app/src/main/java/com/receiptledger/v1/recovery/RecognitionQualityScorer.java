package com.receiptledger.v1.recovery;

import com.receiptledger.v1.validation.ValidationStatus;

public final class RecognitionQualityScorer {
 public int score(QualitySignals s){int v=Math.min(Math.max(s.chars,0),300)+Math.min(Math.max(s.elements,0),80)*2+s.itemCount*180-s.partialCount*30+(s.hasTotal?200:0)+(s.hasDate?80:0);if(s.validation==ValidationStatus.PASS)v+=350;else if(s.validation==ValidationStatus.PASS_WITH_WARNINGS)v+=250;else if(s.validation==ValidationStatus.MISMATCH)v-=150;else v-=200;return v;}
 public boolean needsRecovery(QualitySignals s){if(s.chars<24||s.elements<5||s.itemCount<1||!s.hasTotal||!s.hasDate)return true;return !(s.validation==ValidationStatus.PASS||s.validation==ValidationStatus.PASS_WITH_WARNINGS);}
}
