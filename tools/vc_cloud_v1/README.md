# The Virtual Calculator in a cloud workspace (`tools/vc_cloud_v1`)

Written 15 November 2026, the evening a restarted workspace had lost the whole setup and the notes beside it. Everything needed to stand it up again is here, so that it costs ten minutes and not an evening.

## What it is for

- **Check.** The starter pack's second pass wants the files the calculator itself wrote back after Program Catalog > Edit > Check (`docs/changes/StarterPack_v5_NOTES.md`). That takes a calculator.
- **Run.** A changed program is run where the calculators' firmware runs it, and its screens are captured for the record and for the book.

Rogers-HP has the Virtual Calculator too, and it stays the place for anything a person must watch. This one is for the hours when that computer is in use, asleep or locked.

## What it is

HP's Virtual Calculator 2.4.2 (build 2026-09-09) under Wine 11.21 on an Xvfb display, driven with `xdotool`, its screen captured with ImageMagick's `import` and read with `tesseract`.

| File | What it does |
| --- | --- |
| `setup.sh INSTALLER.exe [VC]` | Installs Wine 11.21 (`winehq-devel`), `cabextract`, `msitools`, `xdotool`; takes the calculator's files out of HP's installer; patches `HPPrime.exe`; writes `env.sh`, `xvfb.sh` and `start.sh` into the folder `VC` (default `/tmp/vc`). Run as root. Run whole on 15 November 2026: its patched file equaled the one in use. |
| `patch_hpprime.py IN OUT` | The patch, with its reason at the top (below too). |
| `vcdrive.py` | The driving: keys, soft keys, taps, "wait until the screen has settled", menu picks, starting a program from the Program Catalog, captures, text reading. Its top says what a tour script gets and what was learned. |
| `check_all.py NAME...` | Checks each named program and logs what the box said. |

HP's installer and the patched program are HP's. They are fetched for the session (the installer is `HP_Prime_Virtual_Calculator_x64_2026_09_09.exe` in the author's `D:\HP-Prime`, 85,350,392 bytes) and never committed.

## Standing it up

1. Get the installer into the workspace (stage it from `D:\HP-Prime`).
2. `bash tools/vc_cloud_v1/setup.sh /path/to/the/installer.exe /tmp/vc`
3. Start `/tmp/vc/xvfb.sh` as a tracked background job. Then `. /tmp/vc/env.sh && wineboot -i`.
4. Start `/tmp/vc/start.sh` as a tracked background job. A job started with `&` inside another command is stopped when that command's reply ends, and a calculator that is stopped that way leaves a lock behind (step 6).
5. **The first start** asks four things, each answered with one click (`vcdrive.click(x, y)` on the X display):
   - HP's licence dialog: Accept, at (746, 654). It is the licence of the program the author has installed on his own computer.
   - "Slide to unlock": press at (482, 459), move right to (630, 459) in ten steps, release.
   - "Choose default language": English is highlighted; soft key 6 (OK), twice.
   - "Initial Configuration", two pages (number format, then time and theme): soft key 6 on each. These are the settings of a calculator after a reset.
6. **Always leave by Calculator > Exit** (the menu at (354, 282), its Exit at (363, 420)). The calculator writes its files back then, the checked ones among them. A calculator that was killed leaves `Documents/HP Prime/Temp/HPEmuInstance.lock`; the next start then opens a second calculator, "HP Prime_1", in a folder of its own. Remove the stale lock (and, on a first run, both calculator folders) before starting again.
7. Files go in and out through the calculator's own folder while it is closed: `$CALC`, which is `Documents/HP Prime/Calculators/Prime` under the Wine prefix.

## The window

The calculator's window stands at +320+272 on the 1280 × 1024 display, with the small skin. Its 320 × 240 screen is at (323, 339): a capture is `import -window root -crop 320x240+323+339 +repage out.png`, and a tap at the calculator's pixel (x, y) is a click at (323 + x, 339 + y). The skin's keys are in `vcdrive.KEYS`; the six soft keys are taps at y = 228 and x = 26, 80, 133, 186, 240, 293.

## The patch, and why

At start the emulator looks for a Connectivity Kit through Windows' device enumeration: WinRT `DeviceInformation.CreateWatcher`, with a filter on `System.Devices.Dnssd.Domain` and `System.Devices.Dnssd.ServiceName` and nine requested properties, eight of them `System.Devices.Dnssd.*`. Wine's property system knows 29 property names and none of the Dnssd ones (`strings -el propsys.dll | grep ^System`), so the call fails, the emulator's C++ exception goes unhandled, and the program ends with exit code 3 before any window opens. Its last line is "Filter string: ...".

Seen on 15 November 2026 with Wine 11.21 (and 11.22): with the filter alone changed, the call failed at the first requested property (`...Dnssd.Domain`); with that one changed too, at the next (`...Dnssd.FullName`). So `patch_hpprime.py` changes the filter and all nine names, each in place and at its own length:

- the filter's text becomes `System.ItemNameDisplay:="`, padded in front with spaces, so the search asks for a device named `_hpconnkit._tcp` and finds none;
- each requested name becomes `System.ItemNameDisplay`, padded with NULs. Wine reads a name as a NUL-terminated string (`dlls/windows.devices.enumeration/main.c`, `devpropcompkeys_append_names`).

Nothing else in the file changes, and the patch stops if any of the ten strings is not found exactly once (another build). The search for a Connectivity Kit then finds nothing, which is all this setup needs. (Lessons Learned v7zm to v7zv said "two strings". That could not be made to work on 15 November; ten is what it took.)

## What it does not settle

Speed (a PC is far faster than a G1), a held key, two fingers, a real finger. And see the next section.

## Key presses that go missing

On this calculator about one key press in eight did nothing on a page that waits in the fleet's `GETKEY` + `MOUSE` loop, however long the key was held. `diagnostics/KeyProbe_beta1.txt` counted it (`verify/round16/keyprobe_r16.txt`): of 60 presses each, on an idle machine, a loop of `GETKEY` alone saw 41, `GETKEY` with `MOUSE` 52, the fleet's whole idiom 50, and `WAIT(-1)` all 60; thirty digits typed at Home all arrived. So a tour must test that each press did something (`vcdrive.act`, `vcdrive.pick`) and stop when one did not (`vcdrive.must`). Whether a G1 or a G2 drops presses the same way is not known; KeyProbe on the calculators will say.
