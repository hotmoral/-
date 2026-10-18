/* Outpost Wilds V18.3: transient HUD collision hardening. */
(function(){
  const style=document.createElement('style');
  style.id='v183CollisionStyle';
  style.textContent=`
    body.v183-boss-visible #toast{
      top:max(158px,calc(env(safe-area-inset-top) + 154px))!important;
    }
  `;
  document.head.appendChild(style);

  const prevHud=updateHud;
  updateHud=function(){
    prevHud();
    const bossVisible=!!document.querySelector('#bossHud.show');
    document.body.classList.toggle('v183-boss-visible',bossVisible);
  };

  window.__OW_V183__={bossToastSeparation:true};
})();
