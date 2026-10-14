#!/usr/bin/env bash
set -euo pipefail

PKG=org.example.mobifootprint
APK=mobi/p1-b2/android-footprint/app/build/outputs/apk/debug/app-debug.apk
OUT=mobi/output/p1-b22-android-footprint
mkdir -p "$OUT"
rm -f "$OUT"/*

log() {
  echo "[p1-b22] $*" | tee -a "$OUT/summary.txt"
}

read_prefs() {
  adb shell run-as "$PKG" cat shared_prefs/p1_b22_qa_state.xml 2>/dev/null || true
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

qa() {
  local command="$1"
  adb shell am start -W -n "$PKG/.MainActivity" --es p1_b22_qa_command "$command" > "$OUT/cmd_${command}.txt"
}

pref_string() {
  local name="$1"
  read_prefs | sed -n "s#.*<string name=\"${name}\">\(.*\)</string>.*#\1#p" | tail -1
}

pref_int() {
  local name="$1"
  read_prefs | sed -n "s#.*<int name=\"${name}\" value=\"\([0-9-]*\)\".*#\1#p" | tail -1
}

# Return actual global screen frame as left,top,right,bottom.
# LayoutParams x/y are relative to the overlay parent frame on API 35, so
# touch evidence must use WindowManager's realized frame rather than requested x/y.
frame_for() {
  local part="$1"
  local dump block frame
  dump="$(adb shell dumpsys window windows)"
  block="$(printf '%s\n' "$dump" | sed -n "/Window #[0-9][0-9]* Window{.*MobiP1B22-${part}}:/,/Frames:/p" | head -40)"
  frame="$(printf '%s\n' "$block" | sed -n 's/.* frame=\[\([-0-9][0-9-]*\),\([-0-9][0-9-]*\)\]\[\([-0-9][0-9-]*\),\([-0-9][0-9-]*\)\].*/\1,\2,\3,\4/p' | tail -1)"
  if [ -z "$frame" ]; then
    echo "Missing realized frame for $part" >&2
    return 1
  fi
  printf '%s\n' "$frame"
}

tap_part() {
  local part="$1"
  local frame l t r b cx cy
  frame="$(frame_for "$part")"
  IFS=',' read -r l t r b <<< "$frame"
  cx=$(((l + r) / 2))
  cy=$(((t + b) / 2))
  adb shell input tap "$cx" "$cy"
  if ! wait_pref "<string name=\"lastHit\">${part}</string>" 40; then
    read_prefs > "$OUT/tap_${part}_failed.xml"
    adb shell dumpsys window windows > "$OUT/tap_${part}_failed_windows.txt"
    log "FAIL: direct realized-frame tap did not reach child $part"
    return 1
  fi
}

window_count() {
  adb shell dumpsys window windows | grep -Ec '^[[:space:]]+Window #[0-9]+ Window\{.*MobiP1B22-' || true
}

assert_window_count() {
  local expected="$1"
  local actual
  actual="$(window_count)"
  if [ "$actual" -ne "$expected" ]; then
    adb shell dumpsys window windows > "$OUT/window_count_${expected}_failed.txt"
    read_prefs > "$OUT/prefs_count_${expected}_failed.xml"
    log "FAIL: expected $expected overlay child Windows, got $actual"
    exit 30
  fi
}

log "Install APK and grant bounded overlay permission"
adb install -r "$APK" > "$OUT/install.txt"
adb shell appops set "$PKG" SYSTEM_ALERT_WINDOW allow
adb shell pm grant "$PKG" android.permission.POST_NOTIFICATIONS >/dev/null 2>&1 || true
adb shell am force-stop "$PKG"
qa reset

log "F0 control: exactly one Window"
qa f0
wait_pref '<string name="variant">F0</string>' 80
wait_pref 'name="childCount" value="1"' 80
assert_window_count 1
read_prefs > "$OUT/01_f0.xml"
adb exec-out screencap -p > "$OUT/01_f0.png"
tap_part ALL
log "PASS F0: one child Window and child hit consumption"

log "F1 comparator: exactly two Windows with no stale F0 child"
qa f1
wait_pref '<string name="variant">F1</string>' 80
wait_pref 'name="childCount" value="2"' 80
assert_window_count 2
read_prefs > "$OUT/02_f1.xml"
adb shell dumpsys window windows > "$OUT/02_f1_windows.txt"
if grep -q 'MobiP1B22-ALL' "$OUT/02_f1_windows.txt"; then
  log "FAIL: stale F0 ALL Window after F1 switch"
  exit 31
