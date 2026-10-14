#!/usr/bin/env bash
set -uo pipefail

PROBE=com.example.overlayprobe
HOST=com.example.touchhost
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
APK_DIR=${APK_DIR:-"$ROOT/mobi/e6-package/apks"}
OUT=${OUT:-"$ROOT/mobi/output/samsung-e6-$(date +%Y%m%d-%H%M%S)"}
RUN_ROTATION=${RUN_ROTATION:-1}
CLEANUP_APPS=${CLEANUP_APPS:-0}

mkdir -p "$OUT"
: > "$OUT/summary.txt"
failures=0
constraints=0

log() {
  echo "[samsung-e6] $*" | tee -a "$OUT/summary.txt"
}

fail() {
  log "FAIL: $*"
  failures=$((failures + 1))
}

constraint() {
  log "CONSTRAINT: $*"
  constraints=$((constraints + 1))
}

kv() {
  local key="$1" text="$2"
  printf '%s\n' "$text" | sed -n "s/^${key}=//p" | tail -n 1
}

insets_bottom() {
  printf '%s\n' "$1" | awk -F',' '{print $4}'
}

read_private_file() {
  local pkg="$1" file="$2"
  adb shell run-as "$pkg" cat "files/$file" 2>/dev/null | tr -d '\r' || true
}

copy_private_file() {
  local pkg="$1" file="$2" dest="$3"
  adb shell run-as "$pkg" cat "files/$file" > "$OUT/$dest" 2>/dev/null || true
}

probe_command() {
  adb shell am broadcast \
    -a com.example.overlayprobe.COMMAND \
    -n "$PROBE/.ProbeCommandReceiver" \
    --es mode "$1" >/dev/null
  sleep 1
}

host_command() {
  adb shell am broadcast \
    -a com.example.touchhost.COMMAND \
    -p "$HOST" \
    --es mode "$1" >/dev/null
}

capture_focus() {
  local stem="$1"
  adb shell dumpsys window > "$OUT/${stem}_window.txt" 2>&1 || true
  grep -E 'mCurrentFocus=|mFocusedApp=' "$OUT/${stem}_window.txt" > "$OUT/${stem}_focus.txt" || true
}

ensure_host_focus() {
  local label="$1" attempt
  for attempt in $(seq 1 6); do
    capture_focus "focus_${label}_${attempt}"
    if grep -Eq 'mCurrentFocus=.*com\.example\.touchhost' "$OUT/focus_${label}_${attempt}_focus.txt"; then
      log "PASS: host is actual focused window before $label"
      return 0
    fi
    adb shell am start -W -n "$HOST/.MainActivity" >> "$OUT/host_relaunch.txt" 2>&1 || true
    sleep 2
  done
  fail "host never became actual focused window before $label"
  return 1
}

wait_host_ime() {
  local expected="$1" label="$2" attempt text value
  for attempt in $(seq 1 30); do
    text=$(read_private_file "$HOST" host_ime_latest.txt)
    value=$(kv imeVisible "$text")
    if [[ "$value" == "$expected" ]]; then
      log "PASS: host IME $label reached imeVisible=$expected"
      return 0
    fi
    sleep 0.35
  done
  fail "host IME $label did not reach imeVisible=$expected"
  return 1
}

capture_state() {
  local stem="$1"
  probe_command capture
  host_command capture
  sleep 0.5
  copy_private_file "$PROBE" env_latest.txt "${stem}_probe_env.txt"
  copy_private_file "$PROBE" overlay_view_insets_latest.txt "${stem}_probe_view_insets.txt"
  copy_private_file "$HOST" host_ime_latest.txt "${stem}_host_ime.txt"
  adb shell dumpsys window windows > "$OUT/${stem}_windows.txt" 2>&1 || true
  adb shell dumpsys input_method > "$OUT/${stem}_input_method.txt" 2>&1 || true
  adb exec-out screencap -p > "$OUT/${stem}.png" 2>/dev/null || true
}

