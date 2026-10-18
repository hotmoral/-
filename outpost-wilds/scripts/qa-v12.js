const assert=require('assert'),fs=require('fs'),path=require('path');
const{FACILITY_TIERS,WEAPON_TIERS}=require('../v11-config');
const src=fs.readFileSync(path.join(__dirname,'..','server-v12.js'),'utf8');
assert.equal(Object.keys(FACILITY_TIERS).length,9,'9 facilities retained');assert.equal(WEAPON_TIERS.length-1,5,'5 weapon families retained');
for(const token of ["SIGNAL_REQ={base:6","weaponLevel:3","totalStages:5","type==='overlord'","ENDGAME.mode='cleared'","m.type==='endless'","if(e.raid)updateRaidEnemy(e,dt);else updateWildEnemy(e,dt)"])assert(src.includes(token),`V12 contract missing: ${token}`);
assert(src.includes("if(!target){target=BASE"),'raid enemies retain base fallback');
const wild=src.slice(src.indexOf('function updateWildEnemy'),src.indexOf('function updateEnemy(e,dt)'));assert(!wild.includes('target=BASE'),'wild AI must never target base');
const final=src.slice(src.indexOf('function spawnFinalStage'),src.indexOf('function spawnWaveStage'));for(let i=1;i<=5;i++)assert(final.includes(`stage===${i}`),`final stage ${i} exists`);
console.log('[QA V12] PASS · wild/raid AI split · signal gate · 5 final waves · final boss · clear/endless contract');