fi
tap_part CORE
tap_part TAIL
log "PASS F1: two child Windows, no stale F0, both consume direct hits"

log "F2 comparator: exactly four Windows"
qa f2
wait_pref '<string name="variant">F2</string>' 80
wait_pref 'name="childCount" value="4"' 80
assert_window_count 4
read_prefs > "$OUT/03_f2_before_hits.xml"
adb shell dumpsys window windows > "$OUT/03_f2_windows.txt"
adb exec-out screencap -p > "$OUT/03_f2.png"
for part in CORE HIND FORE TAIL; do
  tap_part "$part"
done
log "PASS F2: four child Windows and each child consumes its direct hit"

log "F2 real gap must pass through to foreground Activity"
CORE_FRAME="$(frame_for CORE)"
HIND_FRAME="$(frame_for HIND)"
FORE_FRAME="$(frame_for FORE)"
TAIL_FRAME="$(frame_for TAIL)"
IFS=',' read -r cl ct cr cb <<< "$CORE_FRAME"
IFS=',' read -r hl ht hr hb <<< "$HIND_FRAME"
IFS=',' read -r fl ft fr fb <<< "$FORE_FRAME"
IFS=',' read -r tl tt tr tb <<< "$TAIL_FRAME"
gap_x=$(((hr + fl) / 2))
if [ "$tb" -gt "$cb" ]; then lower="$tb"; else lower="$cb"; fi
gap_y=$((lower + 12))
if [ "$gap_x" -le "$hr" ] || [ "$gap_x" -ge "$fl" ] || [ "$gap_y" -ge "$hb" ] || [ "$gap_y" -ge "$fb" ]; then
  log "FAIL: computed realized-frame gap probe is not inside declared gap"
  exit 32
fi
host_before="$(pref_int hostTapCount)"
core_before="$(pref_int coreTapCount)"
fore_before="$(pref_int foreTapCount)"
hind_before="$(pref_int hindTapCount)"
tail_before="$(pref_int tailTapCount)"
adb shell input tap "$gap_x" "$gap_y"
sleep 0.5
host_after="$(pref_int hostTapCount)"
if [ "$host_after" -ne $((host_before + 1)) ]; then
  read_prefs > "$OUT/04_gap_failed.xml"
  adb shell dumpsys window windows > "$OUT/04_gap_failed_windows.txt"
  log "FAIL: declared inter-Window gap did not reach foreground Activity"
  exit 33
fi
for pair in "core $core_before" "fore $fore_before" "hind $hind_before" "tail $tail_before"; do
  set -- $pair
  now="$(pref_int "${1}TapCount")"
  if [ "$now" -ne "$2" ]; then
    log "FAIL: gap tap was consumed by overlay child $1"
    exit 34
  fi
done
log "PASS F2: uncovered gap truthfully passes input to foreground host"

log "Sibling overlap dispatch must be deterministic: TAIL is topmost"
overlap_left=$(( tl > cl ? tl : cl ))
overlap_top=$(( tt > ct ? tt : ct ))
if [ "$tr" -lt "$cr" ]; then overlap_right="$tr"; else overlap_right="$cr"; fi
if [ "$tb" -lt "$cb" ]; then overlap_bottom="$tb"; else overlap_bottom="$cb"; fi
if [ "$overlap_right" -le "$overlap_left" ] || [ "$overlap_bottom" -le "$overlap_top" ]; then
  log "FAIL: CORE/TAIL overlap geometry missing"
  exit 35
fi
overlap_x=$(((overlap_left + overlap_right) / 2))
overlap_y=$(((overlap_top + overlap_bottom) / 2))
for i in 1 2 3; do
  adb shell input tap "$overlap_x" "$overlap_y"
  if ! wait_pref '<string name="lastHit">TAIL</string>' 30; then
    read_prefs > "$OUT/05_overlap_failed_${i}.xml"
    log "FAIL: overlap dispatch was not TAIL-topmost on trial $i"
    exit 36
  fi
done
log "PASS F2: overlap dispatch stable for declared sibling z-order"

