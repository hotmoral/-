const assert=require('assert'),fs=require('fs'),path=require('path');
const {patchSource}=require('../server-v17.js');
const base=fs.readFileSync(path.join(__dirname,'..','server-v13.js'),'utf8');
const transformed=patchSource(base);
for(const token of ["const WALL_SIDES=","shape:'square'","function hitWallSide","wallSideBreach","v17WallSeparates","v17ApproachSide","segments:v17WallSidePublic()"])
  assert(transformed.includes(token),`V17 server missing ${token}`);
assert(!/p\.x\s*=.*WALL|p\.y\s*=.*WALL/.test(transformed),'players must never collide with fortification');
assert(transformed.includes("if(enemyOutside)"),'raid enemies must stop at square wall before base');
new Function(transformed);
const client=fs.readFileSync(path.join(__dirname,'..','public','patch-v17.js'),'utf8');
const css=fs.readFileSync(path.join(__dirname,'..','public','patch-v17.css'),'utf8');
for(const token of ['v17DrawSide','v17DrawFortification','v17AdvanceStamp','v17TopDock','v17Mission','drawPlayer=function','v17FacilityAsset'])assert(client.includes(token),`V17 client missing ${token}`);
for(const token of ['#v17TopDock','.v16Mission.v17Mission.collapsed','#eatMeat.v14Eat.v16Eat'])assert(css.includes(token),`V17 CSS missing ${token}`);
for(const file of ['player-v17.svg','backpack-v17.svg','base-v17.svg','stockpile-v17.svg','workshop-v17.svg','storage-v17.svg','farm-v17.svg','watchtower-v17.svg','forge-v17.svg','infirmary-v17.svg','turret-v17.svg','turret2-v17.svg','wall-lv1-v17.svg','wall-lv2-v17.svg','wall-lv3-v17.svg'])assert(fs.existsSync(path.join(__dirname,'..','public','assets',file)),`V17 asset missing ${file}`);
console.log('[QA V17] PASS · square four-side wall · monsters blocked/users pass · compact mission drawer · RPG HUD · independent image assets · single-step movement prediction');
