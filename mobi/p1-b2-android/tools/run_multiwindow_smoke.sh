#!/usr/bin/env bash
set -euo pipefail

PKG=org.example.catpresence
APK=mobi/p1-b2-android/harness/app/build/outputs/apk/debug/app-debug.apk
OUT=mobi/output/p1-b2-multiwindow
mkdir -p "$OUT"
rm -f "$OUT"/*

log() {
  echo "[p1-b2-multiwindow] $*" | tee -a "$OUT/summary.txt"
}

read_prefs() {
  adb shell run-as "$PKG" cat shared_prefs/p0_qa_state.xml 2>/dev/null || true
}

wait_pref() {
  local needle="$1"
  local attempts="${2:-80}"
  local i
  for ((i=1; i<=attempts; i++)); do
    if read_prefs | grep -q "$needle"; then
      return 0
    fi
    sleep 0.25
  done
  return 1
}

read_int() {
  local key="$1"
  read_prefs | grep "name=\"$key\"" | tail -1 | sed -E 's/.*value="(-?[0-9]+)".*/\1/'
}

qa() {
  local command="$1"
  adb shell am start -W -n "$PKG/.MainActivity" --es p1_qa_command "$command" > "$OUT/command_${command}.txt"
}

assert_int_eq() {
  local key="$1"
  local expected="$2"
  local actual
  actual="$(read_int "$key")"
  if [[ "$actual" != "$expected" ]]; then
    read_prefs > "$OUT/assert_${key}_prefs.xml"
    log "FAIL: $key expected=$expected actual=$actual"
    exit 30
  fi
}

center_tap_part() {
  local id="$1"
  local x y w h cx cy
  x="$(read_int "part_${id}_x")"
  y="$(read_int "part_${id}_y")"
  w="$(read_int "part_${id}_w")"
  h="$(read_int "part_${id}_h")"
  cx=$((x + w / 2))
  cy=$((y + h / 2))
  adb shell input tap "$cx" "$cy"
  sleep 0.25
}

log "Install P1-B2.2 multi-window APK"
adb install -r "$APK" > "$OUT/install.txt"
adb shell appops set "$PKG" SYSTEM_ALERT_WINDOW allow
adb shell pm grant "$PKG" android.permission.POST_NOTIFICATIONS >/dev/null 2>&1 || true
adb shell am force-stop "$PKG"

log "F0: one full-cat rectangle control"
qa start_f0
wait_pref '<string name="mode">F0_SINGLE_ALL</string>' 100
wait_pref 'name="windowCount" value="1"' 100
adb shell dumpsys window windows > "$OUT/01_f0_windows.txt"
read_prefs > "$OUT/01_f0_prefs.xml"
if ! grep -q 'MobiP1F0_ALL' "$OUT/01_f0_windows.txt"; then
  log "FAIL: F0 Window title missing"
  exit 21
fi
qa reset_counts
GAP_X="$(read_int gapTestX)"
GAP_Y="$(read_int gapTestY)"
adb shell input tap "$GAP_X" "$GAP_Y"
sleep 0.5
assert_int_eq overlayTouchCount 1
assert_int_eq hostTouchCount 0
log "PASS: F0 transparent internal gap remains blocked by full rectangle"

log "F1: CORE + TAIL comparator"
qa set_f1
wait_pref '<string name="mode">F1_CORE_TAIL</string>' 80
wait_pref 'name="windowCount" value="2"' 80
adb shell dumpsys window windows > "$OUT/02_f1_windows.txt"
read_prefs > "$OUT/02_f1_prefs.xml"
if ! grep -q 'MobiP1F1_CORE' "$OUT/02_f1_windows.txt" || ! grep -q 'MobiP1F1_TAIL' "$OUT/02_f1_windows.txt"; then
  log "FAIL: F1 expected two Window titles"
  exit 22
fi
qa reset_counts
GAP_X="$(read_int gapTestX)"
GAP_Y="$(read_int gapTestY)"
adb shell input tap "$GAP_X" "$GAP_Y"
sleep 0.5
assert_int_eq overlayTouchCount 1
assert_int_eq hostTouchCount 0
log "PASS: F1 still blocks between-leg internal CORE slack as predicted"

log "F2: CORE + FORE + HIND + TAIL"
qa set_f2
wait_pref '<string name="mode">F2_CORE_FORE_HIND_TAIL</string>' 80
wait_pref 'name="windowCount" value="4"' 80
adb shell dumpsys window windows > "$OUT/03_f2_windows.txt"
read_prefs > "$OUT/03_f2_prefs.xml"
for title in MobiP1F2_CORE MobiP1F2_FORE MobiP1F2_HIND MobiP1F2_TAIL; do
  if ! grep -q "$title" "$OUT/03_f2_windows.txt"; then
    log "FAIL: F2 missing $title"
    exit 23
  fi
