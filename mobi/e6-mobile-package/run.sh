#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

DIR=$(cd "$(dirname "$0")" && pwd)
TARGET_FILE="$DIR/.adb_target"
STAMP=$(date +%Y%m%d-%H%M%S)
OUT_DIR="$DIR/evidence/$STAMP"
ZIP_OUT="$DIR/mobi-samsung-e6-evidence-$STAMP.zip"

if ! command -v adb >/dev/null 2>&1; then
  echo "ERROR: adb is missing. Run bash setup_termux.sh first." >&2
  exit 2
fi

if [[ -f "$TARGET_FILE" ]]; then
  export ANDROID_SERIAL=$(tr -d '\r\n' < "$TARGET_FILE")
fi

if ! adb get-state >/dev/null 2>&1; then
  echo "ERROR: Wireless ADB is not connected." >&2
  echo "Run: bash pair_connect.sh" >&2
  exit 3
fi

MANUFACTURER=$(adb shell getprop ro.product.manufacturer | tr -d '\r')
MODEL=$(adb shell getprop ro.product.model | tr -d '\r')
DEFAULT_IME=$(adb shell settings get secure default_input_method | tr -d '\r')

echo "Target: $MANUFACTURER $MODEL"
echo "Default IME: $DEFAULT_IME"
echo

if [[ "${MANUFACTURER,,}" != *samsung* ]]; then
  echo "ERROR: This E6 package requires a real Samsung Galaxy." >&2
  exit 4
fi

case "$DEFAULT_IME" in
  com.samsung.android.honeyboard/*|com.sec.android.inputmethod/*|*samsung*|*Samsung*) ;;
  *)
    echo "ERROR: Samsung Keyboard is not the active default keyboard." >&2
    echo "Switch the default keyboard to Samsung Keyboard, then run again." >&2
    exit 5
    ;;
esac

export APK_DIR="$DIR/apks"
export OUT="$OUT_DIR"
export RUN_ROTATION="${RUN_ROTATION:-1}"
export CLEANUP_APPS="${CLEANUP_APPS:-0}"

mkdir -p "$DIR/evidence"

set +e
bash "$DIR/run_samsung_e6.sh"
RUN_RC=$?
set -e

if [[ -d "$OUT_DIR" ]]; then
  (
    cd "$DIR"
    zip -qr "$(basename "$ZIP_OUT")" "evidence/$STAMP"
  )
  echo
  echo "Evidence ZIP created:"
  echo "$ZIP_OUT"
else
  echo "WARNING: Evidence directory was not created." >&2
fi

if (( RUN_RC == 0 )); then
  echo
echo "E6 test script completed without critical harness failure."
echo "Upload the evidence ZIP to the Mobi ChatGPT conversation for review."
else
  echo
echo "E6 test script returned code $RUN_RC."
echo "The evidence ZIP is still useful. Upload it for diagnosis; do not rerun repeatedly." >&2
fi

exit "$RUN_RC"
