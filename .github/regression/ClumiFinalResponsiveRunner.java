package com.example.einsteingame;

import android.app.Instrumentation;
import android.os.Bundle;

/** Isolated test-only runner for final production-screen responsive regression. */
public final class ClumiFinalResponsiveRunner extends Instrumentation {
    private Bundle args;

    @Override public void onCreate(Bundle arguments){
        super.onCreate(arguments);
        args=arguments==null?new Bundle():arguments;
        start();
    }

    @Override public void onStart(){
        new ClumiFinalResponsiveEvidence(this,args).run();
    }
}
