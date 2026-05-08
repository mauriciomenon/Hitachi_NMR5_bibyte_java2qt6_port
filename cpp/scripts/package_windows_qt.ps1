param(
    [Parameter(Mandatory = $true)]
    [string]$BuildDir,

    [Parameter(Mandatory = $true)]
    [string]$InstallDir,

    [Parameter(Mandatory = $true)]
    [string]$Version
)

$ErrorActionPreference = "Stop"

if (Test-Path $InstallDir) {
    Remove-Item -Recurse -Force $InstallDir
}

cmake --install $BuildDir --prefix $InstallDir

$exePath = Join-Path $InstallDir "bin\nmr5_qml.exe"
if (-not (Test-Path $exePath)) {
    throw "Executable not found: $exePath"
}

$windeployqt = $env:WINDEPLOYQT
if (-not $windeployqt) {
    $command = Get-Command windeployqt.exe -ErrorAction SilentlyContinue
    if ($command) {
        $windeployqt = $command.Source
    }
}
if (-not $windeployqt -or -not (Test-Path $windeployqt)) {
    throw "windeployqt.exe not found. Install Qt tools or set WINDEPLOYQT."
}

$qmlDir = Join-Path $PSScriptRoot "..\qml"
& $windeployqt --qmldir $qmlDir $exePath

$zipPath = Join-Path (Split-Path $InstallDir -Parent) "nmr5-qml-$Version-windows-with-qt.zip"
if (Test-Path $zipPath) {
    Remove-Item -Force $zipPath
}

Compress-Archive -Path (Join-Path $InstallDir "*") -DestinationPath $zipPath
Write-Host "Created $zipPath"
