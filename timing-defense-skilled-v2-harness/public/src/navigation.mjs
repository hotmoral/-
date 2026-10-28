export const STAGE_PAGE_SIZE = 30;

export function continuePosition(progress, total) {
  if (!Number.isInteger(total) || total < 1) throw new Error('NAV_TOTAL');
  const highest = Math.max(0, Math.min(Number.isInteger(progress?.highestCleared) ? progress.highestCleared : 0, total));
  return highest >= total ? total : highest + 1;
}

export function stageState(position, progress, total) {
  if (!Number.isInteger(position) || position < 1 || position > total) throw new Error('NAV_POSITION');
  const highest = Math.max(0, Math.min(Number.isInteger(progress?.highestCleared) ? progress.highestCleared : 0, total));
  const current = continuePosition(progress, total);
  if (highest >= total && position === total) return 'completed-current';
  if (position <= highest) return 'completed';
  if (position === current && highest < total) return 'current';
  return 'locked';
}

export function stagePage(position, total, pageSize = STAGE_PAGE_SIZE) {
  if (!Number.isInteger(pageSize) || pageSize < 1) throw new Error('NAV_PAGE_SIZE');
  if (!Number.isInteger(position) || position < 1 || position > total) throw new Error('NAV_POSITION');
  const pageIndex = Math.floor((position - 1) / pageSize);
  const start = pageIndex * pageSize + 1;
  const end = Math.min(total, start + pageSize - 1);
  return { pageIndex, start, end, pageSize };
}

export function pageRows(page, columns = 5) {
  if (!page || !Number.isInteger(page.start) || !Number.isInteger(page.end) || page.end < page.start) throw new Error('NAV_PAGE');
  if (!Number.isInteger(columns) || columns < 1) throw new Error('NAV_COLUMNS');
  const positions = Array.from({ length: page.end - page.start + 1 }, (_, index) => page.start + index);
  const rows = [];
  for (let index = 0; index < positions.length; index += columns) rows.push(positions.slice(index, index + columns));
  return rows;
}

export function completionPercent(progress, total) {
  if (!Number.isInteger(total) || total < 1) throw new Error('NAV_TOTAL');
  const highest = Math.max(0, Math.min(Number.isInteger(progress?.highestCleared) ? progress.highestCleared : 0, total));
  return Math.round((highest / total) * 100);
}
