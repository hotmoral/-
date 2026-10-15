package com.receiptledger.v1.review;

import org.junit.Test;import static org.junit.Assert.*;

public class ReviewInputParserTest {
 @Test public void moneyAndQuantityAcceptHumanFormatting(){assertEquals(Long.valueOf(3200),ReviewInputParser.nullableMoney("3,200원"));assertEquals(Long.valueOf(-500),ReviewInputParser.nullableMoney(" -500 "));assertEquals(Integer.valueOf(2),ReviewInputParser.nullableQuantity("2"));assertNull(ReviewInputParser.nullableMoney(""));}
 @Test public void dateIsStrictAndCalendarValid(){assertEquals("2026-10-15",ReviewInputParser.nullableDate("2026-10-15"));try{ReviewInputParser.nullableDate("2026-02-30");fail();}catch(IllegalArgumentException expected){}try{ReviewInputParser.nullableDate("26/10/15");fail();}catch(IllegalArgumentException expected){}}
}
