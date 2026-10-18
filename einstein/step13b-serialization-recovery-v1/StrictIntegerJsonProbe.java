import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

/** Independent public contract probe for an integer-only JSON numeric subset. */
public final class StrictIntegerJsonProbe {
    static final class Parser {
        final String s;
        int i;
        Parser(String s) { this.s = s; }
        void ws() { while (i < s.length() && " \t\r\n".indexOf(s.charAt(i)) >= 0) i++; }
        char next() { if (i >= s.length()) fail("truncated"); return s.charAt(i++); }
        static void fail(String m) { throw new IllegalArgumentException(m); }
        void literal(String token) {
            if (!s.startsWith(token, i)) fail("expected " + token);
            i += token.length();
        }
        void value() {
            ws();
            if (i >= s.length()) fail("missing value");
            char c = s.charAt(i);
            if (c == '"') { string(); return; }
            if (c == '{') { object(); return; }
            if (c == '[') { array(); return; }
            if (c == 't') { literal("true"); return; }
            if (c == 'f') { literal("false"); return; }
            if (c == 'n') { literal("null"); return; }
            integer();
        }
        void object() {
            next(); ws();
            if (i < s.length() && s.charAt(i) == '}') { i++; return; }
            while (true) {
                ws(); if (i >= s.length() || s.charAt(i) != '"') fail("object key required");
                string(); ws(); if (next() != ':') fail("colon required"); value(); ws();
                char c = next(); if (c == '}') return; if (c != ',') fail("comma required");
            }
        }
        void array() {
            next(); ws();
            if (i < s.length() && s.charAt(i) == ']') { i++; return; }
            while (true) {
                value(); ws(); char c = next(); if (c == ']') return; if (c != ',') fail("comma required");
            }
        }
        void integer() {
            int start = i;
            if (s.charAt(i) == '-') i++;
            int digits = i;
            while (i < s.length() && Character.isDigit(s.charAt(i))) i++;
            if (i == digits) fail("integer required");
            if (i - digits > 1 && s.charAt(digits) == '0') fail("leading zero");
            if (i < s.length()) {
                char c = s.charAt(i);
                if (c == '.' || c == 'e' || c == 'E' || c == '+') fail("non-integer numeric form");
            }
            try { Long.parseLong(s.substring(start, i)); }
            catch (NumberFormatException e) { fail("signed 64-bit integer overflow"); }
        }
        void string() {
            if (next() != '"') fail("quote required");
            while (true) {
                char c = next();
                if (c == '"') return;
                if (c < 0x20) fail("control character");
                if (c != '\\') continue;
                c = next();
                if ("\"\\/bfnrt".indexOf(c) >= 0) continue;
                if (c != 'u') fail("bad escape");
                for (int k = 0; k < 4; k++) {
                    char h = next();
                    if (Character.digit(h, 16) < 0) fail("bad unicode escape");
                }
            }
        }
        void parse() {
            value(); ws(); if (i != s.length()) fail("trailing content");
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: StrictIntegerJsonProbe <file>");
        String text = new String(Files.readAllBytes(Paths.get(args[0])), StandardCharsets.UTF_8);
        new Parser(text).parse();
        System.out.println("STRICT_INTEGER_JSON_PROBE_PASS " + args[0]);
    }
}
