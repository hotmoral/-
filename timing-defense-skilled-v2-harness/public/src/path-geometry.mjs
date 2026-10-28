export function roundedOrthogonalPath(cells, n, {
  scale = 100,
  offset = 0,
  radiusRatio = 0.22,
} = {}) {
  if (!Array.isArray(cells) || cells.length === 0) return '';
  if (!Number.isInteger(n) || n < 1) throw new Error('INVALID_GRID_SIZE');

  const span = scale / n;
  const radius = Math.max(0, span * radiusRatio);
  const point = (cell) => {
    const row = Math.floor(cell / n);
    const col = cell % n;
    return [offset + (col + 0.5) * span, offset + (row + 0.5) * span];
  };
  const points = cells.map(point);
  const fmt = (value) => Number(value.toFixed(3));
  let d = `M ${fmt(points[0][0])} ${fmt(points[0][1])}`;

  for (let index = 1; index < points.length - 1; index++) {
    const previous = points[index - 1];
    const current = points[index];
    const next = points[index + 1];
    const incoming = [current[0] - previous[0], current[1] - previous[1]];
    const outgoing = [next[0] - current[0], next[1] - current[1]];
    const incomingLength = Math.hypot(...incoming);
    const outgoingLength = Math.hypot(...outgoing);
    const cross = incoming[0] * outgoing[1] - incoming[1] * outgoing[0];

    if (!incomingLength || !outgoingLength || Math.abs(cross) < 1e-9) {
      d += ` L ${fmt(current[0])} ${fmt(current[1])}`;
      continue;
    }

    const cornerRadius = Math.min(radius, incomingLength / 2, outgoingLength / 2);
    const entry = [
      current[0] - (incoming[0] / incomingLength) * cornerRadius,
      current[1] - (incoming[1] / incomingLength) * cornerRadius,
    ];
    const exit = [
      current[0] + (outgoing[0] / outgoingLength) * cornerRadius,
      current[1] + (outgoing[1] / outgoingLength) * cornerRadius,
    ];

    d += ` L ${fmt(entry[0])} ${fmt(entry[1])}`;
    d += ` Q ${fmt(current[0])} ${fmt(current[1])} ${fmt(exit[0])} ${fmt(exit[1])}`;
  }

  if (points.length > 1) {
    const last = points.at(-1);
    d += ` L ${fmt(last[0])} ${fmt(last[1])}`;
  }
  return d;
}
