/* V6 server already applies cargo-weight speed. Bypass the V5 zone compensation wrapper. */
if(typeof v5RawSend==='function')send=function(m){return v5RawSend(m);};
