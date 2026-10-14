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

dump_ui() {
  adb shell uiautomator dump /sdcard/p0-ui.xml >/dev/null
  adb exec-out cat /sdcard/p0-ui.xml > /tmp/p0-ui.xml
}

tap_text() {
  local needle="$1"
  dump_ui
  local xy
  xy=$(python3 - "$needle" <<'PY'
import re, sys, xml.etree.ElementTree as ET
needle=sys.argv[1]
root=ET.parse('/tmp/p0-ui.xml').getroot()
for node in root.iter('node'):
    text=node.attrib.get('text','')
    if needle in text:
        m=re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', node.attrib.get('bounds',''))
        if m:
            x1,y1,x2,y2=map(int,m.groups())
            print((x1+x2)//2, (y1+y2)//2)
            sys.exit(0)
print('', end='')
sys.exit(2)
PY
) || {
    cp /tmp/p0-ui.xml "$OUT/ui_missing_${needle// /_}.xml" || true
    log "FAIL: UI text not found: $needle"
    exit 20
  }
  read -r x y <<<"$xy"
  adb shell input tap "$x" "$y"
}

read_prefs() {
  adb shell run-as "$PKG" cat shared_prefs/p0_qa_state.xml 2>/dev/null || true
}

wait_pref_event() {
  local needle="$1"
  local attempts="${2:-40}"
  local i
  for ((i=1; i<=attempts; i++)); do
    if read_prefs | grep -q "$needle"; then
      return 0
    fi
    sleep 0.25
  done
  return 1
}

log "Installing APK"
adb install -r "$APK" > "$OUT/install.txt"
adb shell appops set "$PKG" SYSTEM_ALERT_WINDOW allow
adb shell pm grant "$PKG" android.permission.POST_NOTIFICATIONS >/dev/null 2>&1 || true
adb shell am force-stop "$PKG"

log "Launching control Activity"
adb shell am start -W -n "$PKG/.MainActivity" > "$OUT/activity_start.txt"
sleep 2

tap_text "Start Presence"
sleep 2
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
adb shell am start -W -n "$PKG/.MainActivity" >/dev/null
sleep 1
tap_text "Move A"
sleep 2
read_prefs > "$OUT/03_after_move_prefs.xml"
adb shell dumpsys window windows > "$OUT/03_after_move_window.txt"
adb exec-out screencap -p > "$OUT/03_after_move.png"
if ! grep -q 'errorPx=0' "$OUT/03_after_move_prefs.xml"; then
  log "FAIL: deterministic move did not record zero final error"
  exit 24
fi
log "PASS: A to B movement completed with errorPx=0"

log "Testing rotation survival"
ACCEL=$(adb shell settings get system accelerometer_rotation | tr -d '\r')
USERROT=$(adb shell settings get system user_rotation | tr -d '\r')
adb shell settings put system accelerometer_rotation 0
adb shell settings put system user_rotation 1
sleep 3
read_prefs > "$OUT/04_rotation90_prefs.xml"
adb shell dumpsys window windows > "$OUT/04_rotation90_window.txt"
adb exec-out screencap -p > "$OUT/04_rotation90.png"
if ! grep -q 'name="rotation" value="1"' "$OUT/04_rotation90_prefs.xml"; then
  log "FAIL: service QA state did not observe ROTATION_90"
  adb shell settings put system accelerometer_rotation "$ACCEL"
  adb shell settings put system user_rotation "$USERROT"
  exit 25
fi
if ! grep -q 'CatPresenceP0Window' "$OUT/04_rotation90_window.txt"; then
  log "FAIL: overlay missing after rotation"
  adb shell settings put system accelerometer_rotation "$ACCEL"
  adb shell settings put system user_rotation "$USERROT"
  exit 26
fi
adb shell settings put system user_rotation 0
sleep 2
adb shell settings put system accelerometer_rotation "$ACCEL"
adb shell settings put system user_rotation "$USERROT"
log "PASS: overlay survives controlled rotation"

log "Testing screen off/on process-alive lifecycle"
adb shell input keyevent 26
if ! wait_pref_event 'screen_off' 40; then
  read_prefs > "$OUT/05_screen_cycle_prefs.xml"
  log "FAIL: screen_off event was not recorded"
  exit 27
fi
adb shell input keyevent 224
adb shell input keyevent 82 || true
if ! wait_pref_event 'screen_on' 60; then
  read_prefs > "$OUT/05_screen_cycle_prefs.xml"
  log "FAIL: screen_on event was not recorded after explicit wake"
  exit 27
fi
read_prefs > "$OUT/05_screen_cycle_prefs.xml"
log "PASS: screen off/on events recorded while service alive"

log "Testing explicit stop/removal"
adb shell am start -W -n "$PKG/.MainActivity" >/dev/null
sleep 1
tap_text "Stop Presence"
sleep 2
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
