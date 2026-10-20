'use strict';
const http=require('http'),fs=require('fs'),path=require('path'),{spawn}=require('child_process');
const PUBLIC_PORT=Number(process.env.PORT||10000);
const INTERNAL_PORT=Number(process.env.TD_INTERNAL_PORT||19101);
const ROOT=path.resolve(__dirname,'../timing-defense-v011');
const MIME={'.html':'text/html; charset=utf-8','.js':'application/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.svg':'image/svg+xml','.ico':'image/x-icon','.txt':'text/plain; charset=utf-8'};

const child=spawn(process.execPath,[path.join(__dirname,'server.js')],{
  env:{...process.env,PORT:String(INTERNAL_PORT)},stdio:['ignore','inherit','inherit']
});
child.on('exit',(code,signal)=>{console.error('timing-defense child exited',code,signal);process.exit(code||1)});

function safeFile(urlPath){
  const rel=urlPath==='/'?'v035-portable.html':decodeURIComponent(urlPath).replace(/^\/+/, '');
  const file=path.resolve(ROOT,rel);
  if(file!==ROOT&&!file.startsWith(ROOT+path.sep))return null;
  try{const st=fs.statSync(file);return st.isFile()?file:null}catch(_){return null}
}
function serve(req,res,urlPath){
  if(req.method!=='GET'&&req.method!=='HEAD')return false;
  const file=safeFile(urlPath);if(!file)return false;
  res.statusCode=200;res.setHeader('Content-Type',MIME[path.extname(file).toLowerCase()]||'application/octet-stream');res.setHeader('Cache-Control','no-store');
  if(req.method==='HEAD'){res.end();return true}
  fs.createReadStream(file).pipe(res);return true
}
function proxy(req,res){
  const headers={...req.headers,host:`127.0.0.1:${INTERNAL_PORT}`};
  const p=http.request({host:'127.0.0.1',port:INTERNAL_PORT,method:req.method,path:req.url,headers},r=>{
    res.writeHead(r.statusCode||502,r.headers);r.pipe(res)
  });
  p.on('error',e=>{
    if(!res.headersSent)res.writeHead(502,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});
    res.end(JSON.stringify({ok:false,error:'backend-unavailable',detail:e.code||e.message}))
  });
  req.pipe(p)
}

const server=http.createServer((req,res)=>{
  let pathname='/';try{pathname=new URL(req.url,'http://local').pathname}catch(_){}
  if(pathname==='/health'||pathname.startsWith('/api/'))return proxy(req,res);
  if(serve(req,res,pathname))return;
  proxy(req,res)
});
server.listen(PUBLIC_PORT,'0.0.0.0',()=>console.log(`timing-defense portable host listening on ${PUBLIC_PORT} -> ${INTERNAL_PORT}`));
function shutdown(){try{child.kill('SIGTERM')}catch(_){};server.close(()=>process.exit(0));setTimeout(()=>process.exit(0),1500).unref()}
process.on('SIGTERM',shutdown);process.on('SIGINT',shutdown);
