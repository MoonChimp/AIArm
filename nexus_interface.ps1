# Commander Nexus Direct Interface
param(
    [Parameter(Mandatory=$true)]
    [string]$Command,
    
    [Parameter(Mandatory=$false)]
    [string]$Config = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Prompt = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Output = "D:\AIArm\Reports\latest_status.txt"
)

# Load the main framework
try {
    . "D:\AIArm\ai_arm_framework.ps1"
}
catch {
    Write-Host "ERROR: Could not load AI Arm Framework" -ForegroundColor Red
    exit 1
}

function Execute-NexusCommand {
    param($Command, $Config, $Prompt)
    
    try {
        switch ($Command.ToUpper()) {
            "CREATE_VIDEO" {
                $params = @{
                    Prompt = if ($Prompt) { $Prompt } else { "Create a short video" }
                    OutputPath = "D:\Videos\output_$(Get-Date -Format 'yyyyMMdd_HHmmss').mp4"
                    Timeout = 1800
                }
                return Start-CommanderNexusTask -TaskType "CreateVideo" -Parameters $params
            }
            
            "OPEN_PROGRAM" {
                $params = @{
                    ProgramName = if ($Prompt) { $Prompt } else { "notepad" }
                    Arguments = ""
                }
                return Start-CommanderNexusTask -TaskType "OpenProgram" -Parameters $params
            }
            
            "STATUS" {
                return Get-ArmStatus
            }
            
            default {
                return "Command acknowledged: $Command - System operational"
            }
        }
    }
    catch {
        return "ERROR: $($_.Exception.Message)"
    }
}

$result = Execute-NexusCommand -Command $Command -Config $Config -Prompt $Prompt

# Ensure output directory exists
$outputDir = Split-Path $Output -Parent
if ($outputDir -and !(Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# Write result
if ($result) {
    $result | Out-File -FilePath $Output -Encoding UTF8 -Force
}

Write-Host "=== RESULT FOR COMMANDER NEXUS ===" -ForegroundColor Cyan
Write-Host $result -ForegroundColor White
Write-Host "=== END RESULT ===" -ForegroundColor Cyan