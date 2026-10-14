#!/usr/bin/env bash
set -uo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HARNESS="$ROOT/mobi/harness"
OUT="$ROOT/mobi/output/env-probe"
PROBE=com.example.overlayprobe
HOST=com.example.touchhost

rm -rf "$OUT"
mkdir -p "$OUT"
: > "$OUT/summary.txt"
failures=0

log() {
  echo "[env] $*" | tee -a "$OUT/summary.txt"
}

fail() {
  log "HARNESS_FAIL: $*"
  failures=$((failures + 1))
}

read_private_file() {
  local pkg="$1" file="$2"
  adb shell run-as "$pkg" cat "files/$file" 2>/dev/null | tr -d '\r' || true
}

copy_private_file() {
  local pkg="$1" file="$2" dest="$3"
  adb shell run-as "$pkg" cat "files/$file" > "$OUT/$dest" 2>/dev/null || true
}

kv() {
  local key="$1" text="$2"
  printf '%s\n' "$text" | sed -n "s/^${key}=//p" | tail -n 1
}

insets_bottom() {
  local value="$1"
  printf '%s\n' "$value" | awk -F',' '{print $4}'
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
  local name="$1"
  adb shell dumpsys window > "$OUT/${name}_window.txt" 2>&1 || true
  grep -E 'mCurrentFocus=|mFocusedApp=' "$OUT/${name}_window.txt" > "$OUT/${name}_focus.txt" || true
}

host_is_current_focus() {
  capture_focus focus_probe
  grep -Eq 'mCurrentFocus=.*com\.example\.touchhost' "$OUT/focus_probe_focus.txt"
}

ensure_host_focus() {
  local label="$1" attempt
  for attempt in $(seq 1 5); do
    if host_is_current_focus; then
      log "PASS: host is actual focused window before $label"
      return 0
    fi
    adb exec-out screencap -p > "$OUT/focus_recovery_${label}_${attempt}.png" 2>/dev/null || true
    adb shell input keyevent KEYCODE_BACK >/dev/null 2>&1 || true
    adb shell am start -W -n "$HOST/.MainActivity" >> "$OUT/host_relaunch.txt" 2>&1 || true
    sleep 2
  done
  fail "host never became actual focused window before $label"
  return 1
}

