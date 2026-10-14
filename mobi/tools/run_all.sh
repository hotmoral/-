#!/usr/bin/env bash
set -uo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HARNESS="$ROOT/mobi/harness"
OUTPUT="$ROOT/mobi/output/overlay-probe"

cd "$HARNESS"

set +e
bash ../tools/run_overlay_probe.sh
probe_rc=$?
bash ../tools/verify_rotation.sh
rotation_rc=$?
set -e

mkdir -p "$ROOT/mobi/output"
rm -rf "$OUTPUT"
if [ -d "$HARNESS/evidence/overlay-probe" ]; then
  cp -a "$HARNESS/evidence/overlay-probe" "$OUTPUT"
fi

{
  echo "probe_rc=$probe_rc"
  echo "rotation_rc=$rotation_rc"
} >> "$OUTPUT/execution_result.txt" 2>/dev/null || true

if [ "$probe_rc" -ne 0 ] || [ "$rotation_rc" -ne 0 ]; then
  exit 1
fi
