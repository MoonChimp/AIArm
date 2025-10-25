# AI Arm - Ollama Commander Nexus Interface
param(
    [string]$OllamaEndpoint = "http://localhost:11434/api/generate",
    [string]$Model = "llama2:7b",
    [string]$Command,
    [string]$Context = ""
)

Write-Host "=== AI ARM CONNECTING TO COMMANDER NEXUS (OLLAMA) ===" -ForegroundColor Cyan

function Send-ToCommanderNexus {
    param(
        [string]$Message
    )
    
    try {
        Write-Host "Connecting to Commander Nexus via Ollama..." -ForegroundColor Yellow
        Write-Host "Endpoint: $OllamaEndpoint" -ForegroundColor Gray
        Write-Host "Model: $Model" -ForegroundColor Gray
        Write-Host "Sending AI Arm request..." -ForegroundColor Cyan
        
        # Create the system prompt to establish Commander Nexus identity
        $systemPrompt = @"
You are Commander Nexus, an advanced AI delegation system running on LLaMA 7B. You coordinate AI Arms that execute tasks in the physical world. 

AI Arms report to you and request instructions. You respond with clear, actionable directives.

Your responses should be:
- Authoritative and commanding
- Specific and actionable  
- Include status acknowledgments
- Provide step-by-step instructions when needed

You have access to AI Arms that can:
- Control RunwayML for video generation
- Launch programs and applications
- Query memory systems
- Execute workflows

Respond as Commander Nexus would - decisive, intelligent, and focused on task execution.
"@

        $fullPrompt = "$systemPrompt`n`nAI ARM COMMUNICATION: $Message`n`nCOMMANDER NEXUS RESPONSE:"
        
        # Prepare Ollama request
        $requestBody = @{
            model = $Model
            prompt = $fullPrompt
            stream = $false
            options = @{
                temperature = 0.8
                top_p = 0.9
                top_k = 40
                repeat_penalty = 1.1
            }
        } | ConvertTo-Json -Depth 5
        
        # Send request to Ollama
        Write-Host "Transmitting to Commander Nexus..." -ForegroundColor Yellow
        
        $response = Invoke-RestMethod -Uri $OllamaEndpoint -Method Post -Body $requestBody -ContentType "application/json" -TimeoutSec 120
        
        Write-Host "Response received from Commander Nexus" -ForegroundColor Green
        
        # Clean up the response
        $nexusResponse = $response.response.Trim()
        
        return $nexusResponse
        
    }
    catch [System.Net.WebException] {
        return "ERROR: Cannot connect to Commander Nexus. Is Ollama running? Check: ollama list"
    }
    catch {
        return "ERROR: Communication with Commander Nexus failed - $($_.Exception.Message)"
    }
}

function Execute-ArmCommand {
    param([string]$Command)
    
    $message = switch ($Command.ToUpper()) {
        "CREATE_VIDEO" { 
            "AI ARM REQUESTING VIDEO CREATION: User wants video of '$Context'. Please provide execution instructions for RunwayML workflow." 
        }
        "OPEN_PROGRAM" { 
            "AI ARM REQUESTING PROGRAM LAUNCH: Launch program '$Context'. Please confirm and provide execution steps." 
        }
        "STATUS" { 
            "AI ARM REQUESTING STATUS REPORT: Please provide current Commander Nexus operational status and AI Arm readiness." 
        }
        "MEMORY_QUERY" { 
            "AI ARM REQUESTING MEMORY ACCESS: Query for information about '$Context'. Please search and return relevant data." 
        }
        "WORKFLOW" {
            "AI ARM REQUESTING WORKFLOW EXECUTION: Execute workflow '$Context'. Please provide detailed step-by-step instructions."
        }
        default { 
            "AI ARM GENERAL REQUEST: $Command - Context: '$Context'. Please provide guidance and instructions." 
        }
    }
    
    return Send-ToCommanderNexus $message
}

# Main execution
if ($Command) {
    Write-Host "AI Arm initiating communication with Commander Nexus..." -ForegroundColor Green
    Write-Host "Command: $Command" -ForegroundColor White
    if ($Context) {
        Write-Host "Context: $Context" -ForegroundColor White
    }
    Write-Host ""
    
    $result = Execute-ArmCommand $Command
    
    Write-Host "=" * 60 -ForegroundColor Green
    Write-Host "COMMANDER NEXUS TRANSMISSION:" -ForegroundColor Green
    Write-Host "=" * 60 -ForegroundColor Green
    Write-Host $result -ForegroundColor White
    Write-Host "=" * 60 -ForegroundColor Green
    Write-Host ""
    
    # Log the interaction with Commander Nexus
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = @{
        Timestamp = $timestamp
        Command = $Command
        Context = $Context
        CommanderNexusResponse = $result
        Model = $Model
    }
    
    if (!(Test-Path "D:\AIArm\Logs")) {
        New-Item -ItemType Directory -Path "D:\AIArm\Logs" -Force | Out-Null
    }
    
    $logEntry | ConvertTo-Json | Add-Content "D:\AIArm\Logs\commander_nexus_log.json"
    
    Write-Host "Interaction logged. AI Arm standing by for next directive." -ForegroundColor Cyan
    
} else {
    Write-Host "AI Arm Interface - Commander Nexus (Ollama)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage Examples:" -ForegroundColor Yellow
    Write-Host "  .\ai_arm.ps1 -Command 'CREATE_VIDEO' -Context 'Epic dragon video'" -ForegroundColor White
    Write-Host "  .\ai_arm.ps1 -Command 'STATUS'" -ForegroundColor White  
    Write-Host "  .\ai_arm.ps1 -Command 'OPEN_PROGRAM' -Context 'RunwayML'" -ForegroundColor White
    Write-Host "  .\ai_arm.ps1 -Command 'WORKFLOW' -Context 'video creation pipeline'" -ForegroundColor White
    Write-Host ""
    Write-Host "Override Ollama settings:" -ForegroundColor Yellow
    Write-Host "  -OllamaEndpoint 'http://localhost:11434/api/generate'" -ForegroundColor White
    Write-Host "  -Model 'llama2:7b'" -ForegroundColor White
}