done
qa reset_counts
GAP_X="$(read_int gapTestX)"
GAP_Y="$(read_int gapTestY)"
adb shell input tap "$GAP_X" "$GAP_Y"
if ! wait_pref 'name="hostTouchCount" value="1"' 40; then
  read_prefs > "$OUT/03_f2_gap_failed_prefs.xml"
  log "FAIL: F2 geometric gap did not reach host"
  exit 24
fi
assert_int_eq overlayTouchCount 0
log "PASS: F2 between-part gap passes foreground touch"

log "F2: each actual component rectangle remains directly touchable"
for id in CORE FORE HIND TAIL; do
  center_tap_part "$id"
done
sleep 0.5
assert_int_eq overlayTouchCount 4
assert_int_eq hostTouchCount 1
for id in CORE FORE HIND TAIL; do
  assert_int_eq "touch_${id}" 1
done
read_prefs > "$OUT/04_f2_component_touches.xml"
log "PASS: four F2 component rectangles consume their own touches; host count unchanged"

log "F2: 300 coordinated position updates"
qa move_stress
wait_pref 'name="stressUpdateCount" value="300"' 120
assert_int_eq stressExceptions 0
assert_int_eq maxRelativeErrorPx 0
adb shell dumpsys window windows > "$OUT/05_after_move_windows.txt"
adb exec-out screencap -p > "$OUT/05_after_move.png"
for title in MobiP1F2_CORE MobiP1F2_FORE MobiP1F2_HIND MobiP1F2_TAIL; do
  grep -q "$title" "$OUT/05_after_move_windows.txt"
done
log "PASS: 300 coordinated multi-Window updates completed with no recorded exception/relative error"

log "F2: controlled rotation survival"
ACCEL="$(adb shell settings get system accelerometer_rotation | tr -d '\r')"
USERROT="$(adb shell settings get system user_rotation | tr -d '\r')"
adb shell settings put system accelerometer_rotation 0
adb shell settings put system user_rotation 1
if ! wait_pref 'name="rotation" value="1"' 100; then
  adb shell settings put system accelerometer_rotation "$ACCEL"
  adb shell settings put system user_rotation "$USERROT"
  read_prefs > "$OUT/06_rotation_failed_prefs.xml"
  log "FAIL: F2 did not record ROTATION_90"
  exit 25
fi
adb shell dumpsys window windows > "$OUT/06_rotation_windows.txt"
read_prefs > "$OUT/06_rotation_prefs.xml"
for title in MobiP1F2_CORE MobiP1F2_FORE MobiP1F2_HIND MobiP1F2_TAIL; do
  grep -q "$title" "$OUT/06_rotation_windows.txt"
done
adb shell settings put system user_rotation 0
wait_pref 'name="rotation" value="0"' 100 || true
adb shell settings put system accelerometer_rotation "$ACCEL"
adb shell settings put system user_rotation "$USERROT"
log "PASS: all four F2 Windows survive controlled rotation"

log "F2: screen off/on lifecycle"
adb shell input keyevent KEYCODE_SLEEP
wait_pref 'screen_off' 100
adb shell input keyevent KEYCODE_WAKEUP
adb shell wm dismiss-keyguard >/dev/null 2>&1 || true
wait_pref 'screen_on' 120
adb shell dumpsys window windows > "$OUT/07_screen_cycle_windows.txt"
read_prefs > "$OUT/07_screen_cycle_prefs.xml"
for title in MobiP1F2_CORE MobiP1F2_FORE MobiP1F2_HIND MobiP1F2_TAIL; do
  grep -q "$title" "$OUT/07_screen_cycle_windows.txt"
done
log "PASS: all four F2 Windows remain after screen off/on while service is alive"

log "Explicit stop must remove every child Window"
qa stop
wait_pref 'name="serviceActive" value="false"' 100
sleep 1
adb shell dumpsys window windows > "$OUT/08_after_stop_windows.txt"
adb shell dumpsys activity services "$PKG" > "$OUT/08_after_stop_services.txt"
read_prefs > "$OUT/08_after_stop_prefs.xml"
if grep -q 'MobiP1F' "$OUT/08_after_stop_windows.txt"; then
  log "FAIL: one or more P1 child Windows remain after stop"
  exit 26
fi
if grep -q 'org.example.catpresence/.PresenceService' "$OUT/08_after_stop_services.txt"; then
  log "FAIL: PresenceService remains after explicit stop"
  exit 27
fi
log "PASS: explicit stop removes all child Windows and service"

adb shell getprop > "$OUT/device_getprop.txt"
adb shell dumpsys package "$PKG" > "$OUT/package.txt"
sha256sum "$APK" > "$OUT/apk_sha256.txt"
log "P1-B2.2 multi-window generic emulator smoke PASS"
