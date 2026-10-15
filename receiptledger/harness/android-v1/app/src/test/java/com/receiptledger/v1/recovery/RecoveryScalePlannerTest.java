package com.receiptledger.v1.recovery;
import org.junit.Test;import static org.junit.Assert.*;
public class RecoveryScalePlannerTest {@Test public void largeInputIsBoundedWithoutAspectBreak(){RecoveryScalePlanner.Plan p=RecoveryScalePlanner.plan(5000,3000,3200,6_000_000);assertTrue(p.width<=3200);assertTrue((long)p.width*p.height<=6_000_000L+5000);assertEquals(5.0/3.0,p.width/(double)p.height,0.01);}@Test public void smallInputIsNotUpscaled(){RecoveryScalePlanner.Plan p=RecoveryScalePlanner.plan(1200,800,3200,6_000_000);assertEquals(1200,p.width);assertEquals(800,p.height);}}
