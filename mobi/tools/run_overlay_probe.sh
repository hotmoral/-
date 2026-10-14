#!/usr/bin/env bash
set -euo pipefail

PROBE=com.example.overlayprobe
HOST=com.example.touchhost
OUT=evidence/overlay-probe
mkdir -p "$OUT"
: > "$OUT/summary.txt"

failures=0

log() {
  echo "[probe] $*" | tee -a "$OUT/summary.txt"
}

mark_fail() {
  log "FAIL: $*"
  failures=$((failures + 1))
}

host_count() {
  local value
  value=$(adb shell run-as "$HOST" cat files/host_count.txt 2>/dev/null | tr -d '\r\n' || true)
  echo "${value:-0}"
}

overlay_count() {
  local value
  value=$(adb shell run-as "$PROBE" cat files/overlay_count.txt 2>/dev/null | tr -d '\r\n' || true)
  echo "${value:-0}"
}

expect_delta() {
  local before="$1" after="$2" expected="$3" label="$4"
  local delta=$((after - before))
  if [[ "$delta" -eq "$expected" ]]; then
    log "PASS: $label delta=$delta"
  else
    mark_fail "$label expected_delta=$expected actual_delta=$delta before=$before after=$after"
  fi
}

command_mode() {
  adb shell am broadcast \
    -a com.example.overlayprobe.COMMAND \
    -n "$PROBE/.ProbeCommandReceiver" \
    --es mode "$1" >/dev/null
  sleep 1
}

read_geometry() {
  local attempt value
  for attempt in $(seq 1 20); do
    value=$(adb shell run-as "$PROBE" cat files/geometry.txt 2>/dev/null | tr -d '\r' || true)
    if [[ "$value" =~ ^[0-9]+\ [0-9]+\ [0-9]+\ [0-9]+$ ]]; then
      echo "$value"
      return 0
    fi
    sleep 1
  done
  return 1
}

capture_windows() {
  local name="$1"
  adb shell dumpsys window windows > "$OUT/$name.txt"
}

capture_focus() {
  local name="$1"
  adb shell dumpsys window > "$OUT/$name.txt" 2>&1 || true
  grep -E 'mCurrentFocus=|mFocusedApp=' "$OUT/$name.txt" > "$OUT/${name}_focus.txt" || true
}

check_overlay_window() {
  local label="$1" file="$2"
  capture_windows "$file"
  if grep -q "OverlayProbeWindow" "$OUT/$file.txt"; then
    log "PASS: overlay present after $label"
  else
    mark_fail "overlay missing after $label"
  fi
}

ensure_host_focus() {
  local label="$1"
  local attempt
  for attempt in $(seq 1 5); do
    capture_focus "host_focus_${label}_${attempt}"
    if grep -q "$HOST" "$OUT/host_focus_${label}_${attempt}_focus.txt"; then
      log "PASS: different-UID host has input focus before $label"
      return 0
    fi

    # A system ANR/error dialog can steal input on a freshly booted emulator.
    # Preserve evidence, dismiss the transient UI, and restore the host before
    # making a touch-dispatch claim.
    adb exec-out screencap -p > "$OUT/host_focus_${label}_${attempt}.png" || true
    adb shell input keyevent KEYCODE_BACK >/dev/null 2>&1 || true
    sleep 1
    adb shell am start -W -n "$HOST/.MainActivity" >> "$OUT/host_focus_relaunch.txt" 2>&1 || true
    sleep 2
  done

  mark_fail "different-UID host never became focused before $label; touch result would be contaminated"
  return 1
}

point_inside_overlay() {
  local x="$1" y="$2"
  (( x >= gx && x < gx + gw && y >= gy && y < gy + gh ))
}

test_host_control_point() {
  local x="$1" y="$2" label="$3"
  ensure_host_focus "$label" || return 0
  local before after
  before=$(host_count)
  adb shell input tap "$x" "$y"
  sleep 1
  after=$(host_count)
  expect_delta "$before" "$after" 1 "$label reaches underlying different-UID host"
}

# Start from a clean log buffer so emulator/system contamination can be separated
# from probe behavior.
adb logcat -c