wait_host_ime() {
  local expected="$1" label="$2" attempt text value
  for attempt in $(seq 1 25); do
    text=$(read_private_file "$HOST" host_ime_latest.txt)
    value=$(kv imeVisible "$text")
    if [[ "$value" == "$expected" ]]; then
      log "PASS: host IME state $label reached imeVisible=$expected"
      return 0
    fi
    sleep 0.4
  done
  fail "host IME state $label did not reach imeVisible=$expected"
  copy_private_file "$HOST" host_ime_latest.txt "host_${label}_timeout.txt"
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

wait_rotation() {
  local expected="$1" stem="$2" attempt
  for attempt in $(seq 1 12); do
    adb shell dumpsys window displays > "$OUT/${stem}_${attempt}_display.txt" 2>&1 || true
    adb shell dumpsys window > "$OUT/${stem}_${attempt}_window.txt" 2>&1 || true
    if [[ "$expected" == "90" ]]; then
      if grep -Eq 'mCurrentRotation=ROTATION_90|mRotation=1([^0-9]|$)|mDisplayRotation=ROTATION_90' \
        "$OUT/${stem}_${attempt}_display.txt" "$OUT/${stem}_${attempt}_window.txt"; then
        cp "$OUT/${stem}_${attempt}_display.txt" "$OUT/${stem}_display.txt"
        cp "$OUT/${stem}_${attempt}_window.txt" "$OUT/${stem}_window.txt"
        return 0
      fi
    else
      if grep -Eq 'mCurrentRotation=ROTATION_0|mRotation=0([^0-9]|$)|mDisplayRotation=ROTATION_0' \
        "$OUT/${stem}_${attempt}_display.txt" "$OUT/${stem}_${attempt}_window.txt"; then
        cp "$OUT/${stem}_${attempt}_display.txt" "$OUT/${stem}_display.txt"
        cp "$OUT/${stem}_${attempt}_window.txt" "$OUT/${stem}_window.txt"
        return 0
      fi
    fi
    sleep 0.5
  done
  return 1
}

cd "$HARNESS"
adb logcat -c

log "Recording exact execution identity"
{
  echo "git_commit=$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo unknown)"
  echo "java=$(java -version 2>&1 | head -n 1)"
  echo "gradle=$(gradle --version 2>/dev/null | awk '/^Gradle / {print $2; exit}')"
  echo "device_sdk=$(adb shell getprop ro.build.version.sdk | tr -d '\r')"
  echo "device_release=$(adb shell getprop ro.build.version.release | tr -d '\r')"
  echo "device_fingerprint=$(adb shell getprop ro.build.fingerprint | tr -d '\r')"
  echo "device_model=$(adb shell getprop ro.product.model | tr -d '\r')"
  echo "default_ime=$(adb shell settings get secure default_input_method | tr -d '\r')"
  echo "enabled_imes=$(adb shell ime list -s | tr '\n' ';' | tr -d '\r')"
} > "$OUT/execution_identity.txt"

sha256sum \
  overlayprobe/src/main/java/com/example/overlayprobe/OverlayService.java \
  overlayprobe/src/main/java/com/example/overlayprobe/MainActivity.java \
  overlayprobe/src/main/java/com/example/overlayprobe/ProbeCommandReceiver.java \
  overlayprobe/src/main/AndroidManifest.xml \
  hostprobe/src/main/java/com/example/touchhost/MainActivity.java \
  hostprobe/src/main/AndroidManifest.xml \
  build.gradle settings.gradle gradle.properties \
  "$ROOT/mobi/tools/run_env_probe.sh" \
  > "$OUT/source_sha256.txt"

log "Installing generic probe APKs"
adb install -r overlayprobe/build/outputs/apk/debug/overlayprobe-debug.apk > "$OUT/install_overlay.txt" 2>&1 || fail "overlay APK install failed"
adb install -r hostprobe/build/outputs/apk/debug/hostprobe-debug.apk > "$OUT/install_host.txt" 2>&1 || fail "host APK install failed"
adb shell pm clear "$PROBE" >/dev/null 2>&1 || true
adb shell pm clear "$HOST" >/dev/null 2>&1 || true
adb shell appops set "$PROBE" SYSTEM_ALERT_WINDOW allow || fail "SYSTEM_ALERT_WINDOW app-op grant failed"
adb shell pm grant "$PROBE" android.permission.POST_NOTIFICATIONS >/dev/null 2>&1 || true

log "Starting overlay service from visible Activity"
adb shell am start -W -n "$PROBE/.MainActivity" > "$OUT/start_probe_activity.txt" 2>&1 || fail "probe Activity failed to start"
sleep 3
adb shell dumpsys activity services "$PROBE" > "$OUT/services_after_start.txt" 2>&1 || true
if grep -q OverlayService "$OUT/services_after_start.txt"; then
  log "PASS: foreground overlay service exists"
else
  fail "foreground overlay service missing"
fi

log "Starting synthetic different-UID IME host"
adb shell am start -W -n "$HOST/.MainActivity" > "$OUT/start_host_activity.txt" 2>&1 || fail "host Activity failed to start"
sleep 2
ensure_host_focus initial_host || true
host_command hide
wait_host_ime false initial_hidden || true
capture_state 01_hidden_modeA_top

log "Showing docked IME with host editor focused"
ensure_host_focus before_show || true
host_command show
wait_host_ime true first_show || true
sleep 1
capture_state 02_host_ime_shown_modeA_top

host_text=$(read_private_file "$HOST" host_ime_latest.txt)
host_visible=$(kv imeVisible "$host_text")
host_insets=$(kv imeInsets "$host_text")
host_bottom=$(insets_bottom "${host_insets:-0,0,0,0}")
if [[ "$host_visible" == "true" && "${host_bottom:-0}" -gt 0 ]]; then
  log "PASS: host control channel reports visible docked IME bottom=$host_bottom"
else
  fail "host control channel did not produce positive docked IME geometry visible=$host_visible insets=$host_insets"
fi

log "Testing Mode A overlap/z-order while IME remains visible"
probe_command modeA_bottom
ensure_host_focus modeA_bottom || true
host_command capture
sleep 0.5
capture_state 03_modeA_bottom_ime_shown

log "Testing Mode B ALT_FOCUSABLE_IM overlap/z-order while IME remains visible"
probe_command modeB_bottom
ensure_host_focus modeB_bottom || true
host_command capture
sleep 0.5
capture_state 04_modeB_bottom_ime_shown

log "Recording cross-app IME observability without deciding the product result inside the harness"
for stem in 03_modeA_bottom_ime_shown 04_modeB_bottom_ime_shown; do
  probe_text=$(cat "$OUT/${stem}_probe_env.txt" 2>/dev/null || true)
  metrics_visible=$(kv metricsImeVisible "$probe_text")
  metrics_insets=$(kv metricsImeInsets "$probe_text")
  root_visible=$(kv rootImeVisible "$probe_text")
  root_insets=$(kv rootImeInsets "$probe_text")
  echo "$stem metricsImeVisible=$metrics_visible metricsImeInsets=$metrics_insets rootImeVisible=$root_visible rootImeInsets=$root_insets" \
    | tee -a "$OUT/observability_comparison.txt"
done

log "Hiding IME and verifying controlled transition"
host_command hide
wait_host_ime false after_hide || true
capture_state 05_hidden_modeB

log "Repeating show transition under Mode B"
ensure_host_focus before_repeat_show || true
host_command show
wait_host_ime true repeat_show || true
sleep 1
capture_state 06_repeat_show_modeB

log "Testing verified rotation while IME is requested visible"
adb shell wm user-rotation lock 1
if wait_rotation 90 rotation_90; then
  log "PASS: actual display reached ROTATION_90"
  sleep 1
  capture_state 07_rotation90_modeB
else
  fail "actual display did not reach ROTATION_90"
fi
adb shell wm user-rotation lock 0
if wait_rotation 0 rotation_restore; then
  log "PASS: display restored to ROTATION_0"
else
  fail "display did not restore to ROTATION_0"
fi
sleep 1
capture_state 08_rotation_restored

log "Testing interactive/display-state cycle and dynamic screen broadcasts"
adb shell input keyevent KEYCODE_POWER >/dev/null 2>&1 || true
sleep 2
probe_command capture
copy_private_file "$PROBE" env_latest.txt 09_screen_noninteractive_probe_env.txt
adb shell dumpsys power > "$OUT/09_screen_noninteractive_power.txt" 2>&1 || true
adb shell dumpsys display > "$OUT/09_screen_noninteractive_display.txt" 2>&1 || true
adb shell input keyevent KEYCODE_POWER >/dev/null 2>&1 || true
sleep 2
adb shell wm dismiss-keyguard >/dev/null 2>&1 || true
sleep 1
probe_command capture
capture_state 10_screen_interactive_restored

copy_private_file "$PROBE" env_events.txt probe_env_events.txt
copy_private_file "$PROBE" overlay_view_insets_events.txt probe_view_insets_events.txt
copy_private_file "$HOST" host_ime_events.txt host_ime_events.txt
adb logcat -d > "$OUT/logcat_final.txt" 2>&1 || true
adb shell dumpsys window displays > "$OUT/window_displays_final.txt" 2>&1 || true
adb shell dumpsys input_method > "$OUT/input_method_final.txt" 2>&1 || true

log "Classifying whether either low-permission overlay mode observed positive docked IME geometry"
positive_mode="none"
for stem in 03_modeA_bottom_ime_shown 04_modeB_bottom_ime_shown 06_repeat_show_modeB; do
  probe_text=$(cat "$OUT/${stem}_probe_env.txt" 2>/dev/null || true)
  metrics_visible=$(kv metricsImeVisible "$probe_text")
  metrics_insets=$(kv metricsImeInsets "$probe_text")
  root_visible=$(kv rootImeVisible "$probe_text")
  root_insets=$(kv rootImeInsets "$probe_text")
  metrics_bottom=$(insets_bottom "${metrics_insets:-0,0,0,0}")
  root_bottom=$(insets_bottom "${root_insets:-0,0,0,0}")
  if [[ "$metrics_visible" == "true" && "${metrics_bottom:-0}" -gt 0 ]]; then
    positive_mode="$stem:metrics"
    break
  fi
  if [[ "$root_visible" == "true" && "${root_bottom:-0}" -gt 0 ]]; then
    positive_mode="$stem:root"
    break
  fi
done
{
  echo "host_control_visible=$host_visible"
  echo "host_control_bottom=$host_bottom"
  echo "positive_overlay_observation=$positive_mode"
  echo "floating_ime_validation=UNSUPPORTED_NOT_CONFIGURED"
  echo "floating_ime_geometry_policy=UNKNOWN_OR_PARTIAL_IF_VISIBLE_WITH_ZERO_INSETS"
  echo "harness_failure_count=$failures"
} > "$OUT/result_classification.txt"

if [[ "$positive_mode" == "none" ]]; then
  log "EVIDENCE_RESULT: no tested overlay source reported positive docked IME geometry; checkpoint must assess this as a technical constraint, not a harness failure"
else
  log "EVIDENCE_RESULT: positive low-permission cross-app IME observation found via $positive_mode"
fi

log "Harness failure count=$failures"
if (( failures > 0 )); then
  exit 1
fi
log "Environment evidence harness completed successfully"
