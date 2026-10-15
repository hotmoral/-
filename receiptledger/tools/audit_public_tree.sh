#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

bad_paths="$(find receiptledger -type f \( \
  -iname '*.jks' -o -iname '*.keystore' -o -iname '*.p12' -o -iname '*.pfx' -o \
  -iname '*.pem' -o -iname '*.key' -o -iname '*.sqlite' -o -iname '*.sqlite3' -o \
  -iname '*.db' -o -iname '*.aab' -o -iname '*.apk' \
\) -print)"
if [[ -n "$bad_paths" ]]; then
  echo "Forbidden public material detected:"
  echo "$bad_paths"
  exit 20
fi

if grep -RInE --exclude='audit_public_tree.sh' \
  '(BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY|storePassword[[:space:]]*=|keyPassword[[:space:]]*=|gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})' \
  receiptledger; then
  echo "Potential secret material detected"
  exit 21
fi

if git rev-parse --verify main >/dev/null 2>&1; then
  mapfile -t changed < <(git diff --name-only main...HEAD)
  for path in "${changed[@]}"; do
    case "$path" in
      receiptledger/*|.github/workflows/receiptledger-*.yml) ;;
      *)
        echo "ReceiptLedger isolation violation: $path"
        exit 22
        ;;
    esac
  done
fi

echo "ReceiptLedger public-tree audit PASS"
