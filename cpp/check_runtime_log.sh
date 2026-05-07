#!/usr/bin/env bash
set -euo pipefail

app_path="${1:-build/nmr5_qml}"
log_path="${2:-build/runtime-check.log}"
run_seconds="${NMR5_RUNTIME_SECONDS:-2}"

if [[ ! -x "$app_path" ]]; then
    echo "Executable not found or not executable: $app_path" >&2
    exit 2
fi

mkdir -p "$(dirname "$log_path")"

"$app_path" >"$log_path" 2>&1 &
app_pid=$!

sleep "$run_seconds"

set +e
if kill -0 "$app_pid" 2>/dev/null; then
    kill "$app_pid" 2>/dev/null
    wait "$app_pid" 2>/dev/null
    app_status=$?
else
    wait "$app_pid" 2>/dev/null
    app_status=$?
fi
set -e

if [[ "$app_status" -ne 0 && "$app_status" -ne 143 ]]; then
    echo "Runtime exited with status $app_status. Log: $log_path" >&2
    exit "$app_status"
fi

error_pattern='Unable to assign|ReferenceError|TypeError|QQmlApplicationEngine failed|module .* is not installed|qrc:/'
if grep -En "$error_pattern" "$log_path"; then
    echo "QML runtime log check failed. Log: $log_path" >&2
    exit 1
fi

echo "QML runtime log check passed. Log: $log_path"
