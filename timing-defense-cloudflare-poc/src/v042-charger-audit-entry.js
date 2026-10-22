import worker, { TimingDefenseRoom } from "./v042-charger-entry.js";
import { runMonsterCapabilityV1SelfTest } from "./monster-capability-v1-selftest.js";
import { runV039SelfTest } from "./v039-selftest.js";
import { runV040ShieldSelfTest } from "./v040-shield-selftest.js";
import { runV041FlyerSelfTest } from "./v041-flyer-selftest.js";
import { runV042ChargerSelfTest } from "./v042-charger-selftest.js";

function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}

const auditedWorker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==='GET'&&url.pathname==='/api/health')return json({
      ok:true,service:'timing-defense-v042-charger-state-capability',version:'0.42-cf.1',
      transport:'websocket-hibernation-per-socket-event-cursor',authority:'v041-plus-stage-independent-charger-state',
      charger:{status:'capability-enabled',hp:380,baseSpeed:.060,windupMs:650,chargeSpeed:.210,triggerX:.62,rearmMs:900,knockResist:.80,reward:8,balance:'provisional'},
      validation:'foundation-plus-v039-plus-v040-shield-plus-v041-flyer-plus-v042-charger',
      campaign:{legacyStage4_10:'blocked',final50:'not-authored'},scope:'charger-authoritative-state-machine'
    });
    if(request.method==='GET'&&url.pathname==='/api/diagnostics/v042-charger'){
      try{
        const foundation=runMonsterCapabilityV1SelfTest();
        const v039=runV039SelfTest(TimingDefenseRoom);
        const shield=runV040ShieldSelfTest(TimingDefenseRoom);
        const flyer=runV041FlyerSelfTest(TimingDefenseRoom);
        const charger=runV042ChargerSelfTest(TimingDefenseRoom);
        const ok=foundation.ok&&v039.ok&&shield.ok&&flyer.ok&&charger.ok;
        return json({ok,version:'0.42-cf.1-diagnostics',foundation,v039,shield,flyer,charger},ok?200:500);
      }catch(error){return json({ok:false,version:'0.42-cf.1-diagnostics',error:String(error?.stack||error)},500)}
    }
    return worker.fetch(request,env,ctx);
  }
};

export default auditedWorker;
export { TimingDefenseRoom };
