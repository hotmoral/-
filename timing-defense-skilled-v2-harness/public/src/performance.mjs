export const PERFORMANCE_BASELINE_SCHEMA = 'LINKLINE_PERFORMANCE_BASELINE';
export const PERFORMANCE_BASELINE_VERSION = '1.0.0';
export const PERFORMANCE_BASELINE_METRIC = 'M3_V1_SHORTEST_DISTANCE';
export const PERFORMANCE_BASELINE_SHA256 = '25e395b6761dba58f62514456857fbb7c16d4b25cb4e7b8f053532142f38c144';
export const PERFORMANCE_GRADES = Object.freeze(['S+', 'A+', 'B+']);

async function sha256Hex(text) {
  const subtle = globalThis.crypto?.subtle;
  if (!subtle) throw new Error('CRYPTO_SUBTLE_UNAVAILABLE');
  const digest = await subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map((value) => value.toString(16).padStart(2, '0')).join('');
}

export function validatePerformanceBaseline(raw, campaignId, availableCount) {
  if (!raw || raw.schema !== PERFORMANCE_BASELINE_SCHEMA) throw new Error('PERFORMANCE_BASELINE_SCHEMA');
  if (raw.version !== PERFORMANCE_BASELINE_VERSION) throw new Error('PERFORMANCE_BASELINE_VERSION');
  if (raw.campaignId !== campaignId) throw new Error('PERFORMANCE_BASELINE_CAMPAIGN');
  if (raw.metric !== PERFORMANCE_BASELINE_METRIC) throw new Error('PERFORMANCE_BASELINE_METRIC');
  if (raw.moveUnit !== 'accepted authoritative one-cell M2 action') throw new Error('PERFORMANCE_BASELINE_MOVE_UNIT');
  if (!Number.isInteger(raw.launchTotal) || raw.launchTotal !== availableCount) throw new Error('PERFORMANCE_BASELINE_TOTAL');
  if (JSON.stringify(raw.rowEncoding) !== JSON.stringify(['position', 'shortestDistance'])) throw new Error('PERFORMANCE_BASELINE_ENCODING');
  if (!Array.isArray(raw.rows) || raw.rows.length !== availableCount) throw new Error('PERFORMANCE_BASELINE_ROWS');

  const distances = new Array(availableCount + 1);
  for (let index = 0; index < raw.rows.length; index++) {
    const row = raw.rows[index];
    const position = index + 1;
    if (!Array.isArray(row) || row.length !== 2 || row[0] !== position) throw new Error('PERFORMANCE_BASELINE_POSITION');
    const distance = row[1];
    if (!Number.isInteger(distance) || distance < 1) throw new Error('PERFORMANCE_BASELINE_DISTANCE');
    distances[position] = distance;
  }

  return Object.freeze({
    campaignId: raw.campaignId,
    launchTotal: raw.launchTotal,
    metric: raw.metric,
    distances: Object.freeze(distances),
  });
}

export async function loadPerformanceBaseline(url, campaignId, availableCount, fetchImpl = globalThis.fetch) {
  if (typeof fetchImpl !== 'function') throw new Error('FETCH_UNAVAILABLE');
  const response = await fetchImpl(url, { cache: 'no-store' });
  if (!response.ok) throw new Error(`PERFORMANCE_BASELINE_FETCH_${response.status}`);
  const text = await response.text();
  const digest = await sha256Hex(text);
  if (digest !== PERFORMANCE_BASELINE_SHA256) throw new Error('PERFORMANCE_BASELINE_SHA256');
  return validatePerformanceBaseline(JSON.parse(text), campaignId, availableCount);
}

export function gradePerformance(moves, shortestDistance) {
  if (!Number.isInteger(moves) || moves < 1) throw new Error('PERFORMANCE_MOVES');
  if (!Number.isInteger(shortestDistance) || shortestDistance < 1) throw new Error('PERFORMANCE_DISTANCE');
  if (moves < shortestDistance) {
    return Object.freeze({
      ok: false,
      reason: 'PERFORMANCE_BELOW_OPTIMUM',
      moves,
      shortestDistance,
    });
  }
  const grade = moves === shortestDistance ? 'S+' : moves === shortestDistance + 1 ? 'A+' : 'B+';
  return Object.freeze({ ok: true, grade, moves, shortestDistance });
}
