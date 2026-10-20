// Timing Defense v0.35 host adapter.
// On the legacy Render static site, keep using the separate Render API.
// On a full-stack host, transparently route API/SSE traffic to the current origin.
(function(){
  const LEGACY='https://timing-defense-mp.onrender.com';
  const onLegacyStatic=location.hostname==='timing-defense-v011.onrender.com';
  const TARGET=onLegacyStatic?LEGACY:location.origin;
  window.__TD_BACKEND_ORIGIN__=TARGET;
  if(TARGET===LEGACY)return;

  const nativeFetch=window.fetch.bind(window);
  window.fetch=function(input,init){
    if(typeof input==='string'&&input.startsWith(LEGACY)) input=TARGET+input.slice(LEGACY.length);
    else if(input&&typeof input.url==='string'&&input.url.startsWith(LEGACY)){
      input=new Request(TARGET+input.url.slice(LEGACY.length),input);
    }
    return nativeFetch(input,init)
  };

  const NativeEventSource=window.EventSource;
  function RoutedEventSource(url,config){
    const u=typeof url==='string'&&url.startsWith(LEGACY)?TARGET+url.slice(LEGACY.length):url;
    return new NativeEventSource(u,config)
  }
  RoutedEventSource.prototype=NativeEventSource.prototype;
  Object.setPrototypeOf(RoutedEventSource,NativeEventSource);
  window.EventSource=RoutedEventSource;
})();
