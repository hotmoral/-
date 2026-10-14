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
  return 1
}

capture_rotation_state() {
  local name="$1"
  adb shell dumpsys window displays > "$OUT/${name}_display.txt" 2>&1 || true
  adb shell dumpsys window > "$OUT/${name}_window.txt" 2>&1 || true
}

rotation_matches() {
  local expected="$1" name="$2"
  if [[ "$expected" == "90" ]]; then
    grep -Eq 'mCurrentRotation=ROTATION_90|mRotation=1([^0-9]|$)|mDisplayRotation=ROTATION_90' \
      "$OUT/${name}_display.txt" "$OUT/${name}_window.txt"
  else
    grep -Eq 'mCurrentRotation=ROTATION_0|mRotation=0([^0-9]|$)|mDisplayRotation=ROTATION_0' \
      "$OUT/${name}_display.txt" "$OUT/${name}_window.txt"
  fi
}

wait_for_rotation() {
  local expected="$1" stem="$2" attempt
  for attempt in $(seq 1 10); do
    capture_rotation_state "${stem}_${attempt}"
    if rotation_matches "$expected" "${stem}_${attempt}"; then
      cp "$OUT/${stem}_${attempt}_display.txt" "$OUT/${stem}_display.txt"
      cp "$OUT/${stem}_${attempt}_window.txt" "$OUT/${stem}_window.txt"
      return 0
    fi
    sleep 1
  done
  return 1
}

log "Verified rotation test: actual display state, not settings-write success, is the gate"
adb shell wm help > "$OUT/wm_help.txt" 2>&1 || true

# The main probe intentionally force-stops the overlay at the end. Restart it
# from a visible activity path, then restore the different-UID host.
adb shell am start -W -n "$PROBE/.MainActivity" > "$OUT/rotation_restart_overlay_activity.txt"
sleep 3
adb shell am start -W -n "$HOST/.MainActivity" > "$OUT/rotation_restart_host_activity.txt"
sleep 2

rotation_failures=0

adb shell wm user-rotation lock 1
if wait_for_rotation 90 rotation_90; then
  log "PASS: display actually reached ROTATION_90"
else
  log "FAIL: requested rotation did not produce verified ROTATION_90"
  rotation_failures=$((rotation_failures + 1))
fi

adb shell dumpsys window windows > "$OUT/windows_at_verified_rotation.txt" || true
adb exec-out screencap -p > "$OUT/07_verified_rotation.png" || true
if grep -q "OverlayProbeWindow" "$OUT/windows_at_verified_rotation.txt"; then
  log "PASS: overlay remains attached during rotation check"
else
  log "FAIL: overlay missing during rotation check"
  rotation_failures=$((rotation_failures + 1))
fi

adb shell wm user-rotation lock 0
if wait_for_rotation 0 rotation_restore; then
  log "PASS: display restored to ROTATION_0"
else
  log "FAIL: display did not restore to ROTATION_0"
  rotation_failures=$((rotation_failures + 1))
fi

adb shell am force-stop "$PROBE"
log "Rotation failure count=$rotation_failures"
if (( rotation_failures > 0 )); then
  exit 1
fi
log "Verified rotation check completed successfully"
