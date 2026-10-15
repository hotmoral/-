package com.receiptledger.v1.image;

import org.junit.Test;
import java.io.ByteArrayInputStream;
import static org.junit.Assert.*;

public class ExifOrientationParserTest {
    @Test public void readsLittleEndianOrientationSix() throws Exception {
        byte[] payload=new byte[]{'E','x','i','f',0,0,'I','I',42,0,8,0,0,0,1,0,0x12,0x01,3,0,1,0,0,0,6,0,0,0,0,0,0,0};
        int len=payload.length+2; byte[] jpeg=new byte[payload.length+8];int p=0;jpeg[p++]=(byte)0xff;jpeg[p++]=(byte)0xd8;jpeg[p++]=(byte)0xff;jpeg[p++]=(byte)0xe1;jpeg[p++]=(byte)(len>>8);jpeg[p++]=(byte)len;System.arraycopy(payload,0,jpeg,p,payload.length);p+=payload.length;jpeg[p++]=(byte)0xff;jpeg[p]=(byte)0xd9;
        assertEquals(6,ExifOrientationParser.readOrientation(new ByteArrayInputStream(jpeg)));
    }
    @Test public void nonJpegDefaultsToOne() throws Exception {assertEquals(1,ExifOrientationParser.readOrientation(new ByteArrayInputStream(new byte[]{1,2,3,4})));}
}
