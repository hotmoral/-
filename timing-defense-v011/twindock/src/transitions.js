(() => {
  'use strict';
  const TD = window.TwinDock;

  TD.Transitions = function Transitions(ui){
    const stage=document.getElementById('stageTransition');
    const stageKicker=document.getElementById('stageKicker');
    const stageTitle=document.getElementById('stageTitle');
    const complete=document.getElementById('missionCompleteFx');
    const completeText=document.getElementById('missionCompleteText');
    const missionHud=document.getElementById('missionHud');
    let stageTimer=0,completeTimer=0,progressTimer=0;

    function retrigger(el,cls){
      if(!el)return;
      el.classList.remove(cls);
      void el.offsetWidth;
      el.classList.add(cls);
    }

    function reset(){
      clearTimeout(stageTimer);clearTimeout(completeTimer);clearTimeout(progressTimer);
      stage?.classList.remove('on');complete?.classList.remove('on');
      missionHud?.classList.remove('progressPulse','finalHold');
    }

    function progress(){
      if(!missionHud)return;
      clearTimeout(progressTimer);retrigger(missionHud,'progressPulse');
      progressTimer=setTimeout(()=>missionHud.classList.remove('progressPulse'),520);
    }

    function nextTarget(profile,index,total){
      if(!stage||!stageKicker||!stageTitle)return;
      clearTimeout(stageTimer);
      stageKicker.textContent=`TARGET ${index} / ${total}`;
      stageTitle.textContent=profile.label;
      retrigger(stage,'on');
      stageTimer=setTimeout(()=>stage.classList.remove('on'),980);
    }

    function missionComplete(total){
      if(!complete)return;
      clearTimeout(completeTimer);
      if(completeText)completeText.textContent=`${total} / ${total} DOCKS COMPLETE`;
      missionHud?.classList.add('finalHold');
      retrigger(complete,'on');
      completeTimer=setTimeout(()=>complete.classList.remove('on'),1900);
    }

    return Object.freeze({reset,progress,nextTarget,missionComplete});
  };
})();
