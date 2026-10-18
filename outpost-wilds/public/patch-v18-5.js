/* Outpost Wilds V18.5: server-authoritative weapon attack/gather radii. */
const V185_RANGE_FALLBACK=[null,
 {attack:96,gather:88},{attack:104,gather:94},{attack:112,gather:100},{attack:118,gather:120},
 {attack:126,gather:108},{attack:138,gather:114},{attack:140,gather:132},{attack:154,gather:124},
 {attack:170,gather:130},{attack:188,gather:138},{attack:210,gather:146},{attack:360,gather:190},
 {attack:400,gather:210},{attack:440,gather:230},{attack:480,gather:250},{attack:525,gather:275}
];

v18DrawActionRanges=function(){
  const p=myPlayer();if(!p)return;
  const rr=v4Players.get(p.id),px=rr?.x??p.x,py=rr?.y??p.y,s=worldToScreen(px,py);
  const idx=Math.max(1,Math.min(16,Number(p.weaponIndex||p.gearLevel)||1)),fallback=V185_RANGE_FALLBACK[idx]||V185_RANGE_FALLBACK[1];
  const attack=Math.max(50,Number(p.attackRange||p.autoRange)||fallback.attack),gather=Math.max(40,Number(p.gatherRange)||fallback.gather);
  ctx.save();
  ctx.setLineDash([7,7]);ctx.strokeStyle='rgba(108,205,116,.62)';ctx.lineWidth=1.35;ctx.beginPath();ctx.arc(s.x,s.y+2,gather,0,Math.PI*2);ctx.stroke();
  ctx.setLineDash([]);ctx.strokeStyle='rgba(236,119,83,.66)';ctx.lineWidth=1.55;ctx.beginPath();ctx.arc(s.x,s.y+2,attack,0,Math.PI*2);ctx.stroke();
  ctx.restore();
};

if(window.__OW_CORE_RENDER_CONTRACT__)window.__OW_CORE_RENDER_CONTRACT__.weaponRanges='server-authoritative';
window.__OW_V185__={ranges:V185_RANGE_FALLBACK.slice(1),meleeToRangedJump:{attack:[210,360],gather:[146,190]}};
