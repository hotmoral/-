import Phaser from 'https://cdn.jsdelivr.net/npm/phaser@3.90.0/dist/phaser.esm.js';

const PIXELS_PER_METER=32;
const PLAYER_SPEED_MPS=5;
const WORLD_MIN_X=-900,WORLD_MAX_X=900,WORLD_MIN_Y=-650,WORLD_MAX_Y=650;
const START_X=-760,START_Y=100;

const runtimeInput={
  joystick:{x:0,y:0,magnitude:0},keyboard:{x:0,y:0},activeTouchPointers:0,lastSkillPress:{index:0,sequence:0},
  setJoystick(x,y,magnitude){this.joystick={x,y,magnitude};},
  setKeyboard(x,y){this.keyboard={x,y};},
  getMovement(){
    let x=this.joystick.magnitude>0.01?this.joystick.x:this.keyboard.x;
    let y=this.joystick.magnitude>0.01?this.joystick.y:this.keyboard.y;
    const m=Math.hypot(x,y); if(m>1){x/=m;y/=m;} return {x,y};
  },
  pressSkill(index){this.lastSkillPress={index,sequence:this.lastSkillPress.sequence+1};}
};

const telemetry={playerX:START_X,playerY:START_Y,fps:0,cameraZoom:1,viewportWidth:innerWidth,viewportHeight:innerHeight,activePointers:0,lastSkillIndex:0,hp:120,maxHp:120,mp:100,maxMp:100,carriedGem:0};
window.__DEEPHOLD_I1_QA__={runtimeInput,telemetry,build:'cloudflare-subpath-qa'};

class JoystickController{
  constructor(zone){this.zone=zone;this.pointerId=null;this.thumb=zone.querySelector('.joystick-thumb');
    zone.addEventListener('pointerdown',e=>this.down(e),{passive:false});
    zone.addEventListener('pointermove',e=>this.move(e),{passive:false});
    zone.addEventListener('pointerup',e=>this.end(e),{passive:false});
    zone.addEventListener('pointercancel',e=>this.end(e),{passive:false});
    zone.addEventListener('lostpointercapture',e=>this.lost(e));
  }
  down(e){if(this.pointerId!==null)return;e.preventDefault();this.pointerId=e.pointerId;runtimeInput.activeTouchPointers++;this.zone.classList.add('is-active');this.zone.setPointerCapture(e.pointerId);this.update(e);}
  move(e){if(e.pointerId!==this.pointerId)return;e.preventDefault();this.update(e);}
  end(e){if(e.pointerId!==this.pointerId)return;e.preventDefault();this.reset();}
  lost(e){if(e.pointerId!==this.pointerId)return;this.reset();}
  update(e){const r=this.zone.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2,rx=e.clientX-cx,ry=e.clientY-cy,d=Math.hypot(rx,ry),max=r.width*.30,clamp=Math.min(d,max),mag=max>0?Math.min(1,d/max):0,dx=d>0?rx/d:0,dy=d>0?ry/d:0,vx=dx*clamp,vy=dy*clamp;this.thumb.style.transform=`translate(calc(-50% + ${vx}px), calc(-50% + ${vy}px))`;runtimeInput.setJoystick(dx*mag,dy*mag,mag);}
  reset(){if(this.pointerId!==null)runtimeInput.activeTouchPointers=Math.max(0,runtimeInput.activeTouchPointers-1);this.pointerId=null;this.zone.classList.remove('is-active');this.thumb.style.transform='translate(-50%, -50%)';runtimeInput.setJoystick(0,0,0);}
}

