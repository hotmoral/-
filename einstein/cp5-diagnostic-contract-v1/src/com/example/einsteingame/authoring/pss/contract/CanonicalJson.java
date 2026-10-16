package com.example.einsteingame.authoring.pss.contract;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.*;

/** Strict float-free JSON, sorted object keys, no reflection/enum/ordinal serialization. */
public final class CanonicalJson {
    private CanonicalJson() {}
    public static Map<String,Object> object(Object... pairs) {
        if(pairs.length%2!=0) throw new IllegalArgumentException("key/value pairs required");
        Map<String,Object> m=new TreeMap<>();
        for(int i=0;i<pairs.length;i+=2) {
            if(!(pairs[i] instanceof String)||m.containsKey(pairs[i])) throw new IllegalArgumentException("duplicate/invalid key");
            m.put((String)pairs[i],pairs[i+1]);
        }
        return m;
    }
    public static String write(Object value) {
        if(value==null)return "null";
        if(value instanceof String)return quote((String)value);
        if(value instanceof Boolean || value instanceof Integer || value instanceof Long)return value.toString();
        if(value instanceof Map) {
            TreeMap<String,Object> sorted=new TreeMap<>();
            for(Map.Entry<?,?> e:((Map<?,?>)value).entrySet()) {
                if(!(e.getKey() instanceof String))throw new IllegalArgumentException("JSON key must be string");
                sorted.put((String)e.getKey(),e.getValue());
            }
            List<String> parts=new ArrayList<>();
            for(Map.Entry<String,Object> e:sorted.entrySet())parts.add(quote(e.getKey())+":"+write(e.getValue()));
            return "{"+String.join(",",parts)+"}";
        }
        if(value instanceof Collection) {
            List<String> parts=new ArrayList<>();for(Object x:(Collection<?>)value)parts.add(write(x));
            return "["+String.join(",",parts)+"]";
        }
        throw new IllegalArgumentException("noncanonical JSON type: "+value.getClass().getName());
    }
    private static String quote(String s) {
        StringBuilder b=new StringBuilder("\"");
        for(char c:s.toCharArray())switch(c) {
            case '"':b.append("\\\"");break;case '\\':b.append("\\\\");break;
            case '\b':b.append("\\b");break;case '\f':b.append("\\f");break;
            case '\n':b.append("\\n");break;case '\r':b.append("\\r");break;case '\t':b.append("\\t");break;
            default:if(c<32)b.append(String.format(Locale.ROOT,"\\u%04x",(int)c));else b.append(c);
        }
        return b.append('"').toString();
    }
    public static Object read(String json) {
        Parser p=new Parser(Objects.requireNonNull(json));Object value=p.value();p.space();
        if(p.i!=json.length())throw new IllegalArgumentException("trailing JSON");return value;
    }
    public static String hash(Object value) {
        try {
            byte[] bytes=MessageDigest.getInstance("SHA-256").digest(write(value).getBytes(StandardCharsets.UTF_8));
            StringBuilder b=new StringBuilder();for(byte x:bytes)b.append(String.format(Locale.ROOT,"%02x",x&255));return b.toString();
        }catch(java.security.NoSuchAlgorithmException e){throw new IllegalStateException(e);}
    }
    private static final class Parser {
        final String s;int i;
        Parser(String s){this.s=s;}
        void space(){while(i<s.length()&&" \t\r\n".indexOf(s.charAt(i))>=0)i++;}
        char next(){if(i>=s.length())throw new IllegalArgumentException("truncated JSON");return s.charAt(i++);}
        void require(char c){space();if(next()!=c)throw new IllegalArgumentException("expected "+c);}
        Object value(){
            space();if(i>=s.length())throw new IllegalArgumentException("missing JSON value");char c=s.charAt(i);
            if(c=='"')return string();
            if(c=='{'){
                i++;Map<String,Object> m=new TreeMap<>();space();if(i<s.length()&&s.charAt(i)=='}'){i++;return m;}
                do{space();if(i>=s.length()||s.charAt(i)!='"')throw new IllegalArgumentException("missing key");String k=string();require(':');if(m.containsKey(k))throw new IllegalArgumentException("duplicate JSON key: "+k);m.put(k,value());space();c=next();if(c=='}')return m;if(c!=',')throw new IllegalArgumentException("expected comma");}while(true);
            }
            if(c=='['){i++;List<Object> a=new ArrayList<>();space();if(i<s.length()&&s.charAt(i)==']'){i++;return a;}
                do{a.add(value());space();c=next();if(c==']')return a;if(c!=',')throw new IllegalArgumentException("expected comma");}while(true);}
            for(String token:Arrays.asList("true","false","null"))if(s.startsWith(token,i)){i+=token.length();return token.equals("null")?null:Boolean.valueOf(token);}
            int start=i;if(c=='-')i++;int digits=i;while(i<s.length()&&s.charAt(i)>='0'&&s.charAt(i)<='9')i++;
            if(i==digits||(i-digits>1&&s.charAt(digits)=='0'))throw new IllegalArgumentException("invalid integer");
            try{long n=Long.parseLong(s.substring(start,i));return n>=Integer.MIN_VALUE&&n<=Integer.MAX_VALUE?Integer.valueOf((int)n):(Object)Long.valueOf(n);}
            catch(NumberFormatException e){throw new IllegalArgumentException("integer out of range");}
        }
        String string(){
            require('"');StringBuilder b=new StringBuilder();
            while(true){char c=next();if(c=='"')return b.toString();if(c<32)throw new IllegalArgumentException("unescaped control");
                if(c!='\\'){b.append(c);continue;}c=next();switch(c){
                    case '"':case '\\':case '/':b.append(c);break;case 'b':b.append('\b');break;case 'f':b.append('\f');break;
                    case 'n':b.append('\n');break;case 'r':b.append('\r');break;case 't':b.append('\t');break;
                    case 'u':if(i+4>s.length())throw new IllegalArgumentException("truncated escape");try{b.append((char)Integer.parseInt(s.substring(i,i+4),16));}catch(NumberFormatException e){throw new IllegalArgumentException("bad escape");}i+=4;break;
                    default:throw new IllegalArgumentException("invalid escape");
                }
            }
        }
    }
}
