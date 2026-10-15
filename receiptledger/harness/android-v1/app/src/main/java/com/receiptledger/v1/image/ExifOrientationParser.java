package com.receiptledger.v1.image;

import java.io.IOException;
import java.io.InputStream;

public final class ExifOrientationParser {
    private ExifOrientationParser() {}

    public static int readOrientation(InputStream in) throws IOException {
        if (in == null || in.read() != 0xff || in.read() != 0xd8) return 1;
        while (true) {
            int prefix;
            do { prefix = in.read(); } while (prefix != -1 && prefix != 0xff);
            if (prefix == -1) return 1;
            int marker;
            do { marker = in.read(); } while (marker == 0xff);
            if (marker == -1 || marker == 0xd9 || marker == 0xda) return 1;
            if (marker == 0x01 || (marker >= 0xd0 && marker <= 0xd7)) continue;
            int length = readU16(in);
            if (length < 2) return 1;
            int payloadLength = length - 2;
            if (marker == 0xe1 && payloadLength <= 65535) {
                byte[] payload = new byte[payloadLength];
                readFully(in, payload);
                int value = parseExif(payload);
                if (value >= 1 && value <= 8) return value;
            } else {
                skipFully(in, payloadLength);
            }
        }
    }

    private static int parseExif(byte[] b) {
        if (b.length < 14 || b[0]!='E' || b[1]!='x' || b[2]!='i' || b[3]!='f' || b[4]!=0 || b[5]!=0) return 1;
        int t=6; boolean little;
        if (b[t]=='I' && b[t+1]=='I') little=true;
        else if (b[t]=='M' && b[t+1]=='M') little=false;
        else return 1;
        if (u16(b,t+2,little)!=42) return 1;
        long ifdOffset=u32(b,t+4,little); int ifd=t+(int)ifdOffset;
        if (ifd<0 || ifd+2>b.length) return 1;
        int count=u16(b,ifd,little);
        for(int n=0;n<count;n++){
            int e=ifd+2+n*12;
            if(e+12>b.length) return 1;
            if(u16(b,e,little)==0x0112 && u16(b,e+2,little)==3 && u32(b,e+4,little)>=1){
                int orientation=u16(b,e+8,little);
                return orientation>=1&&orientation<=8?orientation:1;
            }
        }
        return 1;
    }

    private static int u16(byte[] b,int o,boolean little){
        int a=b[o]&255,c=b[o+1]&255; return little ? a|(c<<8) : (a<<8)|c;
    }
    private static long u32(byte[] b,int o,boolean little){
        long a=b[o]&255L,c=b[o+1]&255L,d=b[o+2]&255L,e=b[o+3]&255L;
        return little ? a|(c<<8)|(d<<16)|(e<<24) : (a<<24)|(c<<16)|(d<<8)|e;
    }
    private static int readU16(InputStream in)throws IOException{int a=in.read(),b=in.read();if(a<0||b<0)throw new IOException("Unexpected EOF");return(a<<8)|b;}
    private static void readFully(InputStream in,byte[] out)throws IOException{int p=0;while(p<out.length){int n=in.read(out,p,out.length-p);if(n<0)throw new IOException("Unexpected EOF");p+=n;}}
    private static void skipFully(InputStream in,int count)throws IOException{int left=count;while(left>0){long n=in.skip(left);if(n<=0){if(in.read()<0)throw new IOException("Unexpected EOF");n=1;}left-=n;}}
}