compare_global_ime() {
  local stem="$1"
  local host_text probe_text host_visible host_insets host_bottom metrics_visible metrics_insets metrics_bottom
  host_text=$(cat "$OUT/${stem}_host_ime.txt" 2>/dev/null || true)
  probe_text=$(cat "$OUT/${stem}_probe_env.txt" 2>/dev/null || true)
  host_visible=$(kv imeVisible "$host_text")
  host_insets=$(kv imeInsets "$host_text")
  host_bottom=$(insets_bottom "${host_insets:-0,0,0,0}")
  metrics_visible=$(kv metricsImeVisible "$probe_text")
  metrics_insets=$(kv metricsImeInsets "$probe_text")
  metrics_bottom=$(insets_bottom "${metrics_insets:-0,0,0,0}")
  echo "$stem hostVisible=$host_visible hostInsets=$host_insets metricsVisible=$metrics_visible metricsInsets=$metrics_insets" \
    | tee -a "$OUT/ime_comparison.txt"
  if [[ "$host_visible" == "true" && "$metrics_visible" == "true" && "${host_bottom:-0}" -gt 0 && "$host_bottom" == "$metrics_bottom" ]]; then
    log "PASS: $stem WindowMetrics IME geometry matches host control bottom=$host_bottom"
  else
    fail "$stem global IME mismatch hostVisible=$host_visible hostBottom=$host_bottom metricsVisible=$metrics_visible metricsBottom=$metrics_bottom"
  fi
}

wait_rotation() {
  local expected="$1" stem="$2" attempt
  for attempt in $(seq 1 16); do
    adb shell dumpsys window displays > "$OUT/${stem}_${attempt}_display.txt" 2>&1 || true
    adb shell dumpsys window > "$OUT/${stem}_${attempt}_window.txt" 2>&1 || true
    if [[ "$expected" == "90" ]]; then
      if grep -Eq 'mCurrentRotation=ROTATION_90|mRotation=1([^0-9]|$)|mDisplayRotation=ROTATION_90' \
        "$OUT/${stem}_${attempt}_display.txt" "$OUT/${stem}_${attempt}_window.txt"; then
        return 0
      fi
    else
      if grep -Eq 'mCurrentRotation=ROTATION_0|mRotation=0([^0-9]|$)|mDisplayRotation=ROTATION_0' \
        "$OUT/${stem}_${attempt}_display.txt" "$OUT/${stem}_${attempt}_window.txt"; then
        return 0
      fi
    fi
    sleep 0.5
  done
  return 1
}

original_accel=$(adb shell settings get system accelerometer_rotation 2>/dev/null | tr -d '\r' || echo unknown)
original_user_rotation=$(adb shell settings get system user_rotation 2>/dev/null | tr -d '\r' || echo unknown)

