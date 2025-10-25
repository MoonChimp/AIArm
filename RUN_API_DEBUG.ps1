# Nexus AI - API Server Debug Mode
# Run just the Flask API in foreground to see all logs

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "                    NEXUS API SERVER - DEBUG MODE" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if ANTHROPIC_API_KEY is set
$apiKey = $env:ANTHROPIC_API_KEY
if ($apiKey) {
    Write-Host "[OK] ANTHROPIC_API_KEY: " -ForegroundColor Green -NoNewline
    Write-Host "$($apiKey.Substring(0, 10))..." -ForegroundColor DarkGray
    Write-Host "[OK] Using Claude Intelligence Mode" -ForegroundColor Green
} else {
    Write-Host "[WARNING] ANTHROPIC_API_KEY not set" -ForegroundColor Yellow
    Write-Host "[INFO] Using basic Ollama mode" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To enable Claude intelligence:" -ForegroundColor Cyan
    Write-Host '  1. Get API key from: https://console.anthropic.com/settings/keys' -ForegroundColor White
    Write-Host '  2. Run: $env:ANTHROPIC_API_KEY = "your-key-here"' -ForegroundColor White
    Write-Host '  3. Restart this script' -ForegroundColor White
}
Write-Host ""

# Kill existing Python processes
Write-Host "Cleaning up..." -ForegroundColor Cyan
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Write-Host ""

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Starting Flask API Server..." -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "D:\AIArm"
python nexus_api_server.py
