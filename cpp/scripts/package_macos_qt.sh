#!/usr/bin/env bash
set -Eeuo pipefail

exe_path="${1:?missing executable path}"
out_dir="${2:?missing output directory}"
version="${3:?missing version}"

app_name="NMR5QtQML"
bundle_dir="$out_dir/$app_name.app"
zip_path="$out_dir/nmr5-qml-$version-macos-with-qt.zip"
deploy_log="$out_dir/macdeployqt.log"
build_dir="$(cd "$(dirname "$exe_path")" && pwd)"

if [[ ! -x "$exe_path" ]]; then
    echo "Executable not found or not executable: $exe_path" >&2
    exit 2
fi

macdeployqt_path="${MACDEPLOYQT:-}"
if [[ -z "$macdeployqt_path" ]]; then
    macdeployqt_path="$(command -v macdeployqt || true)"
fi
if [[ -z "$macdeployqt_path" || ! -x "$macdeployqt_path" ]]; then
    echo "macdeployqt not found. Install Qt tools or set MACDEPLOYQT." >&2
    exit 2
fi

rm -rf "$out_dir"
mkdir -p "$bundle_dir/Contents/MacOS" "$bundle_dir/Contents/Resources"
cp "$exe_path" "$bundle_dir/Contents/MacOS/nmr5_qml"
chmod +x "$bundle_dir/Contents/MacOS/nmr5_qml"

cat >"$bundle_dir/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>nmr5_qml</string>
    <key>CFBundleIdentifier</key>
    <string>br.com.menon.nmr5qml</string>
    <key>CFBundleName</key>
    <string>NMR5 Qt/QML</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>$version</string>
</dict>
</plist>
PLIST

qt_lib_dir="$(cd "$(dirname "$macdeployqt_path")/../lib" && pwd)"
qt_link_dir="$build_dir/lib"
deploy_link_dir="$out_dir/lib"
mkdir -p "$qt_link_dir" "$deploy_link_dir"
for framework in "$qt_lib_dir"/Qt*.framework; do
    [[ -e "$framework" ]] || continue
    ln -sfn "$framework" "$qt_link_dir/$(basename "$framework")"
    ln -sfn "$framework" "$deploy_link_dir/$(basename "$framework")"
done
"$macdeployqt_path" "$bundle_dir" \
    -libpath="$qt_lib_dir" \
    -no-codesign \
    -verbose=1 \
    2>&1 | tee "$deploy_log"

if grep -q "ERROR:" "$deploy_log"; then
    echo "macdeployqt reported errors. See $deploy_log" >&2
    exit 1
fi

rm -f "$zip_path"
ditto -c -k --keepParent "$bundle_dir" "$zip_path"
echo "Created $zip_path"
