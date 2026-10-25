(() => {
  'use strict';
  const TD = window.TwinDock;

  function flag(name, fallback=true){
    const value=new URLSearchParams(location.search).get(name);
    if(value===null)return fallback;
    return !['0','false','off','no'].includes(value.toLowerCase());
  }

  TD.Effects = function Effects(state){
    const settings=Object.freeze({audio:flag('audio',true),haptics:flag('haptics',true)});
    let ctx=null,master=null,rcsGain=null,lastRcsTarget=0;

    function ensureAudio(){
      if(!settings.audio||ctx)return;
      const AC=window.AudioContext||window.webkitAudioContext;
      if(!AC)return;
      ctx=new AC();
      master=ctx.createGain();master.gain.value=.72;master.connect(ctx.destination);

      const buffer=ctx.createBuffer(1,Math.floor(ctx.sampleRate*.35),ctx.sampleRate);
      const data=buffer.getChannelData(0);
      for(let i=0;i<data.length;i++)data[i]=(Math.random()*2-1)*(.55+.45*Math.sin(i*.017));
      const source=ctx.createBufferSource(),filter=ctx.createBiquadFilter();
      source.buffer=buffer;source.loop=true;filter.type='bandpass';filter.frequency.value=620;filter.Q.value=.7;
      rcsGain=ctx.createGain();rcsGain.gain.value=0;
      source.connect(filter);filter.connect(rcsGain);rcsGain.connect(master);source.start();
    }

    function unlock(){
      if(!settings.audio)return Promise.resolve(false);
      ensureAudio();
      if(!ctx||ctx.state==='closed')return Promise.resolve(false);
      if(ctx.state==='running')return Promise.resolve(true);
      return Promise.resolve(ctx.resume()).then(()=>ctx.state==='running').catch(()=>false);
    }

    function tone(freq,duration,gain=.06,type='sine',delay=0){
      if(!settings.audio)return;
      ensureAudio();if(!ctx)return;
      const t=ctx.currentTime+delay,o=ctx.createOscillator(),g=ctx.createGain();
      o.type=type;o.frequency.setValueAtTime(freq,t);
      g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(gain,t+.012);g.gain.exponentialRampToValueAtTime(.0001,t+duration);
      o.connect(g);g.connect(master);o.start(t);o.stop(t+duration+.02);
    }

    function burst(duration=.08,gain=.04,cutoff=900){
      if(!settings.audio)return;
      ensureAudio();if(!ctx)return;
      const count=Math.max(1,Math.floor(ctx.sampleRate*duration)),buffer=ctx.createBuffer(1,count,ctx.sampleRate),data=buffer.getChannelData(0);
      for(let i=0;i<count;i++)data[i]=(Math.random()*2-1)*(1-i/count);
      const source=ctx.createBufferSource(),filter=ctx.createBiquadFilter(),g=ctx.createGain();
      source.buffer=buffer;filter.type='lowpass';filter.frequency.value=cutoff;g.gain.value=gain;
      source.connect(filter);filter.connect(g);g.connect(master);source.start();
    }

    function vibrate(pattern){if(settings.haptics&&navigator.vibrate)navigator.vibrate(pattern);}

    function update(){
      if(!settings.audio||!ctx||ctx.state!=='running'||!rcsGain)return;
      const l=state.input.left,r=state.input.right;
      const magnitude=Math.min(1,(Math.hypot(l.x,l.y)+Math.hypot(r.x,r.y))*.58);
      const target=state.running&&!state.docked?magnitude*.08:0;
      if(target!==0&&Math.abs(target-lastRcsTarget)<.003)return;
      if(target===0&&lastRcsTarget===0)return;
      lastRcsTarget=target;rcsGain.gain.setTargetAtTime(target,ctx.currentTime,.045);
    }

    function badContact(){unlock();burst(.10,.055,760);tone(118,.13,.055,'triangle');vibrate(24);}
    function softCapture(){unlock();tone(330,.12,.055);tone(520,.17,.045,'sine',.045);vibrate([16,28,30]);}
    function latch(){unlock();tone(210,.09,.045,'triangle');tone(430,.11,.035,'sine',.055);vibrate([12,28,18]);}
    function nextTarget(){unlock();tone(410,.08,.035,'sine',.12);tone(620,.10,.03,'sine',.19);}
    function missionComplete(){unlock();tone(330,.12,.05);tone(495,.14,.045,'sine',.10);tone(660,.22,.04,'sine',.21);vibrate([20,35,20,45,45]);}
    function silence(){lastRcsTarget=0;if(ctx&&rcsGain)rcsGain.gain.setTargetAtTime(0,ctx.currentTime,.025);}

    const arm=()=>{unlock();};
    document.addEventListener('pointerdown',arm,{passive:true,capture:true});
    document.addEventListener('touchstart',arm,{passive:true,capture:true});
    document.addEventListener('click',arm,{passive:true,capture:true});
    document.addEventListener('visibilitychange',()=>{if(document.hidden)silence();});
    window.addEventListener('pagehide',silence);

    return Object.freeze({settings,unlock,update,badContact,softCapture,latch,nextTarget,missionComplete,silence,audioState:()=>ctx?ctx.state:'unavailable'});
  };
})();
