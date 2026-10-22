import worker, { TimingDefenseRoom } from "./v043-splitter-entry.js";
import { runMonsterCapabilityV1SelfTest } from "./monster-capability-v1-selftest.js";
import { runV039SelfTest } from "./v039-selftest.js";
import { runV040ShieldSelfTest } from "./v040-shield-selftest.js";
import { runV041FlyerSelfTest } from "./v041-flyer-selftest.js";
import { runV042ChargerSelfTest } from "./v042-charger-selftest.js";
import { runV043SplitterSelfTest } from "./v043-splitter-selftest.js";

function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}

const auditedWorker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==='GET'&&url.pathname==='/api/health')return json({
      ok:true,service:'timing-defense-v043-splitter-kernel-capability',version:'0.43-cf.1',
      transport:'websocket-hibernation-per-socket-event-cursor',authority:'v042-plus-stage-independent-splitter-child-kernel',
      splitter:{status:'capability-enabled',rewardAccounting:{parent:4,childEach:2,package:8,status:'provisional-not-production-frozen'}},
      validation:'foundation-plus-v039-v040-v041-v042-plus-v043-splitter',
      campaign:{legacyStage4_10:'blocked',final50:'not-authored'},scope:'splitter-authoritative-child-spawn-kernel'
    });
    if(request.method==='GET'&&url.pathname==='/api/diagnostics/v043-splitter'){
      try{
        const foundation=runMonsterCapabilityV1SelfTest();
        const v039=runV039SelfTest(TimingDefenseRoom);
        const shield=runV040ShieldSelfTest(TimingDefenseRoom);
        const flyer=runV041FlyerSelfTest(TimingDefenseRoom);
        const charger=runV042ChargerSelfTest(TimingDefenseRoom);
        const splitter=runV043SplitterSelfTest(TimingDefenseRoom);
        const ok=foundation.ok&&v039.ok&&shield.ok&&flyer.ok&&charger.ok&&splitter.ok;
        return json({ok,version:'0.43-cf.1-diagnostics',foundation,v039,shield,flyer,charger,splitter},ok?200:500);
      }catch(error){return json({ok:false,version:'0.43-cf.1-diagnostics',error:String(error?.stack||error)},500)}
    }
    return worker.fetch(request,env,ctx);
  }
};

export default auditedWorker;
export { TimingDefenseRoom };
