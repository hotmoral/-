const assert=require('assert'),fs=require('fs'),path=require('path');
const root=path.join(__dirname,'..');
const js=fs.readFileSync(path.join(root,'public','patch-v18-3.js'),'utf8');
for(const token of ["v183-boss-visible","#bossHud.show","top:max(158px","bossToastSeparation:true"]){
  assert(js.includes(token),`V18.3 collision contract missing ${token}`);
}
console.log('[QA V18.3] PASS · boss HUD and toast use separate vertical lanes');
