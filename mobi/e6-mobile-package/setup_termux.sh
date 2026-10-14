#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "[Mobi E6 Mobile] Termux environment setup"

if ! command -v pkg >/dev/null 2>&1; then
  echo "ERROR: This script must be run inside Termux." >&2
  exit 2
fi

pkg update -y
pkg install -y android-tools coreutils grep sed gawk zip unzip

if ! command -v adb >/dev/null 2>&1; then
  echo "ERROR: adb was not installed successfully." >&2
  exit 3
fi

echo
adb version | head -n 2 || true
echo
echo "Setup complete."
echo "Next: open Android Settings > Developer options > Wireless debugging,"
echo "then return to Termux and run: bash pair_connect.sh"
