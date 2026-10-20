'use strict';
// Timing Defense portable full-stack host wrapper.
// Keeps the authoritative multiplayer server unchanged on an internal port,
// proxies API/SSE, and serves the game client from the same public origin.
const http=require('http');
const fs=require('fs');
const path=require('path');
const {spawn}=require('child_process');

const PUBLIC_PORT=Number(process.env.PORT||10000);
const INTERNAL_PORT=Number(process.env.TD_INTERNAL_PORT||PUBLIC_PORT+1);
const ROOT=path.resolve(__dirname,'../timing-defense-v011');
const SERVER=path.resolve(__dirname,'server.js');
const MIME={
  '.html':'text/html; charset=utf-8','.js':'application/javascript; charset=utf-8',
  '.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8',
  '.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.svg':'image/svg+xml',
  '.ico':'image/x-icon','.txt':'text/plain; charset=utf-8'
};

const child=spawn(process.execPath,[SERVER],{
  stdio:['ignore','inherit','inherit'],
  env:{...process.env,PORT:String(INTERNAL_PORT),ALLOW_ANY_ORIGIN:'1'}
});
child.on('exit',(code,signal)=>{
  console.error(`authoritative server exited code=${code} signal=${signal||''}`);
  process.exit(code||1);
});

function isApi(pathname){
  return pathname==='/health'||pathname.startsWith('/api/');
}

function proxy(req,res){
  const upstream=http.request({
    hostname:'127.0.0.1',port:INTERNAL_PORT,path:req.url,method:req.method,headers:{...req.headers,host:`127.0.0.1:${INTERNAL_PORT}`}
  },up=>{
    res.writeHead(up.statusCode||502,up.headers);
    up.pipe(res);
  });
  upstream.on('error',err=>{
    if(!res.headersSent){res.statusCode=502;res.setHeader('Content-Type','application/json; charset=utf-8')}
    if(!res.writableEnded)res.end(JSON.stringify({ok:false,error:'backend-unavailable',detail:err.code||err.message}));
  });
  req.pipe(upstream);
}

function staticFile(req,res,pathname){
  let rel;
  try{rel=pathname==='/'?'v035-portable.html':decodeURIComponent(pathname).replace(/^\/+/, '')}catch(_){return false}
  const file=path.resolve(ROOT,rel);
  if(file!==ROOT&&!file.startsWith(ROOT+path.sep))return false;
  let st;try{st=fs.statSync(file)}catch(_){return false}
  if(!st.isFile())return false;
  res.statusCode=200;
  res.setHeader('Content-Type',MIME[path.extname(file).toLowerCase()]||'application/octet-stream');
  res.setHeader('Cache-Control','no-store');
  if(req.method==='HEAD')res.end();else fs.createReadStream(file).pipe(res);
  return true;
}

const server=http.createServer((req,res)=>{
  let pathname='/';
  try{pathname=new URL(req.url,'http://localhost').pathname}catch(_){}
  if(isApi(pathname))return proxy(req,res);
  if((req.method==='GET'||req.method==='HEAD')&&staticFile(req,res,pathname))return;
  res.statusCode=404;res.setHeader('Content-Type','text/plain; charset=utf-8');res.end('not found');
});

server.listen(PUBLIC_PORT,'0.0.0.0',()=>{
  console.log(`timing-defense portable host listening on ${PUBLIC_PORT}; backend ${INTERNAL_PORT}`)
});

function shutdown(){try{child.kill('SIGTERM')}catch(_){};server.close(()=>process.exit(0));setTimeout(()=>process.exit(0),1500).unref()}
process.on('SIGTERM',shutdown);process.on('SIGINT',shutdown);
