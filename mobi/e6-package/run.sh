#!/usr/bin/env bash
set -euo pipefail
DIR=$(cd "$(dirname "$0")" && pwd)
STAMP=$(date +%Y%m%d-%H%M%S)
export APK_DIR="$DIR/apks"
export OUT="${OUT:-$DIR/evidence/$STAMP}"
exec bash "$DIR/run_samsung_e6.sh"
