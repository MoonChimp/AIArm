# Nexus AI - Debug Launcher
# Run both servers in PowerShell for easy monitoring

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "                          NEXUS AI - DEBUG MODE" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if ANTHROPIC_API_KEY is set
$apiKey = $env:ANTHROPIC_API_KEY
if ($apiKey) {
    Write-Host "[OK] ANTHROPIC_API_KEY is set - Using Claude Intelligence" -ForegroundColor Green
} else {
    Write-Host "[WARNING] ANTHROPIC_API_KEY not set - Using basic Ollama mode" -ForegroundColor Yellow
    Write-Host "To enable full Claude intelligence, set your API key:" -ForegroundColor Yellow
    Write-Host '  $env:ANTHROPIC_API_KEY = "your-key-here"' -ForegroundColor Yellow
}
Write-Host ""

# Check Ollama
Write-Host "Checking Ollama..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "[OK] Ollama is running" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Ollama not running - some features may be limited" -ForegroundColor Yellow
}
Write-Host ""

# Kill any existing Python processes
Write-Host "Cleaning up existing processes..." -ForegroundColor Cyan
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Write-Host "[OK] Cleanup complete" -ForegroundColor Green
Write-Host ""

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Starting Servers..." -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Start Flask API Server
Write-Host "[1/2] Starting Flask API Server (Backend)..." -ForegroundColor Cyan
$apiJob = Start-Job -ScriptBlock {
    Set-Location "D:\AIArm"
    python nexus_api_server.py
}
Start-Sleep -Seconds 3

# Check if API started
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/status" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "[OK] Flask API running on http://localhost:5000" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Flask API failed to start" -ForegroundColor Red
    Receive-Job $apiJob
    exit 1
}
Write-Host ""

# Start UI Server
Write-Host "[2/2] Starting UI Server (Frontend)..." -ForegroundColor Cyan
$uiJob = Start-Job -ScriptBlock {
    Set-Location "D:\AIArm"
    python serve_ui.py
}
Start-Sleep -Seconds 2

# Check if UI started
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3002" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "[OK] UI Server running on http://localhost:3002" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] UI Server failed to start" -ForegroundColor Red
    Receive-Job $uiJob
    exit 1
}
Write-Host ""

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "                       NEXUS AI IS NOW RUNNING!" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Frontend (UI):  http://localhost:3002" -ForegroundColor White
Write-Host "  Backend (API):  http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "  Opening browser..." -ForegroundColor Cyan
Start-Process "http://localhost:3002"
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "MONITORING MODE - Showing live server output" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop all servers and exit" -ForegroundColor Yellow
Write-Host ""
Write-Host "--------------------------------------------------------------------------------" -ForegroundColor DarkGray

# Monitor both jobs and show output
try {
    while ($true) {
        # Show API output
        $apiOutput = Receive-Job $apiJob -ErrorAction SilentlyContinue
        if ($apiOutput) {
            Write-Host "[API] " -ForegroundColor Cyan -NoNewline
            Write-Host $apiOutput
        }

        # Show UI output
        $uiOutput = Receive-Job $uiJob -ErrorAction SilentlyContinue
        if ($uiOutput) {
            Write-Host "[UI] " -ForegroundColor Magenta -NoNewline
            Write-Host $uiOutput
        }

        Start-Sleep -Milliseconds 100
    }
} finally {
    Write-Host ""
    Write-Host "Shutting down servers..." -ForegroundColor Yellow
    Stop-Job $apiJob, $uiJob -ErrorAction SilentlyContinue
    Remove-Job $apiJob, $uiJob -Force -ErrorAction SilentlyContinue
    Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Servers stopped" -ForegroundColor Green
}
