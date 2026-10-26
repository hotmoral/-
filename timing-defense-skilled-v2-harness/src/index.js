const VERSION = "linkline-nl6-repair-preview-v1";
const SESSION_ID = "NL6_MATCHED_1_REPAIR_1";
const EXPECTED_APP_BLOB = "4eb9fa0c7deded41d9e33074618873edd760c86a";
const EXPECTED_PROTOCOL_BLOB = "bf076ae47a21c2aab7004b2ee5aa4bcb9d051868";

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store"
    }
  });
}

function replaceOnce(text, oldValue, newValue) {
  const first = text.indexOf(oldValue);
  if (first < 0 || text.indexOf(oldValue, first + oldValue.length) >= 0) {
    throw new Error("MATERIALIZATION_CARDINALITY");
  }
  return text.slice(0, first) + newValue + text.slice(first + oldValue.length);
}

function materializeApp(text) {
  return replaceOnce(
    text,
    "a.download='linkline-nl5-matched-repair-1.json'",
    "a.download='linkline-nl6-matched-repair-1.json'"
  );
}

function materializeProtocol(text) {
  text = replaceOnce(text, "LINKLINE_A3_NL5_RUNTIME_ANALYSIS_METADATA", "LINKLINE_A3_NL6_RUNTIME_ANALYSIS_METADATA");
  text = replaceOnce(
    text,
    "\nexport async function validateSessionBundle(bundle,metadata){",
    "\nconst EXPECTED_PAIR_SHAPES=Object.freeze([\n" +
      "  {axis:'SAME_L',controlN:4,controlL:8,largerN:6,largerL:8},\n" +
      "  {axis:'OCCUPANCY_40_EXACT_DISTANCE',controlN:4,controlL:6,largerN:6,largerL:15},\n" +
      "  {axis:'SAME_L',controlN:4,controlL:9,largerN:6,largerL:9},\n" +
      "  {axis:'OCCUPANCY_40_EXACT_DISTANCE',controlN:4,controlL:6,largerN:6,largerL:15},\n" +
      "  {axis:'SAME_L',controlN:4,controlL:9,largerN:6,largerL:9},\n" +
      "  {axis:'OCCUPANCY_40_EXACT_DISTANCE',controlN:4,controlL:7,largerN:6,largerL:15}\n" +
      "]);\n\nexport async function validateSessionBundle(bundle,metadata){"
  );
  text = replaceOnce(text, "if(bundle?.largerN!==5)errors.push('largerN');", "if(bundle?.largerN!==6)errors.push('largerN');");
  text = replaceOnce(
    text,
    "  const quarantine=new Set(QUARANTINED_RESEARCH_EQUIVALENCE_IDS),ids=new Set();\n  const lengthCounts=new Map([[6,0],[7,0],[9,0]]);",
    "  const quarantine=new Set(QUARANTINED_RESEARCH_EQUIVALENCE_IDS),ids=new Set();"
  );
  text = replaceOnce(
    text,
    "    const pair=bundle.pairs?.[pairIndex],position=pairIndex+1;",
    "    const pair=bundle.pairs?.[pairIndex],position=pairIndex+1,shape=EXPECTED_PAIR_SHAPES[pairIndex];"
  );
  text = replaceOnce(text, "if(pair?.axis!=='SAME_L')errors.push(`pairAxis:${position}`);", "if(pair?.axis!==shape.axis)errors.push(`pairAxis:${position}`);");
  text = replaceOnce(text, "p.axis!=='SAME_L'", "p.axis!==shape.axis");
  text = replaceOnce(
    text,
    "    if(members[0].length!==members[1].length||!lengthCounts.has(members[0].length))errors.push(`pairLength:${position}`);\n" +
      "    else lengthCounts.set(members[0].length,lengthCounts.get(members[0].length)+1);\n" +
      "    const control=members.find(p=>p.pairMember==='control'),larger=members.find(p=>p.pairMember==='larger');\n" +
      "    if(!control||!larger||control.n!==4||larger.n!==5)errors.push(`pairMembers:${position}`);",
    "    const control=members.find(p=>p.pairMember==='control'),larger=members.find(p=>p.pairMember==='larger');\n" +
      "    if(!control||!larger)errors.push(`pairMembers:${position}`);\n" +
      "    else{\n" +
      "      if(control.n!==shape.controlN||control.length!==shape.controlL||larger.n!==shape.largerN||larger.length!==shape.largerL)errors.push(`pairShape:${position}`);\n" +
      "      if(shape.axis==='SAME_L'&&control.length!==larger.length)errors.push(`pairLength:${position}`);\n" +
      "      if(shape.axis==='OCCUPANCY_40_EXACT_DISTANCE'&&metadata?.shortestDistanceByResearchEquivalenceIdV1?.[control.researchEquivalenceIdV1]!==metadata?.shortestDistanceByResearchEquivalenceIdV1?.[larger.researchEquivalenceIdV1])errors.push(`pairExactDistance:${position}`);\n" +
      "    }"
  );
  text = replaceOnce(text, "  for(const [length,count] of lengthCounts)if(count!==2)errors.push(`lengthPairCount:${length}:${count}`);\n\n", "\n");
  text = replaceOnce(text, "if(![4,5].includes(puzzle.n))", "if(![4,6].includes(puzzle.n))");
  return text;
}

async function gitBlobSha(text) {
  const body = new TextEncoder().encode(text);
  const header = new TextEncoder().encode(`blob ${body.byteLength}\0`);
  const bytes = new Uint8Array(header.byteLength + body.byteLength);
  bytes.set(header, 0);
  bytes.set(body, header.byteLength);
  const digest = await crypto.subtle.digest("SHA-1", bytes);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function materializedAsset(request, env, basePath, transform, expectedBlob) {
  const baseUrl = new URL(request.url);
  baseUrl.pathname = basePath;
  baseUrl.search = "";
  const baseResponse = await env.ASSETS.fetch(new Request(baseUrl.toString(), { method: "GET" }));
  if (!baseResponse.ok) return new Response("base asset missing", { status: 500 });
  const text = transform(await baseResponse.text());
  const blob = await gitBlobSha(text);
  if (blob !== expectedBlob) return new Response("canonical asset mismatch", { status: 500 });
  return new Response(text, {
    status: 200,
    headers: {
      "content-type": "text/javascript; charset=utf-8",
      "cache-control": "no-store",
      "x-linkline-git-blob": blob,
      "x-linkline-session": SESSION_ID
    }
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    try {
      if (url.pathname === "/api/health") {
        return json({
          ok: true,
          version: VERSION,
          lane: "LINKLINE_NL6_PREVIEW_ONLY",
          sessionId: SESSION_ID,
          humanCollectionEnabled: false,
          canonicalAppBlob: EXPECTED_APP_BLOB,
          canonicalProtocolBlob: EXPECTED_PROTOCOL_BLOB,
          campaignPersistence: false,
          externalTelemetry: false
        });
      }
      if (url.pathname === "/app.mjs") {
        return await materializedAsset(request, env, "/app.base.mjs", materializeApp, EXPECTED_APP_BLOB);
      }
      if (url.pathname === "/protocol.mjs") {
        return await materializedAsset(request, env, "/protocol.base.mjs", materializeProtocol, EXPECTED_PROTOCOL_BLOB);
      }
      if (url.pathname === "/app.base.mjs" || url.pathname === "/protocol.base.mjs") {
        return new Response("Not Found", { status: 404 });
      }
      return env.ASSETS.fetch(request);
    } catch (error) {
      return json({ ok: false, error: "LINKLINE_PREVIEW_MATERIALIZATION_FAILED" }, 500);
    }
  }
};