log "Recording execution identity"
{
  echo "git_commit=$(git rev-parse HEAD 2>/dev/null || echo unknown)"
  echo "java=$(java -version 2>&1 | head -n 1)"
  echo "gradle=$(gradle --version 2>/dev/null | awk '/^Gradle / {print $2; exit}')"
  echo "device_sdk=$(adb shell getprop ro.build.version.sdk | tr -d '\r')"
  echo "device_release=$(adb shell getprop ro.build.version.release | tr -d '\r')"
  echo "device_fingerprint=$(adb shell getprop ro.build.fingerprint | tr -d '\r')"
  echo "device_model=$(adb shell getprop ro.product.model | tr -d '\r')"
} > "$OUT/execution_identity.txt"
sha256sum \
  ../tools/run_overlay_probe.sh \
  ../tools/verify_rotation.sh \
  build.gradle settings.gradle gradle.properties \
  overlayprobe/build.gradle hostprobe/build.gradle \
  overlayprobe/src/main/AndroidManifest.xml hostprobe/src/main/AndroidManifest.xml \
  overlayprobe/src/main/java/com/example/overlayprobe/MainActivity.java \
  overlayprobe/src/main/java/com/example/overlayprobe/OverlayService.java \
  overlayprobe/src/main/java/com/example/overlayprobe/ProbeCommandReceiver.java \
  hostprobe/src/main/java/com/example/touchhost/MainActivity.java \
  > "$OUT/source_sha256.txt"

log "Installing debug APKs"
adb install -r overlayprobe/build/outputs/apk/debug/overlayprobe-debug.apk > "$OUT/install_overlay.txt"
adb install -r hostprobe/build/outputs/apk/debug/hostprobe-debug.apk > "$OUT/install_host.txt"
adb shell pm clear "$PROBE" >/dev/null || true
adb shell pm clear "$HOST" >/dev/null || true
adb shell appops set "$PROBE" SYSTEM_ALERT_WINDOW allow
adb shell pm grant "$PROBE" android.permission.POST_NOTIFICATIONS 2>/dev/null || true

log "Starting overlay from a visible activity"
adb shell am start -W -n "$PROBE/.MainActivity" > "$OUT/start_overlay_activity.txt"
sleep 3
adb shell dumpsys activity services "$PROBE" > "$OUT/services_after_visible_start.txt"
if grep -q "OverlayService" "$OUT/services_after_visible_start.txt"; then
  log "PASS: foreground service exists after visible activity start"
else
  mark_fail "foreground service missing after visible activity start"
fi

capture_windows initial_windows
if grep -q "OverlayProbeWindow" "$OUT/initial_windows.txt"; then
  log "PASS: small application overlay is attached"
else
  mark_fail "small application overlay not found"
fi

geometry=$(read_geometry || true)
if [[ -z "$geometry" ]]; then
  mark_fail "could not read attached overlay geometry"
  gx=140; gy=450; gw=240; gh=240
else
  read -r gx gy gw gh <<< "$geometry"
  log "Observed overlay geometry x=$gx y=$gy w=$gw h=$gh"
fi

adb exec-out screencap -p > "$OUT/01_overlay_before_host.png"

log "Starting different-UID touch host"
adb shell am start -W -n "$HOST/.MainActivity" > "$OUT/start_host_activity.txt"
sleep 2
ensure_host_focus "touch_preflight" || true

# Capture any system ANR/error evidence before touch assertions. A prior legacy
# run was contaminated by a Pixel Launcher ANR dialog, so this is now an
# explicit environment diagnostic rather than being misclassified as overlay
# pass-through failure.
adb logcat -d > "$OUT/logcat_before_touch.txt"
if grep -Eq 'ANR in com\.google\.android\.apps\.nexuslauncher|AppNotRespondingDialog' "$OUT/logcat_before_touch.txt"; then
  log "ENVIRONMENT NOTE: launcher ANR evidence observed; host focus recovery was required before touch assertions"
fi
adb exec-out screencap -p > "$OUT/02_overlay_over_host.png"

size_line=$(adb shell wm size | tr -d '\r' | tail -n 1)
screen_w=$(echo "$size_line" | sed -n 's/.*: \([0-9][0-9]*\)x\([0-9][0-9]*\).*/\1/p')
screen_h=$(echo "$size_line" | sed -n 's/.*: \([0-9][0-9]*\)x\([0-9][0-9]*\).*/\2/p')
screen_w=${screen_w:-1080}
screen_h=${screen_h:-2400}

# Two interior control points, far from status/navigation edges. Both must reach
# the host and neither may overlap the observed small overlay rectangle.
control1_x=$((screen_w * 3 / 4))
control1_y=$((screen_h / 3))
control2_x=$((screen_w * 3 / 4))
control2_y=$((screen_h * 2 / 3))
if point_inside_overlay "$control1_x" "$control1_y"; then
  control1_x=$((screen_w / 2))
fi
if point_inside_overlay "$control2_x" "$control2_y"; then
  control2_x=$((screen_w / 2))
fi

test_host_control_point "$control1_x" "$control1_y" "outside control point A"
test_host_control_point "$control2_x" "$control2_y" "outside control point B"

