import worker, { TimingDefenseRoom } from "./v041-flyer-entry.js";
import { runMonsterCapabilityV1SelfTest } from "./monster-capability-v1-selftest.js";
import { runV039SelfTest } from "./v039-selftest.js";
import { runV040ShieldSelfTest } from "./v040-shield-selftest.js";
import { runV041FlyerSelfTest } from "./v041-flyer-selftest.js";

function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}

const auditedWorker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health")return json({
      ok:true,service:"timing-defense-v041-flyer-y-capability",version:"0.41-cf.1",
      transport:"websocket-hibernation-per-socket-event-cursor",authority:"v040-plus-stage-independent-flyer-y",
      flyer:{status:"capability-enabled",speed:.100,size:.78,knockResist:.90,oscAmp:.020,oscOmega:5,balance:"provisional",groundImmunity:false},
      validation:"foundation-plus-v039-plus-v040-shield-plus-v041-flyer",
      campaign:{legacyStage5_6:"blocked",final50:"not-authored"},scope:"flyer-authoritative-y-geometry"
    });
    if(request.method==="GET"&&url.pathname==="/api/diagnostics/v041-flyer"){
      try{
        const foundation=runMonsterCapabilityV1SelfTest();
        const v039=runV039SelfTest(TimingDefenseRoom);
        const shield=runV040ShieldSelfTest(TimingDefenseRoom);
        const flyer=runV041FlyerSelfTest(TimingDefenseRoom);
        const ok=foundation.ok&&v039.ok&&shield.ok&&flyer.ok;
        return json({ok,version:"0.41-cf.1-diagnostics",foundation,v039,shield,flyer},ok?200:500);
      }catch(error){return json({ok:false,version:"0.41-cf.1-diagnostics",error:String(error?.stack||error)},500)}
    }
    return worker.fetch(request,env,ctx);
  }
};

export default auditedWorker;
export { TimingDefenseRoom };