log "Synchronized A→B move must preserve every child relative offset"
read_prefs > "$OUT/06_move_before.xml"
qa move_b
wait_pref 'name="moveErrorPx" value="0"' 80
sleep 0.35
read_prefs > "$OUT/06_move_after.xml"
python3 - "$OUT/06_move_before.xml" "$OUT/06_move_after.xml" <<'PY'
import sys, xml.etree.ElementTree as ET

def vals(path):
    root=ET.parse(path).getroot()
    data={e.attrib['name']:(e.text or '') for e in root.findall('string')}
    g={}
    for token in data['geometry'].split(';'):
        name, raw=token.split('=',1)
        g[name]=tuple(map(int,raw.split(',')))
    return g
b=vals(sys.argv[1]); a=vals(sys.argv[2])
assert set(b)==set(a)=={'CORE','FORE','HIND','TAIL'}, (b,a)
deltas=set()
for k in sorted(b):
    bx,by,bw,bh=b[k]; ax,ay,aw,ah=a[k]
    assert (bw,bh)==(aw,ah), (k,b[k],a[k])
    deltas.add((ax-bx, ay-by))
assert len(deltas)==1, deltas
assert next(iter(deltas)) != (0,0), deltas
print('relative_geometry_preserved delta=', next(iter(deltas)))
PY
log "PASS F2: all child rectangles moved by one identical translation"

log "Rotation must preserve four-part logical group"
ACCEL=$(adb shell settings get system accelerometer_rotation | tr -d '\r')
USERROT=$(adb shell settings get system user_rotation | tr -d '\r')
adb shell settings put system accelerometer_rotation 0
adb shell settings put system user_rotation 1
if ! wait_pref 'name="rotation" value="1"' 120; then
  read_prefs > "$OUT/07_rotation_failed.xml"
  adb shell settings put system accelerometer_rotation "$ACCEL"
  adb shell settings put system user_rotation "$USERROT"
  log "FAIL: service did not observe ROTATION_90"
  exit 37
fi
assert_window_count 4
read_prefs > "$OUT/07_rotation90.xml"
adb exec-out screencap -p > "$OUT/07_rotation90.png"
adb shell settings put system user_rotation 0
wait_pref 'name="rotation" value="0"' 120 || true
adb shell settings put system accelerometer_rotation "$ACCEL"
adb shell settings put system user_rotation "$USERROT"
log "PASS F2: four-part group survives controlled rotation"

log "Screen off/on must preserve complete child set"
adb shell input keyevent KEYCODE_SLEEP
wait_pref 'name="screenOffSeen" value="true"' 100
adb shell input keyevent KEYCODE_WAKEUP
adb shell wm dismiss-keyguard >/dev/null 2>&1 || true
wait_pref 'name="screenOnSeen" value="true"' 120
assert_window_count 4
read_prefs > "$OUT/08_screen_cycle.xml"
log "PASS F2: screen off/on retains complete child set"

log "Switch F2→F1→F0 with no stale child Windows"
qa f1
wait_pref 'name="childCount" value="2"' 80
assert_window_count 2
qa f0
wait_pref 'name="childCount" value="1"' 80
assert_window_count 1
adb shell dumpsys window windows > "$OUT/09_switch_final_windows.txt"
if grep -Eq 'MobiP1B22-(CORE|FORE|HIND|TAIL)' "$OUT/09_switch_final_windows.txt"; then
  log "FAIL: stale partition Window after F0 switch"
  exit 38
fi
log "PASS: variant switching removes stale child Windows"

log "Explicit stop must remove all child Windows and service"
qa stop
wait_pref 'name="serviceActive" value="false"' 100
sleep 1
assert_window_count 0
adb shell dumpsys activity services "$PKG" > "$OUT/10_after_stop_services.txt"
if grep -q 'org.example.mobifootprint/.MultiWindowService' "$OUT/10_after_stop_services.txt"; then
  log "FAIL: service still active after stop"
  exit 39
fi
read_prefs > "$OUT/10_after_stop.xml"
log "PASS: explicit stop removes every child Window and service"

adb shell dumpsys package "$PKG" > "$OUT/package.txt"
adb shell getprop > "$OUT/device_getprop.txt"
sha256sum "$APK" > "$OUT/apk_sha256.txt"
log "P1-B2.2 generic Android multi-window footprint smoke PASS"
