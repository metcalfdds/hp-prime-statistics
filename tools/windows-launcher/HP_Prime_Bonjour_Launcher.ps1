# HP Prime Connectivity Kit launcher (checks Bonjour first), version 2.
# Checks that Apple's Bonjour Service is running, starts it with Windows
# administrator consent if needed, then opens your own HP Connectivity Kit
# shortcut (.lnk). It opens the shortcut, not the program file, because the
# shortcut carries launch settings the Kit needs (opening the .exe directly
# can fail with a Qt error).
# No persistent system, network, firewall or registry settings are changed.
# From the hp-prime-statistics repository (Roger D. Metcalf); written with AI
# assistance and tested by the author on Windows, October 2026.

$ErrorActionPreference = 'Stop'
$serviceName = 'Bonjour Service'

function End-WithError([string]$message) {
    Write-Host ''
    Write-Host "ERROR: $message" -ForegroundColor Red
    Write-Host ''
    Read-Host 'Press Enter to close' | Out-Null
    exit 1
}

# 1. Check and start Bonjour only if necessary.
try {
    $bonjour = Get-Service -Name $serviceName
} catch {
    End-WithError 'Bonjour Service was not found on this computer.'
}

if ($bonjour.Status -ne 'Running') {
    Write-Host 'Bonjour is stopped. Attempting to start it...'
    try {
        $principal = [Security.Principal.WindowsPrincipal]::new(
            [Security.Principal.WindowsIdentity]::GetCurrent()
        )
        if ($principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
            Start-Service -Name $serviceName -ErrorAction Stop
        } else {
            # The only elevated action is Start-Service. HP Connectivity Kit
            # itself is launched in the user's original non-elevated session.
            $command = @'
try {
    Start-Service -Name 'Bonjour Service' -ErrorAction Stop
    (Get-Service -Name 'Bonjour Service').WaitForStatus('Running', [TimeSpan]::FromSeconds(10))
    exit 0
} catch { exit 1 }
'@
            $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($command))
            $ps = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
            $result = Start-Process -FilePath $ps -Verb RunAs -Wait -PassThru `
                -ArgumentList "-NoProfile -NonInteractive -EncodedCommand $encoded"
            if ($result.ExitCode -ne 0) {
                End-WithError 'Windows did not allow Bonjour to start.'
            }
        }
        (Get-Service -Name $serviceName).WaitForStatus('Running', [TimeSpan]::FromSeconds(10))
    } catch {
        End-WithError "Bonjour could not be started: $($_.Exception.Message)"
    }
}

if ((Get-Service -Name $serviceName).Status -ne 'Running') {
    End-WithError 'Bonjour is not running. The Connectivity Kit was not launched.'
}
Write-Host 'Bonjour is running.' -ForegroundColor Green

# 2. Find the original, known-working HP Connectivity Kit SHORTCUT.
# Windows opens the .lnk with its own launch settings (working folder etc.).
$configDir = Join-Path $env:LOCALAPPDATA 'HP_Prime_Bonjour_Launcher'
$configFile = Join-Path $configDir 'OriginalShortcut.txt'
$originalShortcut = $null

if (Test-Path -LiteralPath $configFile -PathType Leaf) {
    try {
        $candidate = (Get-Content -LiteralPath $configFile -Raw -ErrorAction Stop).Trim()
        if ($candidate -and $candidate.EndsWith('.lnk', [StringComparison]::OrdinalIgnoreCase) -and
            (Test-Path -LiteralPath $candidate -PathType Leaf)) {
            $originalShortcut = $candidate
        }
    } catch { }
}

if (-not $originalShortcut) {
    $shortcutFolders = @(
        [Environment]::GetFolderPath('CommonPrograms'),
        [Environment]::GetFolderPath('Programs'),
        [Environment]::GetFolderPath('Desktop'),
        [Environment]::GetFolderPath('CommonDesktopDirectory')
    ) | Where-Object { $_ -and (Test-Path -LiteralPath $_ -PathType Container) } | Select-Object -Unique

    $links = @(
        foreach ($folder in $shortcutFolders) {
            Get-ChildItem -LiteralPath $folder -Recurse -File -Filter '*.lnk' -ErrorAction SilentlyContinue |
                Where-Object { $_.BaseName -match '(?i)connectivity\s*kit' -and $_.BaseName -notmatch '(?i)bonjour.*launcher' }
        }
    ) | Sort-Object -Property FullName -Unique

    if ($links.Count -eq 1) {
        $originalShortcut = $links[0].FullName
    } elseif ($links.Count -gt 1) {
        Write-Host ''
        Write-Host 'I found several Connectivity Kit shortcuts. Select the one you normally use:'
        for ($i = 0; $i -lt $links.Count; $i++) {
            Write-Host ("  {0}. {1}" -f ($i + 1), $links[$i].FullName)
        }
        $selection = Read-Host 'Enter shortcut number (default 1)'
        if ([string]::IsNullOrWhiteSpace($selection)) { $selection = '1' }
        $index = 0
        if (-not [int]::TryParse($selection, [ref]$index) -or $index -lt 1 -or $index -gt $links.Count) {
            End-WithError 'Invalid shortcut selection.'
        }
        $originalShortcut = $links[$index - 1].FullName
    } else {
        Write-Host 'No HP Connectivity Kit shortcut found automatically.'
        Write-Host 'Please select the ORIGINAL working Connectivity Kit shortcut (.lnk), not an .exe.'
        try {
            Add-Type -AssemblyName System.Windows.Forms
            $dialog = New-Object System.Windows.Forms.OpenFileDialog
            $dialog.Title = 'Choose the original HP Connectivity Kit shortcut (.lnk)'
            $dialog.Filter = 'Windows shortcut (*.lnk)|*.lnk'
            $dialog.CheckFileExists = $true
            if ($shortcutFolders.Count -gt 0) { $dialog.InitialDirectory = $shortcutFolders[0] }
            if ($dialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) {
                End-WithError 'No shortcut was selected.'
            }
            $originalShortcut = $dialog.FileName
        } catch {
            End-WithError "Could not select a shortcut: $($_.Exception.Message)"
        }
    }

    try {
        New-Item -ItemType Directory -Force -Path $configDir | Out-Null
        Set-Content -LiteralPath $configFile -Encoding UTF8 -Value $originalShortcut
    } catch {
        Write-Host 'The shortcut choice could not be saved; this does not prevent launch.'
    }
}

# 3. Ask Windows to open the *original .lnk*, not its resolved .exe.
try {
    Write-Host "Opening original shortcut: $originalShortcut"
    Start-Process -FilePath $originalShortcut -ErrorAction Stop
} catch {
    End-WithError "The original shortcut could not be launched: $($_.Exception.Message)"
}
