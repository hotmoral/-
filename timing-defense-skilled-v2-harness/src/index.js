const VERSION = "skilled-v2-harness-v0.1";

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store"
    }
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/health") {
      return json({
        ok: true,
        version: VERSION,
        lane: "HARNESS_ONLY",
        campaignPersistence: false,
        externalTelemetry: false
      });
    }
    return env.ASSETS.fetch(request);
  }
};
