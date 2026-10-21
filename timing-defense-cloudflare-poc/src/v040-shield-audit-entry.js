import worker, { TimingDefenseRoom } from "./v040-shield-entry.js";
import { runV039SelfTest } from "./v039-selftest.js";
import { runMonsterCapabilityV1SelfTest } from "./monster-capability-v1-selftest.js";
import { runV040ShieldSelfTest } from "./v040-shield-selftest.js";

function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}

const auditedWorker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health")return json({
      ok:true,service:"timing-defense-v040-shield-capability",version:"0.40-cf.1",
      transport:"websocket-hibernation-per-socket-event-cursor",
      authority:"v039-plus-stage-independent-shield-armor",
      shield:{status:"capability-enabled",armor:.72,knockResist:.62,size:1.08,speed:.057,balance:"provisional"},
      validation:"v039-regression-plus-capability-foundation-plus-shield-authority",
      campaign:{legacyStage4:"blocked",final50:"not-authored"},scope:"shield-common-armor-capability"
    });
    if(request.method==="GET"&&url.pathname==="/api/diagnostics/v040-shield"){
      try{
        const foundation=runMonsterCapabilityV1SelfTest();
        const v039=runV039SelfTest(TimingDefenseRoom);
        const shield=runV040ShieldSelfTest(TimingDefenseRoom);
        const ok=foundation.ok&&v039.ok&&shield.ok;
        return json({ok,version:"0.40-cf.1-diagnostics",foundation,v039,shield},ok?200:500);
      }catch(error){return json({ok:false,version:"0.40-cf.1-diagnostics",error:String(error?.stack||error)},500)}
    }
    return worker.fetch(request,env,ctx);
  }
};

export default auditedWorker;
export { TimingDefenseRoom };