cleanup() {
  adb shell am broadcast -a com.example.overlayprobe.COMMAND -n "$PROBE/.ProbeCommandReceiver" --es mode remove >/dev/null 2>&1 || true
  adb shell am force-stop "$PROBE" >/dev/null 2>&1 || true
  adb shell am force-stop "$HOST" >/dev/null 2>&1 || true
  if [[ "$original_accel" =~ ^[01]$ ]]; then
    adb shell settings put system accelerometer_rotation "$original_accel" >/dev/null 2>&1 || true
  fi
  if [[ "$original_user_rotation" =~ ^[0-3]$ ]]; then
    adb shell settings put system user_rotation "$original_user_rotation" >/dev/null 2>&1 || true
  fi
  if [[ "$CLEANUP_APPS" == "1" ]]; then
    adb uninstall "$PROBE" >/dev/null 2>&1 || true
    adb uninstall "$HOST" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

if ! adb get-state >/dev/null 2>&1; then
  echo "No ADB device connected." >&2
  exit 2
fi

manufacturer=$(adb shell getprop ro.product.manufacturer | tr -d '\r')
model=$(adb shell getprop ro.product.model | tr -d '\r')
release=$(adb shell getprop ro.build.version.release | tr -d '\r')
sdk=$(adb shell getprop ro.build.version.sdk | tr -d '\r')
fingerprint=$(adb shell getprop ro.build.fingerprint | tr -d '\r')
security_patch=$(adb shell getprop ro.build.version.security_patch | tr -d '\r')
build_display=$(adb shell getprop ro.build.display.id | tr -d '\r')
default_ime=$(adb shell settings get secure default_input_method | tr -d '\r')

{
  echo "capturedAtUtc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "manufacturer=$manufacturer"
  echo "model=$model"
  echo "androidRelease=$release"
  echo "sdk=$sdk"
  echo "fingerprint=$fingerprint"
  echo "securityPatch=$security_patch"
  echo "buildDisplay=$build_display"
  echo "defaultIme=$default_ime"
  echo "originalAccelerometerRotation=$original_accel"
  echo "originalUserRotation=$original_user_rotation"
  adb shell getprop | grep -Ei 'oneui|sem_platform|build\.PDA|build\.version' || true
} > "$OUT/device_identity.txt"

if [[ "${manufacturer,,}" != *samsung* ]]; then
  log "FAIL: E6 requires a real Samsung device; manufacturer=$manufacturer model=$model"
  exit 3
fi
log "PASS: Samsung device detected manufacturer=$manufacturer model=$model Android=$release SDK=$sdk"

case "$default_ime" in
  com.samsung.android.honeyboard/*|com.sec.android.inputmethod/*|*samsung*|*Samsung*)
    log "PASS: Samsung-family default IME detected: $default_ime"
    ;;
  *)
    log "FAIL: Samsung Keyboard must be the active default IME for this E6 run; current=$default_ime"
    exit 4
    ;;
esac

OVERLAY_APK="$APK_DIR/overlayprobe-debug.apk"
HOST_APK="$APK_DIR/hostprobe-debug.apk"
if [[ ! -f "$OVERLAY_APK" || ! -f "$HOST_APK" ]]; then
  log "FAIL: APKs not found under APK_DIR=$APK_DIR"
  exit 5
fi

sha256sum "$OVERLAY_APK" "$HOST_APK" "$SCRIPT_DIR/run_samsung_e6.sh" > "$OUT/input_sha256.txt"

log "Installing sanitized E6 probe APKs"
adb install -r "$OVERLAY_APK" > "$OUT/install_overlay.txt" 2>&1 || fail "overlay APK install failed"
adb install -r "$HOST_APK" > "$OUT/install_host.txt" 2>&1 || fail "host APK install failed"
adb shell pm clear "$PROBE" >/dev/null 2>&1 || true
adb shell pm clear "$HOST" >/dev/null 2>&1 || true
adb shell appops set "$PROBE" SYSTEM_ALERT_WINDOW allow >/dev/null 2>&1 || fail "SYSTEM_ALERT_WINDOW app-op grant failed"
adb shell pm grant "$PROBE" android.permission.POST_NOTIFICATIONS >/dev/null 2>&1 || true

log "Starting overlay from visible Activity"
adb shell am start -W -n "$PROBE/.MainActivity" > "$OUT/start_probe.txt" 2>&1 || fail "probe Activity failed"
sleep 3
adb shell dumpsys activity services "$PROBE" > "$OUT/services.txt" 2>&1 || true
if grep -q OverlayService "$OUT/services.txt"; then
  log "PASS: overlay foreground service exists"
else
  fail "overlay foreground service missing"
fi

log "Starting synthetic host"
adb shell am start -W -n "$HOST/.MainActivity" > "$OUT/start_host.txt" 2>&1 || fail "host Activity failed"
sleep 2
ensure_host_focus initial || true
host_command reset
host_command show
wait_host_ime true samsung_show || true

log "Mode A: observe Samsung Keyboard with legacy not-focusable flags"
probe_command modeA_bottom
ensure_host_focus modeA || true
capture_state 01_samsung_modeA
compare_global_ime 01_samsung_modeA

modeA_env=$(cat "$OUT/01_samsung_modeA_probe_env.txt" 2>/dev/null || true)
modeA_geometry=$(kv overlayGeometry "$modeA_env")
IFS=',' read -r ax ay aw ah <<< "${modeA_geometry:-0,0,0,0}"
a_center_x=$((ax + aw / 2))
a_center_y=$((ay + ah / 2))
host_before=$(read_private_file "$HOST" host_ime_latest.txt)
host_len_before=$(kv editorLength "$host_before")
overlay_before=$(read_private_file "$PROBE" overlay_count.txt | tr -d '\n' || echo 0)
adb shell input tap "$a_center_x" "$a_center_y" >/dev/null 2>&1 || true
sleep 1
host_command capture
sleep 0.3
host_after=$(read_private_file "$HOST" host_ime_latest.txt)
host_len_after=$(kv editorLength "$host_after")
overlay_after=$(read_private_file "$PROBE" overlay_count.txt | tr -d '\n' || echo 0)
{
  echo "modeA_overlayCenter=$a_center_x,$a_center_y"
  echo "modeA_hostLengthBefore=$host_len_before"
  echo "modeA_hostLengthAfter=$host_len_after"
  echo "modeA_overlayTapBefore=$overlay_before"
  echo "modeA_overlayTapAfter=$overlay_after"
} > "$OUT/modeA_overlap_touch.txt"
if [[ "$overlay_after" =~ ^[0-9]+$ && "$overlay_before" =~ ^[0-9]+$ && $((overlay_after-overlay_before)) -eq 1 ]]; then
  log "PASS: Mode A overlapping touch was consumed by overlay as expected"
else
  constraint "Mode A overlapping touch dispatch was not conclusive"
fi

log "Mode B: place overlay below Samsung Keyboard and compare geometry"
host_command reset
host_command show
wait_host_ime true samsung_show_modeB || true
probe_command modeB_bottom
ensure_host_focus modeB || true
capture_state 02_samsung_modeB
compare_global_ime 02_samsung_modeB

modeB_host=$(cat "$OUT/02_samsung_modeB_host_ime.txt" 2>/dev/null || true)
modeB_editor_focus=$(kv editorFocus "$modeB_host")
if [[ "$modeB_editor_focus" == "true" ]]; then
  log "PASS: host editor remains focused with Mode B overlay present"
else
  fail "host editor lost focus under Mode B"
fi

log "Mode B: verify synthetic text input still reaches focused editor"
before_text=$(kv editorText "$modeB_host")
adb shell input text E6 >/dev/null 2>&1 || true
sleep 1
host_command capture
sleep 0.3
after_host=$(read_private_file "$HOST" host_ime_latest.txt)
after_text=$(kv editorText "$after_host")
{
  echo "before=$before_text"
  echo "after=$after_text"
} > "$OUT/modeB_typing.txt"
if [[ "$after_text" == "${before_text}E6" ]]; then
  log "PASS: synthetic text input reaches host editor with Mode B overlay present"
else
  fail "synthetic text input did not reach host as expected before='$before_text' after='$after_text'"
fi
capture_state 03_samsung_modeB_after_typing

if [[ "$RUN_ROTATION" == "1" ]]; then
  log "Testing One UI rotation with state restoration"
  adb shell wm user-rotation lock 1 >/dev/null 2>&1 || true
  if wait_rotation 90 samsung_rotation90; then
    log "PASS: Samsung device reached ROTATION_90"
    sleep 1
    capture_state 04_samsung_rotation90
  else
    constraint "Samsung device did not reach ROTATION_90 under adb rotation request"
  fi
  adb shell wm user-rotation lock 0 >/dev/null 2>&1 || true
  if wait_rotation 0 samsung_rotation0; then
    log "PASS: Samsung device returned to ROTATION_0"
  else
    constraint "Samsung device did not return to ROTATION_0 before settings restoration"
  fi
fi

copy_private_file "$PROBE" env_events.txt probe_env_events.txt
copy_private_file "$PROBE" overlay_view_insets_events.txt probe_view_insets_events.txt
copy_private_file "$HOST" host_ime_events.txt host_ime_events.txt
adb logcat -d > "$OUT/logcat_final.txt" 2>&1 || true
adb shell dumpsys window displays > "$OUT/window_displays_final.txt" 2>&1 || true
adb shell dumpsys input_method > "$OUT/input_method_final.txt" 2>&1 || true

{
  echo "manufacturer=$manufacturer"
  echo "model=$model"
  echo "defaultIme=$default_ime"
  echo "failures=$failures"
  echo "constraints=$constraints"
  echo "e6Scope=Samsung_OneUI_SamsungKeyboard_structural_observability"
} > "$OUT/result_classification.txt"

log "Samsung E6 failures=$failures constraints=$constraints"
if (( failures > 0 )); then
  exit 1
fi
log "Samsung E6 evidence run completed without critical harness failure"
