package com.example.einsteingame;

import android.app.Instrumentation;
import android.os.Bundle;
import java.io.PrintWriter;
import java.io.StringWriter;

/** Isolated test-only runner for final production-screen responsive regression. */
public final class ClumiFinalResponsiveRunner extends Instrumentation {
    private Bundle args;

    @Override public void onCreate(Bundle arguments){
        super.onCreate(arguments);
        args=arguments==null?new Bundle():arguments;
        Thread.UncaughtExceptionHandler previous=Thread.getDefaultUncaughtExceptionHandler();
        Thread.setDefaultUncaughtExceptionHandler((thread,failure)->{
            try{
                StringWriter detail=new StringWriter();
                failure.printStackTrace(new PrintWriter(detail));
                Bundle status=new Bundle();
                status.putString("stream","Clumi V3 UNCAUGHT ["+thread.getName()+"]:\n"+detail+"\n");
                sendStatus(-1,status);
            }catch(Throwable ignored){}
            if(previous!=null)previous.uncaughtException(thread,failure);
        });
        start();
    }

    @Override public void onStart(){
        new ClumiFinalResponsiveEvidence(this,args).run();
    }
}
