Set-Location $PSScriptRoot
$ROOT = git rev-parse --show-toplevel
. $ROOT/scripts/util.ps1
$name=get-name
Remove-Item $ROOT/temp/$name -Recurse -ErrorAction SilentlyContinue
New-Item $ROOT/temp/$name -ItemType Directory
aria2c -c -x16 -s16 -d "$ROOT/temp/$name/" `
    "https://sourceforge.net/projects/pkgconfiglite/files/0.28-1/$name-0.28-1_bin-win32.zip/download" `
    -o "$name.zip"
Expand-Archive $ROOT/temp/$name/$name.zip $ROOT/temp/$name/

build-pkg
