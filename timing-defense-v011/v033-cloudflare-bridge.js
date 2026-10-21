// Timing Defense Cloudflare transport bridge for v0.33 Stage 1.
// Observes the existing v0.31 WebSocket without replacing waiting-room ownership.
(function(){
  if(window.__TDCFBridge)return;
  const NativeWebSocket=window.WebSocket;
  const bridge={
    socket:null,session:null,slot:null,state:null,lastSeq:0,
    send(payload){
      const ws=this.socket;
      if(!ws||ws.readyState!==NativeWebSocket.OPEN)return false;
      try{ws.send(JSON.stringify(payload));return true}catch(_){return false}
    }
  };
  function emit(name,detail){window.dispatchEvent(new CustomEvent(`tdcf:${name}`,{detail}))}
  function WrappedWebSocket(url,protocols){
    const ws=protocols===undefined?new NativeWebSocket(url):new NativeWebSocket(url,protocols);
    if(String(url).includes('/ws/')){
      bridge.socket=ws;emit('socket',{socket:ws,url:String(url)});
      ws.addEventListener('message',event=>{
        let data;try{data=JSON.parse(event.data)}catch(_){return}
        if(data.type==='welcome'){
          bridge.session=data.session||bridge.session;
          bridge.slot=Number.isInteger(data.slot)?data.slot:bridge.slot;
          bridge.lastSeq=Number(data.lastSeq)||0;
          if(data.state)bridge.state=data.state;
          emit('welcome',{...data,socket:ws});
          if(data.state)emit('state',{state:data.state,source:'welcome',socket:ws});
        }else if(data.type==='state'&&data.state){
          bridge.state=data.state;emit('state',{state:data.state,source:'state',socket:ws});
        }else if(data.type==='action-result')emit('action-result',{...data,socket:ws});
        else if(data.type==='error')emit('error',{...data,socket:ws});
      });
      ws.addEventListener('close',event=>{
        if(bridge.socket===ws)emit('socket-close',{code:event.code,reason:event.reason,socket:ws});
      });
    }
    return ws;
  }
  Object.setPrototypeOf(WrappedWebSocket,NativeWebSocket);
  WrappedWebSocket.prototype=NativeWebSocket.prototype;
  window.WebSocket=WrappedWebSocket;
  window.__TDCFBridge=bridge;
})();