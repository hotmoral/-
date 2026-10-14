#!/usr/bin/env bash
set -euo pipefail

PROBE=com.example.overlayprobe
HOST=com.example.touchhost
OUT=evidence/overlay-probe
mkdir -p "$OUT"

log() {
  echo "[rotation] $*" | tee -a "$OUT/summary.txt"
}

fail() {
  log "FAIL: $*"
  exit 1
}

log "Supplemental rotation verification: supersedes the earlier settings-based orientation assertion"
adb shell wm help > "$OUT/wm_help.txt" 2>&1 || true

# The main probe intentionally force-stops the overlay at the end. Restart it from a visible UI path.
adb shell am start -W -n "$PROBE/.MainActivity" > "$OUT/rotation_restart_overlay_activity.txt"
sleep 3
adb shell am start -W -n "$HOST/.MainActivity" > "$OUT/rotation_restart_host_activity.txt"
sleep 2

adb shell wm user-rotation lock 1
sleep 4
adb shell dumpsys window displays > "$OUT/display_after_verified_rotation.txt"
adb shell dumpsys window windows > "$OUT/windows_after_verified_rotation.txt"
adb exec-out screencap -p > "$OUT/08_verified_rotation.png"

if grep -Eq 'mCurrentRotation=ROTATION_90|mRotation=1([^0-9]|$)|mDisplayRotation=ROTATION_90' "$OUT/display_after_verified_rotation.txt" "$OUT/windows_after_verified_rotation.txt"; then
  log "PASS: display actually reached ROTATION_90"
else
  fail "requested rotation did not produce verified ROTATION_90"
fi

if grep -q "OverlayProbeWindow" "$OUT/windows_after_verified_rotation.txt"; then
  log "PASS: overlay remains attached during verified ROTATION_90"
else
  fail "overlay missing during verified ROTATION_90"
fi

adb shell wm user-rotation lock 0
sleep 4
adb shell dumpsys window displays > "$OUT/display_after_rotation_restore.txt"
if grep -Eq 'mCurrentRotation=ROTATION_0|mRotation=0([^0-9]|$)|mDisplayRotation=ROTATION_0' "$OUT/display_after_rotation_restore.txt"; then
  log "PASS: display restored to ROTATION_0"
else
  fail "display did not restore to ROTATION_0"
fi

adb shell am force-stop "$PROBE"
log "Supplemental verified rotation check completed"
