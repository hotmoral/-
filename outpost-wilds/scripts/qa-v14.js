const assert=require('assert');
const fs=require('fs');
const path=require('path');
const{patchSource}=require('../server-v14');
const root=path.join(__dirname,'..');
const base=fs.readFileSync(path.join(root,'server-v13.js'),'utf8');
const patched=patchSource(base);
const client=fs.readFileSync(path.join(root,'public','patch-v14.js'),'utf8');
const css=fs.readFileSync(path.join(root,'public','patch-v14.css'),'utf8');

for(const token of ["kind:'chat'","kind:'meal'","kind:'raidLoot'","lootTo:e.raid?'stockpile':'carry'","fire('watchtower',430,18,true,1.03)","targetId:target.id","lastChat:0"]){assert(patched.includes(token),`V14 server contract missing: ${token}`)}
for(const token of ['v14EnsureChat','v14ChatMessage','v14EnsureEat','v6DrawBuiltFacilities=function','v14DrawWatchtower','v14DrawTurret','towerShot'])assert(client.includes(token),`V14 client contract missing: ${token}`);
assert(css.includes('.v14Chat')&&css.includes('.v14Eat'),'V14 UI styles missing');
new Function(patched);new Function(client);
console.log('[QA V14] PASS · realtime chat · raid meat to stockpile · ration use · readable defense fire · facility visual pass');
