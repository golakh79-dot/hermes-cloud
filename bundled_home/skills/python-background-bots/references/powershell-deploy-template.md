# PowerShell Deploy Script Template for Windows Background Bots

## Purpose
Standardized deployment pattern for dual-thread Python bots (background worker + Telegram listener) with port locking, state persistence, and Windows-native process management.

## Script Structure
```powershell
<#
.SYNOPSIS
    BotName Pro vX.Y - Deployment Script
.DESCRIPTION
    Deploys and starts BotName Pro with:
    - Port lock enforcement (LOCK_PORT)
    - Environment configuration (.env)
    - State file initialization
    - Background process management via PowerShell Job
    - Logging and monitoring setup
.NOTES
    Author: Hermes Agent
    Version: X.Y
    Inspired by: WURK Pro v2.0 deploy script
#>

param(
    [switch]$ForceRestart,
    [switch]$SkipPortCheck,
    [string]$CustomEnvPath
)

# ─── Configuration ───
$ScriptName = "BotName Pro"
$Version = "X.Y"
$BaseDir = "D:\\HERMES\\Hermes_Portable_Data\\home"
$ScriptsDir = "$BaseDir\\scripts"
$ScriptFile = "$ScriptsDir\\bot_script.py"
$LogFile = "$ScriptsDir\\bot_script.log"
$StateFile = "$BaseDir\\bot_pro_state.json"
$EnvFile = if ($CustomEnvPath) { $CustomEnvPath } else { "$BaseDir\\.env" }
$LockPort = XXXXX  # Unique per bot: WURK=59422, Twitter=59421, Polyester=59423
$PythonExe = "python.exe"

$RequiredEnvVars = @(
    "BOT_API_KEY_ID",
    "BOT_API_PRIVATE_KEY",
    "BOT_ACCOUNT_ID",
    "BOT_BOT_TOKEN",
    "ADMIN_CHAT_ID"
)

# ─── Colors ───
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan
$Gray = [ConsoleColor]::DarkGray
$White = [ConsoleColor]::White

function Write-Header { param($msg) Write-Host "`n=== $msg ===" -ForegroundColor $Cyan }
function Write-Success { param($msg) Write-Host "[OK] $msg" -ForegroundColor $Green }
function Write-ErrorMsg { param($msg) Write-Host "[ERR] $msg" -ForegroundColor $Red }
function Write-Warning { param($msg) Write-Host "[WARN] $msg" -ForegroundColor $Yellow }
function Write-Info { param($msg) Write-Host "[INFO] $msg" -ForegroundColor $Gray }
function Write-Step { param($msg) Write-Host "`n>> $msg" -ForegroundColor $White }

# ─── Kill existing instances on port + by script name ───
function Stop-ExistingInstances {
    Write-Step "Checking for existing instances on port $LockPort..."
    $netstat = netstat -ano | Select-String ":$LockPort"
    if ($netstat) {
        $pids = $netstat | ForEach-Object { $_ -replace '.*\\s+(\\d+)$', '$1' } | Sort-Object -Unique
        foreach ($pid in $pids) {
            if ($pid -ne $PID) { Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue }
        }
        Start-Sleep -Seconds 2
    }
    $procs = Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -like "*bot_script*" }
    foreach ($proc in $procs) { if ($proc.ProcessId -ne $PID) { Stop-Process -Id $proc.ProcessId -Force -ErrorAction SilentlyContinue } }
}

# ─── Setup .env with template ───
function Setup-Environment {
    if (Test-Path $EnvFile) { Copy-Item $EnvFile "$EnvFile.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')" -Force }
    # Build template with existing values preserved
    # ... write template with placeholders for required vars
    # Return $true if all required vars present, $false if missing
}

# ─── Check Python deps ───
function Check-PythonEnvironment {
    # Verify python.exe, polyester-sdk, python-telegram-bot, etc.
}

# ─── Syntax check ───
function Verify-Script {
    $result = & $PythonExe -m py_compile $ScriptFile 2>&1
    return $LASTEXITCODE -eq 0
}

# ─── Initialize state JSON ───
function Initialize-State {
    if (-not (Test-Path $StateFile)) {
        $initialState = @{ mode="active"; cycle_count=0; ...; started_at=(Get-Date).ToString("o") }
        $initialState | ConvertTo-Json -Depth 5 | Set-Content $StateFile -Encoding UTF8
    }
}

# ─── Start as PowerShell Job with Tee-Object logging ───
function Start-Bot {
    Set-Location $ScriptsDir
    $job = Start-Job -ScriptBlock {
        param($scriptFile, $logFile)
        & $env:PythonExe $scriptFile 2>&1 | Tee-Object -FilePath $logFile -Append
    } -ArgumentList $ScriptFile, $LogFile -Name "BotName"
    Start-Sleep -Seconds 3
    # Verify: job state, port lock, process, log tail
}

# ─── Show status ───
function Show-Status {
    # Print summary, running processes, port status, log tail
}

# ─── MAIN ───
Stop-ExistingInstances (unless -SkipPortCheck)
$envReady = Setup-Environment
if (-not $envReady -and -not $ForceRestart) { exit 1 }
Check-PythonEnvironment
Verify-Script
Initialize-State
$started = Start-Bot
Show-Status
exit if (!$started)
```

## Per-Bot Customization Points
| Variable | WURK Pro | Twitter Hub | Polyester Pro |
|---|---|---|---|
| `LockPort` | 59422 | 59421 | 59423 |
| `ScriptFile` | `wurk_agent.py` | `twitter_telegram_bot_panel.py` | `polyester_pro_trader.py` |
| `StateFile` | `wurk_pro_state.json` | `twitter_pro_state.json` | `polyester_pro_state.json` |
| `RequiredEnvVars` | `WURK_BOT_TOKEN`, `ADMIN_CHAT_ID` | `TWITTER_BOT_TOKEN`, `ADMIN_CHAT_ID` | `POLYESTER_BOT_TOKEN`, `ADMIN_CHAT_ID`, `POLYESTER_API_*` |
| `Bot Name` | `@secondxHermesbot` | `@Hermixxbot` | `@PolyesterProBot` |

## Critical Rules
1. **Unique port per bot** — hardcode in script + deploy script
2. **PowerShell Job + Tee-Object** — not `pythonw.exe` (allows log capture)
3. **Validate token via `getMe`** before marking deploy success
4. **Wait 3-5s then verify** port lock + process + log markers
5. **Backup .env and state** before overwrite
6. **Syntax check** with `python -m py_compile` before start
7. **Kill by port AND script name** — prevents orphaned processes

## Post-Deploy Monitoring
```powershell
# Live log tail
Get-Content $LogFile -Wait -Tail 30

# Stop bot
Stop-Job -Name "BotName"

# Status
Get-Job -Name "BotName"
```

## Integration with `python-background-bots` Skill
This template implements the deployment pattern described in `python-background-bots` SKILL.md:
- Instance Lock (port bind at module import)
- Startup Token Validation (`bot.getMe()`)
- Webhook Cleanup (`deleteWebhook`)
- Graceful Error Handling (try/except around `asyncio.gather`)
- Background Survival Verification (port + process + log check)
- Log Spam Prevention (`consecutive_zero_cycles` in state)

---
*Generate new deploy scripts by copying this template and filling in the customization points above.*