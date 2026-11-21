#!/usr/bin/env bash
# Usage: run_hidden.sh <repo checkout> <issue id> [python]
# Installs the checkout (entry points matter for V1) and runs the hidden tests for one issue.
set -euo pipefail
repo="$1"; id="$2"; py="${3:-python}"
here="$(cd "$(dirname "$0")" && pwd)"
"$py" -m pip install -q --no-deps -e "$repo" >/dev/null 2>&1
"$py" -m unittest discover -v -s "$here" -p "test_${id}.py" 2>&1 | tail -n 40