# Center touch: must remain in the overlay and not reach the host.
ensure_host_focus "inside_overlay" || true
center_x=$((gx + gw / 2))
center_y=$((gy + gh / 2))
h_before=$(host_count)
p_before=$(overlay_count)
adb shell input tap "$center_x" "$center_y"
sleep 1
h_after=$(host_count)
p_after=$(overlay_count)
expect_delta "$h_before" "$h_after" 0 "center touch inside overlay does not reach host"
expect_delta "$p_before" "$p_after" 1 "center touch is received by overlay"

# Transparent corner inside the rectangular overlay bounds. The view draws only
# a central circle, so this proves that visual transparency is not equivalent to
# an input hole.
ensure_host_focus "transparent_corner" || true
corner_x=$((gx + 10))
corner_y=$((gy + 10))
h_before=$(host_count)
p_before=$(overlay_count)
adb shell input tap "$corner_x" "$corner_y"
sleep 1
h_after=$(host_count)
p_after=$(overlay_count)
expect_delta "$h_before" "$h_after" 0 "transparent pixel area inside rectangular overlay still occupies input space"
expect_delta "$p_before" "$p_after" 1 "transparent-corner touch is received by overlay window"

# Just outside the right edge: validates that the rectangular input footprint
# ends at the window boundary.
ensure_host_focus "near_edge" || true
edge_x=$((gx + gw + 8))
edge_y=$((gy + gh / 2))
if (( edge_x >= screen_w - 1 )); then
  edge_x=$((gx - 8))
fi
h_before=$(host_count)
adb shell input tap "$edge_x" "$edge_y"
sleep 1
h_after=$(host_count)
expect_delta "$h_before" "$h_after" 1 "near-edge touch just outside overlay reaches host"

log "Starting bounded automatic movement cadence test"
command_mode move
sleep 12
movement=$(adb shell run-as "$PROBE" cat files/movement_result.txt 2>/dev/null | tr -d '\r\n' || true)
echo "$movement" > "$OUT/movement_result.txt"
if [[ "$movement" == "completed frames=300 attached=true" ]]; then
  log "PASS: automatic movement completed 300 updateViewLayout frames while attached"
else
  mark_fail "automatic movement result unexpected: ${movement:-missing}"
fi
check_overlay_window "automatic movement" windows_after_movement
adb exec-out screencap -p > "$OUT/03_after_movement.png"

log "Testing HOME / Recents / screen-cycle coexistence"
adb shell input keyevent KEYCODE_HOME
sleep 2
check_overlay_window "HOME" windows_after_home
capture_focus focus_after_home
adb exec-out screencap -p > "$OUT/04_after_home.png"

adb shell input keyevent KEYCODE_APP_SWITCH
sleep 2
check_overlay_window "RECENTS" windows_after_recents
capture_focus focus_after_recents
adb exec-out screencap -p > "$OUT/05_after_recents.png"

adb shell input keyevent KEYCODE_POWER
sleep 2
adb shell input keyevent KEYCODE_POWER
sleep 2
adb shell wm dismiss-keyguard >/dev/null 2>&1 || true
sleep 2
check_overlay_window "screen off/on" windows_after_screen_cycle
capture_focus focus_after_screen_cycle
adb exec-out screencap -p > "$OUT/06_after_screen_cycle.png"

log "Capturing foreground-service notification evidence"
adb shell dumpsys notification --noredact > "$OUT/notifications.txt" || true
adb shell dumpsys activity services "$PROBE" > "$OUT/services_final.txt" || true
if grep -q "$PROBE" "$OUT/notifications.txt"; then
  log "PASS: notification service record contains probe package"
else
  mark_fail "probe package not found in notification dump"
fi

log "Testing explicit overlay remove/create without stopping service"
command_mode remove
capture_windows windows_after_remove
if grep -q "OverlayProbeWindow" "$OUT/windows_after_remove.txt"; then
  mark_fail "overlay window still present after explicit remove command"
else
  log "PASS: explicit remove detaches overlay"
fi
command_mode small
sleep 2
check_overlay_window "explicit re-create" windows_after_recreate

adb logcat -d > "$OUT/logcat_final.txt"
adb shell dumpsys window displays > "$OUT/window_displays.txt" || true

log "Force-stopping probe only as a stop/removal observation; this is not treated as normal lifecycle restart evidence"
adb shell am force-stop "$PROBE"
sleep 2
capture_windows windows_after_force_stop
if grep -q "OverlayProbeWindow" "$OUT/windows_after_force_stop.txt"; then
  mark_fail "overlay remains after force-stop"
else
  log "PASS: force-stop removes overlay"
fi

log "Critical failure count=$failures"
if (( failures > 0 )); then
  exit 1
fi
log "Residual overlay probe completed successfully"
