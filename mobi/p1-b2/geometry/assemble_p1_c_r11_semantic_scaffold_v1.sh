#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PART_DIR="$HERE/r11_stage0_parts"
TARGET="$HERE/p1_c_r11_semantic_scaffold_v1.py"
EXPECTED_SHA256='af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87'
EXPECTED_BYTES='37871'
mapfile -t parts < <(find "$PART_DIR" -maxdepth 1 -type f -name 'part*.txt' -print | LC_ALL=C sort)
if [ "${#parts[@]}" -ne 7 ]; then
  echo "expected 7 implementation parts, got ${#parts[@]}" >&2
  exit 2
fi
cat "${parts[@]}" > "$TARGET"
test "$(wc -c < "$TARGET" | tr -d ' ')" = "$EXPECTED_BYTES"
echo "$EXPECTED_SHA256  $TARGET" | sha256sum -c -
