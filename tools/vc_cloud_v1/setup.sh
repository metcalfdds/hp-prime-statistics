#!/bin/bash
# setup.sh INSTALLER.exe [VC=/tmp/vc] -- the HP Prime Virtual Calculator in a cloud workspace (Ubuntu 24.04), about ten minutes.
#   INSTALLER.exe   HP's own HP_Prime_Virtual_Calculator_x64_2026_09_09.exe (version 2.4.2), from the author's D:\HP-Prime.
#                   It is HP's program: it is fetched for the session and never committed.
# Run as root.  See README.md beside this file for what each step is for and what was seen on 15 Nov 2026.
set -e
INST="$1"; VC="${2:-/tmp/vc}"; HERE="$(cd "$(dirname "$0")" && pwd)"
[ -f "$INST" ] || { echo "setup.sh: the installer is needed"; exit 1; }
export DEBIAN_FRONTEND=noninteractive
dpkg --add-architecture i386
mkdir -pm755 /etc/apt/keyrings
curl -sS -o /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key
curl -sS -o /etc/apt/sources.list.d/winehq-noble.sources https://dl.winehq.org/wine-builds/ubuntu/dists/noble/winehq-noble.sources
apt-get update -q | tail -2
# Wine 11.21 is the version every Check and run of 15 Nov 2026 was made on (Ubuntu's own Wine 9.0 fails)
apt-get install -y -q --install-recommends winehq-devel=11.21~noble-1 wine-devel=11.21~noble-1 wine-devel-amd64=11.21~noble-1 wine-devel-i386:i386=11.21~noble-1 | tail -2
apt-get install -y -q cabextract msitools xdotool x11-utils imagemagick tesseract-ocr xvfb | tail -2
mkdir -p "$VC/x1" "$VC/msi" "$VC/tmp" "$VC/checks"
( cd "$VC/x1" && cabextract -q "$INST" )                 # a WiX bundle: a0 a runtime, a1 Apple's Bonjour, a2 the calculator
( cd "$VC/msi" && msiextract ../x1/a2 > ../msiextract.log )
rm -rf "$VC/app"; cp -r "$VC/msi/HP/HP Prime Virtual Calculator" "$VC/app"
cp "$VC/app/HPPrime.exe" "$VC/app/HPPrime.exe.orig"
python3 "$HERE/patch_hpprime.py" "$VC/app/HPPrime.exe.orig" "$VC/app/HPPrime.exe"
cat > "$VC/env.sh" <<EOT
export VC=$VC
export WINEPREFIX=$VC/prefix
export WINEARCH=win64
export DISPLAY=:99
export WINEDEBUG=-all
export WINEDLLOVERRIDES="mscoree,mshtml="
export APP=$VC/app
export CALC="$VC/prefix/drive_c/users/root/Documents/HP Prime/Calculators/Prime"
EOT
printf '#!/bin/bash\n# Xvfb for the calculator: run it as a tracked background job\nexec Xvfb :99 -screen 0 1280x1024x24 -nolisten tcp\n' > "$VC/xvfb.sh"
printf '#!/bin/bash\n# the calculator: run it as a tracked background job; leave it by Calculator > Exit so that its files are written back\n. %s/env.sh\ncd "$APP" && exec wine HPPrime.exe\n' "$VC" > "$VC/start.sh"
chmod +x "$VC/xvfb.sh" "$VC/start.sh"
echo "setup.sh: done.  Next: $VC/xvfb.sh (background), then  . $VC/env.sh && wineboot -i  , then $VC/start.sh (background); README.md has the first start."
