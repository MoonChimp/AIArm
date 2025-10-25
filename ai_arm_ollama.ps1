# AI Arm - Ollama Commander Nexus Interface
param(
    [string]$Model = "commander-nexus-optimized:latest",
    [string]$Command,
    [string]$Context = ""
)

Write-Host "=== AI ARM - COMMANDER NEXUS INTERFACE ===" -ForegroundColor Cyan

function Send-ToCommanderNexus {
    param([string]$Message)
    
    try {
        Write-Host "Connecting to Commander Nexus..." -ForegroundColor Yellow
        
        $requestBody = @{
            model = $Model
            prompt = $Message
            stream = $false
            options = @{
                temperature = 0.8
                top_p = 0.9
                num_ctx = 4096
            }
        } | ConvertTo-Json -Depth 3
        
        $response = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $requestBody -ContentType "application/json" -TimeoutSec 90
        
        Write-Host "Response received from Commander Nexus" -ForegroundColor Green
        return $response.response.Trim()
        
    }
    catch {
        return "ERROR: Could not connect to Commander Nexus - $($_.Exception.Message)"
    }
}

if ($Command) {
    $timestamp = Get-Date -Format "HH:mm:ss"
    $request = "[$timestamp] AI ARM REQUEST: $Command"
    if ($Context) { $request += " - Context: $Context" }
    
    Write-Host "Sending: $request" -ForegroundColor Cyan
    $result = Send-ToCommanderNexus $request
    
    Write-Host ""
    Write-Host "COMMANDER NEXUS RESPONSE:" -ForegroundColor Green
    Write-Host $result -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "Usage: .\ai_arm_ollama.ps1 -Command 'STATUS' -Context 'optional context'" -ForegroundColor Yellow
}