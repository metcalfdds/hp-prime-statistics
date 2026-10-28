# HP Connectivity Kit launcher for Windows (checks Bonjour first)

On some Windows computers the HP Connectivity Kit does not find the calculator, or misbehaves, unless Apple's **Bonjour Service** is running, and Bonjour is sometimes stopped. This small launcher checks Bonjour, starts it if needed, then opens the Connectivity Kit the way you normally do.

## What is in this folder

- `Start_HP_Prime.cmd`: the file you double-click.
- `HP_Prime_Bonjour_Launcher.ps1`: the PowerShell script it runs. Keep the two files in the same folder.

## Installing

1. Copy both files into a folder of their own.
2. Double-click `Start_HP_Prime.cmd`.
3. If Bonjour is stopped, Windows asks for administrator approval to start it. Approve it.
4. The launcher looks for your HP Connectivity Kit shortcut (`.lnk`) in the Start menu and on the desktop.
   - If it finds one, it uses it.
   - If it finds several, it lists them and asks which one you normally use.
   - If it finds none, it asks you to browse to the shortcut you normally use to start the Kit (a `.lnk`, not the `.exe`).
5. The Connectivity Kit opens, just as if you had clicked its own shortcut.
6. To make it handy: right-click `Start_HP_Prime.cmd`, choose **Show more options → Send to → Desktop (create shortcut)**.

## Good to know

- **Why a shortcut and not the program file?** The Kit's own shortcut carries launch settings. Opening the `.exe` directly can fail with a Qt error, so the launcher always opens your shortcut.
- **What it remembers:** the shortcut you chose, in `%LOCALAPPDATA%\HP_Prime_Bonjour_Launcher\OriginalShortcut.txt`. To choose again, delete that file and run the launcher.
- **What it changes:** nothing permanent. No registry, firewall, network or service-startup settings. Administrator approval is asked for only when Bonjour has to be started, and the Kit itself runs as you, not as administrator.
- **What it cannot do:** start Bonjour where a computer's management policy forbids it, or help if Bonjour is not installed. (Bonjour comes with Apple software such as iTunes, or as Apple's "Bonjour Print Services" download.)
- `Start_HP_Prime.cmd` runs the script with `-ExecutionPolicy Bypass` for that one run, so Windows' default script policy does not block it. Read the script first if you prefer; it is short and commented.

Windows only. Tested by the author on Windows, October 2026. Written with AI assistance. Free for educational and personal use, like the rest of this repository.
