#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

DIR=$(cd "$(dirname "$0")" && pwd)
TARGET_FILE="$DIR/.adb_target"

if ! command -v adb >/dev/null 2>&1; then
  echo "ERROR: adb is missing. Run: bash setup_termux.sh" >&2
  exit 2
fi

adb start-server >/dev/null 2>&1 || true

echo
cat <<'EOF'
[Mobi E6 Mobile] Wireless debugging pairing

1) Leave Termux open in recent apps.
2) Open Android Settings > Developer options > Wireless debugging.
3) Turn Wireless debugging ON.
4) Tap "Pair device with pairing code".
5) Enter the shown IP address & pairing port below, then the 6-digit code.
EOF

read -r -p "Pairing address (example 192.168.0.10:37123): " PAIR_ADDR
read -r -p "6-digit pairing code: " PAIR_CODE

if [[ "$PAIR_ADDR" != *:* || -z "$PAIR_CODE" ]]; then
  echo "ERROR: Pairing address/code is incomplete." >&2
  exit 3
fi

set +e
adb pair "$PAIR_ADDR" "$PAIR_CODE"
PAIR_RC=$?
set -e
if (( PAIR_RC != 0 )); then
  PAIR_PORT=${PAIR_ADDR##*:}
  echo "Pairing to the displayed address failed; trying local loopback with the same pairing port."
  adb pair "127.0.0.1:$PAIR_PORT" "$PAIR_CODE"
fi

echo
cat <<'EOF'
Return to the main Wireless debugging screen.
Use its normal "IP address & Port" entry (this is usually a DIFFERENT port from the pairing screen).
EOF
read -r -p "Connection address (example 192.168.0.10:42137): " CONNECT_ADDR

if [[ "$CONNECT_ADDR" != *:* ]]; then
  echo "ERROR: Connection address must include a port." >&2
  exit 4
fi

set +e
CONNECT_OUTPUT=$(adb connect "$CONNECT_ADDR" 2>&1)
CONNECT_RC=$?
set -e
echo "$CONNECT_OUTPUT"

if (( CONNECT_RC != 0 )) || ! printf '%s' "$CONNECT_OUTPUT" | grep -Eqi 'connected to|already connected'; then
  CONNECT_PORT=${CONNECT_ADDR##*:}
  echo "Displayed address did not connect; trying local loopback with the same connection port."
  adb connect "127.0.0.1:$CONNECT_PORT"
fi

mapfile -t DEVICES < <(adb devices | awk 'NR>1 && $2=="device" {print $1}')
if (( ${#DEVICES[@]} == 0 )); then
  echo "ERROR: No authorized wireless ADB device is connected." >&2
  adb devices
  exit 5
fi

TARGET="${DEVICES[0]}"
if (( ${#DEVICES[@]} > 1 )); then
  echo "Multiple ADB devices are connected:"
  printf '  %s\n' "${DEVICES[@]}"
  read -r -p "Type the target serial/address exactly: " TARGET
fi

export ANDROID_SERIAL="$TARGET"
MANUFACTURER=$(adb shell getprop ro.product.manufacturer | tr -d '\r')
MODEL=$(adb shell getprop ro.product.model | tr -d '\r')

printf '%s\n' "$TARGET" > "$TARGET_FILE"
chmod 600 "$TARGET_FILE" 2>/dev/null || true

echo
echo "ADB connected."
echo "Target: $TARGET"
echo "Device: $MANUFACTURER $MODEL"
echo "Next: bash run.sh"