class SkillBarController{
  constructor(root){this.buttons=[...root.querySelectorAll('.skill-button')];
    for(const b of this.buttons){b._pointerId=null;b.addEventListener('pointerdown',e=>this.down(e),{passive:false});b.addEventListener('pointerup',e=>this.end(e),{passive:false});b.addEventListener('pointercancel',e=>this.end(e),{passive:false});b.addEventListener('lostpointercapture',e=>this.lost(e));}
    addEventListener('keydown',e=>this.key(e));
  }
  down(e){e.preventDefault();const b=e.currentTarget;if(b._pointerId!==null)return;const i=Number(b.dataset.skillIndex||0);if(i<1||i>5)return;b._pointerId=e.pointerId;runtimeInput.activeTouchPointers++;b.classList.add('is-pressed');b.setPointerCapture(e.pointerId);runtimeInput.pressSkill(i);}
  end(e){e.preventDefault();const b=e.currentTarget;if(b._pointerId!==e.pointerId)return;b._pointerId=null;runtimeInput.activeTouchPointers=Math.max(0,runtimeInput.activeTouchPointers-1);b.classList.remove('is-pressed');}
  lost(e){const b=e.currentTarget;if(b._pointerId!==e.pointerId)return;b._pointerId=null;runtimeInput.activeTouchPointers=Math.max(0,runtimeInput.activeTouchPointers-1);b.classList.remove('is-pressed');}
  key(e){if(e.repeat)return;const i=Number(e.key);if(i<1||i>5)return;runtimeInput.pressSkill(i);const b=this.buttons[i-1];b?.classList.add('is-pressed');setTimeout(()=>b?.classList.remove('is-pressed'),110);}
}

class HudController{
  constructor(root){root.innerHTML=`
    <section class="player-status hud-panel"><div class="status-line"><span class="status-label">HP</span><div class="meter hp-meter"><span data-hp-fill></span></div><span class="status-value" data-hp-value>120/120</span></div><div class="status-line"><span class="status-label">MP</span><div class="meter mp-meter"><span data-mp-fill></span></div><span class="status-value" data-mp-value>100/100</span></div><div class="status-line"><span class="status-label">GEM</span><div class="meter gem-meter"><span data-gem-fill></span></div><span class="status-value" data-gem-value>0</span></div></section>
    <section class="minimap hud-panel"><div class="minimap-grid"></div><div class="minimap-player" data-minimap-player></div><div class="minimap-caption">FALLEN BASIN · I1 QA</div></section>
    <section class="joystick-zone"><div class="joystick-base"></div><div class="joystick-thumb"></div></section>
    <section class="skill-cluster"><button class="skill-button skill-1" data-skill-index="1" data-key="1">S1</button><button class="skill-button skill-2" data-skill-index="2" data-key="2">S2</button><button class="skill-button skill-3" data-skill-index="3" data-key="3">S3</button><button class="skill-button skill-4" data-skill-index="4" data-key="4">S4</button><button class="skill-button skill-5 signature" data-skill-index="5" data-key="5">S5</button></section>
    <div class="debug-overlay" data-debug-overlay>I1 QA</div>`;
    this.hpFill=root.querySelector('[data-hp-fill]');this.mpFill=root.querySelector('[data-mp-fill]');this.gemFill=root.querySelector('[data-gem-fill]');this.hpValue=root.querySelector('[data-hp-value]');this.mpValue=root.querySelector('[data-mp-value]');this.gemValue=root.querySelector('[data-gem-value]');this.mapPlayer=root.querySelector('[data-minimap-player]');this.debug=root.querySelector('[data-debug-overlay]');
    new JoystickController(root.querySelector('.joystick-zone'));new SkillBarController(root.querySelector('.skill-cluster'));this.loop();
  }
  loop(){const hp=Math.max(0,Math.min(1,telemetry.hp/telemetry.maxHp)),mp=Math.max(0,Math.min(1,telemetry.mp/telemetry.maxMp)),gem=Math.min(1,telemetry.carriedGem/100);this.hpFill.style.transform=`scaleX(${hp})`;this.mpFill.style.transform=`scaleX(${mp})`;this.gemFill.style.transform=`scaleX(${gem})`;this.hpValue.textContent=`${Math.round(telemetry.hp)}/${telemetry.maxHp}`;this.mpValue.textContent=`${Math.round(telemetry.mp)}/${telemetry.maxMp}`;this.gemValue.textContent=String(telemetry.carriedGem);const mx=(telemetry.playerX-WORLD_MIN_X)/(WORLD_MAX_X-WORLD_MIN_X),my=(telemetry.playerY-WORLD_MIN_Y)/(WORLD_MAX_Y-WORLD_MIN_Y);this.mapPlayer.style.left=`${Math.max(3,Math.min(97,mx*100))}%`;this.mapPlayer.style.top=`${Math.max(3,Math.min(97,my*100))}%`;this.debug.textContent=`I1 · ${Math.round(telemetry.fps)} FPS · ${telemetry.viewportWidth}×${telemetry.viewportHeight} · Z ${telemetry.cameraZoom.toFixed(2)} · PTR ${telemetry.activePointers} · ${telemetry.lastSkillIndex?`S${telemetry.lastSkillIndex}`:'S–'}`;requestAnimationFrame(()=>this.loop());}
}

