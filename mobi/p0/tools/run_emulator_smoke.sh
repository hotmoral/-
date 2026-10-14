#!/usr/bin/env bash
set -euo pipefail

PKG=org.example.catpresence
APK=mobi/p0/harness/app/build/outputs/apk/debug/app-debug.apk
OUT=mobi/output/p0-presence-runtime
mkdir -p "$OUT"
rm -f "$OUT"/*

log() {
  echo "[p0-smoke] $*" | tee -a "$OUT/summary.txt"
}

read_prefs() {
  adb shell run-as "$PKG" cat shared_prefs/p0_qa_state.xml 2>/dev/null || true
}

wait_pref_event() {
  local needle="$1"
  local attempts="${2:-60}"
  local i
  for ((i=1; i<=attempts; i++)); do
    if read_prefs | grep -q "$needle"; then
      return 0
    fi
    sleep 0.25
  done
  return 1
}

qa_command() {
  local command="$1"
  adb shell am start -W -n "$PKG/.MainActivity" --es p0_qa_command "$command" > "$OUT/command_${command}.txt"
}

log "Installing APK"
adb install -r "$APK" > "$OUT/install.txt"
adb shell appops set "$PKG" SYSTEM_ALERT_WINDOW allow
adb shell pm grant "$PKG" android.permission.POST_NOTIFICATIONS >/dev/null 2>&1 || true
adb shell am force-stop "$PKG"

log "Starting bounded presence through deterministic QA command"
qa_command start
if ! wait_pref_event 'name="overlayAttached" value="true"' 80; then
  read_prefs > "$OUT/01_after_start_prefs.xml"
  adb shell dumpsys window windows > "$OUT/01_after_start_window.txt"
  adb shell dumpsys activity services "$PKG" > "$OUT/01_after_start_services.txt"
  log "FAIL: overlay state did not become attached"
  exit 21
fi
adb shell dumpsys window windows > "$OUT/01_after_start_window.txt"
adb shell dumpsys activity services "$PKG" > "$OUT/01_after_start_services.txt"
read_prefs > "$OUT/01_after_start_prefs.xml"
if ! grep -q 'CatPresenceP0Window' "$OUT/01_after_start_window.txt"; then
  log "FAIL: overlay Window not present after start"
  exit 21
fi
if ! grep -q 'PresenceService' "$OUT/01_after_start_services.txt"; then
  log "FAIL: PresenceService not active after start"
  exit 22
fi
log "PASS: bounded overlay Window and service active"

log "Switching to Settings while overlay remains"
adb shell am start -W -a android.settings.SETTINGS > "$OUT/settings_start.txt"
sleep 2
adb shell dumpsys window windows > "$OUT/02_settings_window.txt"
adb exec-out screencap -p > "$OUT/02_settings_overlay.png"
if ! grep -q 'CatPresenceP0Window' "$OUT/02_settings_window.txt"; then
  log "FAIL: overlay missing after foreground app switch"
  exit 23
fi
log "PASS: overlay remains across ordinary app switch"

log "Running deterministic A to B movement"
qa_command move_a_to_b
if ! wait_pref_event 'errorPx=0' 80; then
  read_prefs > "$OUT/03_after_move_prefs.xml"
  log "FAIL: deterministic move did not record zero final error"
  exit 24
fi
read_prefs > "$OUT/03_after_move_prefs.xml"
adb shell dumpsys window windows > "$OUT/03_after_move_window.txt"
adb exec-out screencap -p > "$OUT/03_after_move.png"
log "PASS: A to B movement completed with errorPx=0"

log "Testing rotation survival"
ACCEL=$(adb shell settings get system accelerometer_rotation | tr -d '\r')
USERROT=$(adb shell settings get system user_rotation | tr -d '\r')
adb shell settings put system accelerometer_rotation 0
adb shell settings put system user_rotation 1
if ! wait_pref_event 'name="rotation" value="1"' 80; then
  read_prefs > "$OUT/04_rotation90_prefs.xml"
  adb shell settings put system accelerometer_rotation "$ACCEL"
  adb shell settings put system user_rotation "$USERROT"
  log "FAIL: service QA state did not observe ROTATION_90"
  exit 25
fi
read_prefs > "$OUT/04_rotation90_prefs.xml"
adb shell dumpsys window windows > "$OUT/04_rotation90_window.txt"
adb exec-out screencap -p > "$OUT/04_rotation90.png"
if ! grep -q 'CatPresenceP0Window' "$OUT/04_rotation90_window.txt"; then
  adb shell settings put system accelerometer_rotation "$ACCEL"
  adb shell settings put system user_rotation "$USERROT"
  log "FAIL: overlay missing after rotation"
  exit 26
fi
adb shell settings put system user_rotation 0
wait_pref_event 'name="rotation" value="0"' 80 || true
adb shell settings put system accelerometer_rotation "$ACCEL"
adb shell settings put system user_rotation "$USERROT"
log "PASS: overlay survives controlled rotation"

log "Testing screen off/on process-alive lifecycle"
adb shell input keyevent KEYCODE_SLEEP
if ! wait_pref_event 'screen_off' 80; then
  read_prefs > "$OUT/05_screen_cycle_prefs.xml"
  adb shell dumpsys power > "$OUT/05_power_after_sleep.txt" || true
  log "FAIL: screen_off event was not recorded"
  exit 27
fi
adb shell dumpsys power > "$OUT/05_power_after_sleep.txt" || true
adb shell input keyevent KEYCODE_WAKEUP
adb shell wm dismiss-keyguard >/dev/null 2>&1 || true
if ! wait_pref_event 'screen_on' 120; then
  read_prefs > "$OUT/05_screen_cycle_prefs.xml"
  adb shell dumpsys power > "$OUT/05_power_after_wake.txt" || true
  log "FAIL: screen_on event was not recorded after explicit wake"
  exit 27
fi
adb shell dumpsys power > "$OUT/05_power_after_wake.txt" || true
read_prefs > "$OUT/05_screen_cycle_prefs.xml"
log "PASS: screen off/on events recorded while service alive"

log "Testing explicit stop/removal"
qa_command stop
if ! wait_pref_event 'name="serviceActive" value="false"' 80; then
  read_prefs > "$OUT/06_after_stop_prefs.xml"
  log "FAIL: service state did not stop after explicit command"
  exit 28
fi
sleep 1
adb shell dumpsys window windows > "$OUT/06_after_stop_window.txt"
adb shell dumpsys activity services "$PKG" > "$OUT/06_after_stop_services.txt"
read_prefs > "$OUT/06_after_stop_prefs.xml"
if grep -q 'CatPresenceP0Window' "$OUT/06_after_stop_window.txt"; then
  log "FAIL: overlay still present after explicit stop"
  exit 28
fi
if grep -q 'org.example.catpresence/.PresenceService' "$OUT/06_after_stop_services.txt"; then
  log "FAIL: service still active after explicit stop"
  exit 29
fi
log "PASS: explicit stop removes overlay and service"

adb shell getprop > "$OUT/device_getprop.txt"
adb shell dumpsys package "$PKG" > "$OUT/package.txt"
sha256sum "$APK" > "$OUT/apk_sha256.txt"
log "P0 generic emulator smoke PASS"
