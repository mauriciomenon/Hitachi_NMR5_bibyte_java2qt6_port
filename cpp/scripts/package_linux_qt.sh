#!/usr/bin/env bash
set -Eeuo pipefail

exe_path="${1:?missing executable path}"
out_dir="${2:?missing output directory}"
version="${3:?missing version}"

appdir="$out_dir/NMR5QtQML.AppDir"

if [[ ! -x "$exe_path" ]]; then
    echo "Executable not found or not executable: $exe_path" >&2
    exit 2
fi

linuxdeployqt_path="${LINUXDEPLOYQT:-}"
if [[ -z "$linuxdeployqt_path" ]]; then
    linuxdeployqt_path="$(command -v linuxdeployqt || true)"
fi
if [[ -z "$linuxdeployqt_path" || ! -x "$linuxdeployqt_path" ]]; then
    echo "linuxdeployqt not found. Install linuxdeployqt or set LINUXDEPLOYQT." >&2
    exit 2
fi

rm -rf "$out_dir"
mkdir -p "$appdir/usr/bin" "$appdir/usr/share/applications"
cp "$exe_path" "$appdir/usr/bin/nmr5_qml"
chmod +x "$appdir/usr/bin/nmr5_qml"

cat >"$appdir/usr/share/applications/nmr5-qml.desktop" <<DESKTOP
[Desktop Entry]
Type=Application
Name=NMR5 Qt/QML
Exec=nmr5_qml
Categories=Utility;
DESKTOP

"$linuxdeployqt_path" "$appdir/usr/share/applications/nmr5-qml.desktop" \
    -qmldir="$PWD/qml" \
    -appimage

echo "Created Linux package in $out_dir for version $version"
