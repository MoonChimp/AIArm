# AI Arm - Optimized Commander Nexus (16GB RAM Compatible)
param(
    [string]$Model = "commander-nexus-optimized:latest",
    [string]$Command,
    [string]$Context = ""
)

Write-Host "=== AI ARM - OPTIMIZED COMMANDER NEXUS ===" -ForegroundColor Cyan
Write-Host "Optimized for 16GB RAM - Preparing for 64GB+ upgrade" -ForegroundColor Yellow

function Send-ToCommanderNexus {
    param([string]$Message)
    
    try {
        Write-Host "Connecting to optimized Commander Nexus..." -ForegroundColor Yellow
        Write-Host "Model: $Model" -ForegroundColor Gray
        
        $requestBody = @{
            model = $Model
            prompt = $Message
            stream = $false
            options = @{
                temperature = 0.8
                top_p = 0.9
                num_ctx = 4096
                repeat_penalty = 1.1
            }
        } | ConvertTo-Json -Depth 3
        
        Write-Host "Transmitting to Commander Nexus..." -ForegroundColor Cyan
        
        $response = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -Body $requestBody -ContentType "application/json" -TimeoutSec 90
        
        Write-Host "✓ Response received from Commander Nexus" -ForegroundColor Green
        return $response.response.Trim()
        
    }
    catch [System.Net.WebException] {
        return "ERROR: Cannot connect to Commander Nexus. Is Ollama running? Check: ollama ps"
    }
    catch {
        return "ERROR: Communication failed - $($_.Exception.Message)"
    }
}

function Format-OptimizedRequest {
    param([string]$Command, [string]$Context)
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    $request = switch ($Command.ToUpper()) {
        "STATUS" { 
            "[$timestamp] AI ARM STATUS REQUEST: Provide current Commander Nexus operational status and system readiness. Include memory optimization status and AI Arm coordination capabilities." 
        }
        "CREATE_VIDEO" { 
            "[$timestamp] AI ARM VIDEO REQUEST: Execute video generation workflow for '$Context'. Provide optimized RunwayML automation steps with resource management." 
        }
        "OPEN_PROGRAM" { 
            "[$timestamp] AI ARM PROGRAM REQUEST: Launch program '$Context'. Provide efficient execution steps with system resource awareness." 
        }
        "WORKFLOW" {
            "[$timestamp] AI ARM WORKFLOW REQUEST: Execute optimized workflow for '$Context'. Provide step-by-step coordination with current system constraints."
        }
        "MEMORY_QUERY" {
            "[$timestamp] AI ARM MEMORY REQUEST: Query information about '$Context'. Access Commander Nexus memory banks efficiently."
        }
        "OPTIMIZE" {
            "[$timestamp] AI ARM OPTIMIZATION REQUEST: Analyze and optimize '$Context' for current 16GB system preparing for 64GB+ upgrade."
        }
        default { 
            "[$timestamp] AI ARM REQUEST: $Command - Context: '$Context'. Provide guidance optimized for current system capabilities." 
        }
    }
    
    return $request
}

# Main execution
if ($Command) {
    Write-Host "Current System: 16GB RAM (Upgrading to 64-96GB Tuesday)" -ForegroundColor Yellow
    Write-Host "Command: $Command" -ForegroundColor White
    if ($Context) {
        Write-Host "Context: $Context" -ForegroundColor White
    }
    Write-Host ""
    
    $formattedRequest = Format-OptimizedRequest -Command $Command -Context $Context
    $nexusResponse = Send-ToCommanderNexus -Message $formattedRequest
    
    # Display response
    Write-Host "╔" + "═" * 78 + "╗" -ForegroundColor Green
    Write-Host "║" + "COMMANDER NEXUS - OPTIMIZED RESPONSE".PadRight(78) + "║" -ForegroundColor Green
    Write-Host "╠" + "═" * 78 + "╣" -ForegroundColor Green
    Write-Host ""
    Write-Host $nexusResponse -ForegroundColor Cyan
    Write-Host ""
    Write-Host "╚" + "═" * 78 + "╝" -ForegroundColor Green
    Write-Host ""
    
    # Log interaction
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = @{
        Timestamp = $timestamp
        Model = $Model
        SystemRAM = "16GB"
        Command = $Command
        Context = $Context
        Response = $nexusResponse
        Success = -not $nexusResponse.StartsWith("ERROR")
    }
    
    if (!(Test-Path "D:\AIArm\Logs")) {
        New-Item -ItemType Directory -Path "D:\AIArm\Logs" -Force | Out-Null
    }
    
    $logEntry | ConvertTo-Json -Depth 5 | Add-Content "D:\AIArm\Logs\optimized_nexus.json"
    
    Write-Host "AI Arm ready for next directive. Awaiting Tuesday RAM upgrade for enhanced capabilities." -ForegroundColor Yellow
    
} else {
    Write-Host "AI Arm Interface - Optimized Commander Nexus" -ForegroundColor Cyan
    Write-Host "Current Configuration: 16GB RAM Compatible" -ForegroundColor Yellow
    Write-Host "Upgrade Planned: 64-96GB RAM (Tuesday)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Available Commands:" -ForegroundColor Yellow
    Write-Host "  STATUS        - System status and readiness" -ForegroundColor White
    Write-Host "  CREATE_VIDEO  - Optimized video workflows" -ForegroundColor White
    Write-Host "  OPEN_PROGRAM  - Efficient program launching" -ForegroundColor White
    Write-Host "  WORKFLOW      - Multi-step task coordination" -ForegroundColor White
    Write-Host "  OPTIMIZE      - System optimization analysis" -ForegroundColor White
    Write-Host "  MEMORY_QUERY  - Memory system access" -ForegroundColor White
    Write-Host ""
    Write-Host "Usage Examples:" -ForegroundColor Yellow
    Write-Host "  .\ai_arm_optimized.ps1 -Command 'STATUS'" -ForegroundColor White
    Write-Host "  .\ai_arm_optimized.ps1 -Command 'CREATE_VIDEO' -Context 'Dragon video'" -ForegroundColor White
    Write-Host "  .\ai_arm_optimized.ps1 -Command 'OPTIMIZE' -Context 'video workflow'" -ForegroundColor White
}