const REGION_ANCHORS=[['R0 · ASH CRADLE',-760,100],['R1 · GLOWCAP',-585,320],['R2 · SPLIT GALLERY',-390,60],['R3 · GNAWER',-360,-300],['R4 · RUSTVEIN',-20,50],['R5 · IRON LIFT',0,430],['R6 · IRONBACK',350,20],['R7 · CHAIN POST',650,280],['R8 · DEEP SCAR',780,-300]];

class WorldScene extends Phaser.Scene{
  constructor(){super('WorldScene');this.lastSkillSequence=0;}
  create(){this.cameras.main.setBackgroundColor('#0b1011');this.drawWorld();this.createPlayer();this.configureCamera();this.configureKeyboard();this.scale.on(Phaser.Scale.Events.RESIZE,()=>this.applyZoom());}
  update(_time,delta){this.updateKeyboard();const m=runtimeInput.getMovement(),ds=Math.min(delta,50)/1000,sp=PLAYER_SPEED_MPS*PIXELS_PER_METER;this.player.x+=m.x*sp*ds;this.player.y+=m.y*sp*ds;const margin=20*PIXELS_PER_METER;this.player.x=Phaser.Math.Clamp(this.player.x,WORLD_MIN_X*PIXELS_PER_METER+margin,WORLD_MAX_X*PIXELS_PER_METER-margin);this.player.y=Phaser.Math.Clamp(this.player.y,WORLD_MIN_Y*PIXELS_PER_METER+margin,WORLD_MAX_Y*PIXELS_PER_METER-margin);this.cameras.main.setFollowOffset(-m.x*70,-m.y*46);this.skillPulse();telemetry.playerX=this.player.x/PIXELS_PER_METER;telemetry.playerY=this.player.y/PIXELS_PER_METER;telemetry.fps=this.game.loop.actualFps;telemetry.cameraZoom=this.cameras.main.zoom;telemetry.viewportWidth=this.scale.width;telemetry.viewportHeight=this.scale.height;telemetry.activePointers=runtimeInput.activeTouchPointers;telemetry.lastSkillIndex=runtimeInput.lastSkillPress.index;}
  drawWorld(){const g=this.add.graphics(),minX=WORLD_MIN_X*PIXELS_PER_METER,maxX=WORLD_MAX_X*PIXELS_PER_METER,minY=WORLD_MIN_Y*PIXELS_PER_METER,maxY=WORLD_MAX_Y*PIXELS_PER_METER,step=96*PIXELS_PER_METER;g.lineStyle(1,0x32403b,.28);for(let x=minX;x<=maxX;x+=step)g.lineBetween(x,minY,x,maxY);for(let y=minY;y<=maxY;y+=step)g.lineBetween(minX,y,maxX,y);g.lineStyle(3,0x58685f,.5);g.strokeRect(minX,minY,maxX-minX,maxY-minY);for(const [label,xm,ym] of REGION_ANCHORS){const x=xm*PIXELS_PER_METER,y=ym*PIXELS_PER_METER;this.add.circle(x,y,24,0xa8b6ad,.18).setStrokeStyle(2,0xb7c4bc,.32);this.add.text(x+34,y-10,label,{color:'#8fa098',fontFamily:'monospace',fontSize:'20px'}).setOrigin(0,.5);}this.add.text(START_X*PIXELS_PER_METER,START_Y*PIXELS_PER_METER-95,'DEEPHOLD · I1 CLOUDFARE QA',{color:'#d6ded8',fontFamily:'system-ui, sans-serif',fontSize:'28px',fontStyle:'bold'}).setOrigin(.5);}
  createPlayer(){const shadow=this.add.ellipse(0,12,34,18,0x000000,.34),body=this.add.circle(0,0,17,0xd6d0b7,1).setStrokeStyle(3,0x343d39,1),core=this.add.circle(5,-5,5,0x9da8c7,1),facing=this.add.triangle(0,-24,0,10,7,-4,-7,-4,0xe9e5d2,.9);this.player=this.add.container(START_X*PIXELS_PER_METER,START_Y*PIXELS_PER_METER,[shadow,body,core,facing]);this.player.setDepth(10);}
  configureCamera(){const minX=WORLD_MIN_X*PIXELS_PER_METER,minY=WORLD_MIN_Y*PIXELS_PER_METER,w=(WORLD_MAX_X-WORLD_MIN_X)*PIXELS_PER_METER,h=(WORLD_MAX_Y-WORLD_MIN_Y)*PIXELS_PER_METER;this.cameras.main.setBounds(minX,minY,w,h);this.cameras.main.startFollow(this.player,true,.12,.12);this.applyZoom();}
  applyZoom(){this.cameras.main.setZoom(Phaser.Math.Clamp((this.scale.height||innerHeight)/900,.72,1.05));}
  configureKeyboard(){if(!this.input.keyboard)return;this.cursors=this.input.keyboard.createCursorKeys();this.wasd={w:this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W),a:this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A),s:this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S),d:this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D)};}
  updateKeyboard(){const l=!!(this.cursors?.left.isDown||this.wasd?.a.isDown),r=!!(this.cursors?.right.isDown||this.wasd?.d.isDown),u=!!(this.cursors?.up.isDown||this.wasd?.w.isDown),d=!!(this.cursors?.down.isDown||this.wasd?.s.isDown);runtimeInput.setKeyboard(Number(r)-Number(l),Number(d)-Number(u));}
  skillPulse(){const p=runtimeInput.lastSkillPress;if(p.sequence===this.lastSkillSequence)return;this.lastSkillSequence=p.sequence;const c=this.add.circle(this.player.x,this.player.y,25,0xffffff,0).setStrokeStyle(4,0xdcd7ad,.8).setDepth(9);this.tweens.add({targets:c,scaleX:2.3,scaleY:2.3,alpha:0,duration:260,ease:'Quad.Out',onComplete:()=>c.destroy()});}
}

const game=new Phaser.Game({type:Phaser.AUTO,parent:'game-root',backgroundColor:'#080b0d',transparent:false,antialias:true,pixelArt:false,roundPixels:false,banner:false,input:{activePointers:5,smoothFactor:0},scale:{mode:Phaser.Scale.RESIZE,width:innerWidth,height:innerHeight,autoCenter:Phaser.Scale.CENTER_BOTH},render:{antialias:true,powerPreference:'high-performance'},scene:[WorldScene]});
new HudController(document.querySelector('#hud-root'));
addEventListener('contextmenu',e=>e.preventDefault());document.addEventListener('touchmove',e=>{if(e.cancelable)e.preventDefault();},{passive:false});document.addEventListener('visibilitychange',()=>{document.hidden?game.loop.sleep():game.loop.wake();});
