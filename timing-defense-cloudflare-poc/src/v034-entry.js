import baseWorker, { TimingDefenseRoom } from "./v033-entry.js";

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" }
  });
}

const worker = {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (request.method === "GET" && url.pathname === "/api/health") {
      return json({
        ok: true,
        service: "timing-defense-cloudflare-v034-render",
        version: "0.34-cf.1",
        transport: "websocket-hibernation",
        authority: "durable-object-event-driven-stage1",
        presentation: "id-reconcile-smooth-remote-projectiles-local-impact-prediction",
        locationHint: "apac-ne",
        scope: "room-ready-start-stage1-render-parity"
      });
    }
    if (request.method === "GET" && url.pathname === "/") {
      const assetUrl = new URL(request.url);
      assetUrl.pathname = "/v034-cloudflare.html";
      return env.ASSETS.fetch(new Request(assetUrl, request));
    }
    return baseWorker.fetch(request, env, ctx);
  }
};

export default worker;
export { TimingDefenseRoom };
