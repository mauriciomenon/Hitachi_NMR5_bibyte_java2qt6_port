#!/usr/bin/env bash
set -euo pipefail

app_path="${1:-build/nmr5_qml}"
out_path="${2:-build/visual-smoke.png}"
log_path="${3:-build/visual-smoke.log}"
wait_timeout_seconds="${NMR5_VISUAL_TIMEOUT_SECONDS:-10}"

if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "Visual smoke is currently implemented only for macOS." >&2
    exit 2
fi

for tool in osascript screencapture sips; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "Required tool not found: $tool" >&2
        exit 2
    fi
done

if [[ ! -x "$app_path" ]]; then
    echo "Executable not found or not executable: $app_path" >&2
    exit 2
fi

mkdir -p "$(dirname "$out_path")"
mkdir -p "$(dirname "$log_path")"

"$app_path" >"$log_path" 2>&1 &
app_pid=$!
cleanup() {
    if kill -0 "$app_pid" 2>/dev/null; then
        kill "$app_pid" 2>/dev/null || true
        wait "$app_pid" 2>/dev/null || true
    fi
}
trap cleanup EXIT

window_rect=""
deadline=$((SECONDS + wait_timeout_seconds))

while [[ "$SECONDS" -lt "$deadline" ]]; do
    set +e
    window_rect="$(osascript 2>/dev/null <<APPLESCRIPT
tell application "System Events"
    set appProcess to first process whose unix id is $app_pid
    if (count of windows of appProcess) is 0 then error "window not ready"
    set win to window 1 of appProcess
    set winPosition to position of win
    set winSize to size of win
    return (item 1 of winPosition as text) & "," & (item 2 of winPosition as text) & "," & (item 1 of winSize as text) & "," & (item 2 of winSize as text)
end tell
APPLESCRIPT
)"
    osascript_status=$?
    set -e

    if [[ "$osascript_status" -eq 0 && -n "$window_rect" ]]; then
        break
    fi

    sleep 0.2
done

if [[ -z "$window_rect" ]]; then
    echo "Visual capture smoke failed: window not ready. Log: $log_path" >&2
    exit 1
fi

screencapture -x -R"$window_rect" "$out_path"

width="$(sips -g pixelWidth "$out_path" 2>/dev/null | awk '/pixelWidth/ { print $2 }')"
height="$(sips -g pixelHeight "$out_path" 2>/dev/null | awk '/pixelHeight/ { print $2 }')"

if [[ -z "$width" || -z "$height" || "$width" -lt 980 || "$height" -lt 820 ]]; then
    echo "Visual capture smoke failed: unexpected image size ${width}x${height}. Output: $out_path. Log: $log_path" >&2
    exit 1
fi

echo "Visual capture smoke passed: ${width}x${height}. Output: $out_path. Log: $log_path"
