# Commander Nexus Web Bridge Service
param([switch]$Start, [switch]$Stop, [switch]$Status)

$servicePath = "D:\AIArm\WebInterface"
$commandFile = "$servicePath\command.json"
$responseFile = "$servicePath\response.json"
$statusFile = "$servicePath\service_status.txt"

if (!(Test-Path $servicePath)) {
    New-Item -ItemType Directory -Path $servicePath -Force | Out-Null
}

function Start-WebBridge {
    Write-Host "Starting Commander Nexus Web Bridge..." -ForegroundColor Green
    
    # Initialize files
    @{status = "ready"; timestamp = Get-Date} | ConvertTo-Json | Out-File $responseFile -Encoding UTF8
    "RUNNING" | Out-File $statusFile -Encoding UTF8
    
    Write-Host "Web Bridge is now monitoring for commands..." -ForegroundColor Cyan
    Write-Host "Command file: $commandFile" -ForegroundColor Yellow
    Write-Host "Response file: $responseFile" -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Red
    
    $lastCommandTime = Get-Date
    
    while ($true) {
        try {
            if (Test-Path $commandFile) {
                $fileInfo = Get-Item $commandFile
                
                # Check if command file has been updated
                if ($fileInfo.LastWriteTime -gt $lastCommandTime) {
                    $lastCommandTime = $fileInfo.LastWriteTime
                    
                    # Read and process command
                    $commandData = Get-Content $commandFile -Raw | ConvertFrom-Json
                    
                    Write-Host "Processing command: $($commandData.command)" -ForegroundColor Cyan
                    
                    # Execute the command via nexus_command.bat
                    $tempOutput = "D:\AIArm\temp_output.txt"
                    
                    if ($commandData.prompt) {
                        $processArgs = @($commandData.command, '""', $commandData.prompt)
                    } else {
                        $processArgs = @($commandData.command)
                    }
                    
                    # Execute command
                    $process = Start-Process -FilePath "D:\AIArm\nexus_command.bat" -ArgumentList $processArgs -Wait -PassThru -RedirectStandardOutput $tempOutput -NoNewWindow
                    
                    # Read the output
                    $output = ""
                    if (Test-Path $tempOutput) {
                        $output = Get-Content $tempOutput -Raw
                        Remove-Item $tempOutput -Force -ErrorAction SilentlyContinue
                    }
                    
                    # Create response
                    $response = @{
                        commandId = $commandData.id
                        status = if ($process.ExitCode -eq 0) { "success" } else { "error" }
                        output = $output
                        timestamp = Get-Date
                        processed = $true
                    }
                    
                    # Write response
                    $response | ConvertTo-Json -Depth 5 | Out-File $responseFile -Encoding UTF8
                    
                    Write-Host "Command completed. Response written." -ForegroundColor Green
                }
            }
            
            Start-Sleep -Milliseconds 500
        }
        catch {
            Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
}

function Stop-WebBridge {
    "STOPPED" | Out-File $statusFile -Encoding UTF8
    Write-Host "Web Bridge stopped." -ForegroundColor Red
}

function Get-WebBridgeStatus {
    if (Test-Path $statusFile) {
        $status = Get-Content $statusFile -Raw
        Write-Host "Web Bridge Status: $status" -ForegroundColor Cyan
    } else {
        Write-Host "Web Bridge Status: NOT RUNNING" -ForegroundColor Red
    }
}

# Handle parameters
if ($Start) {
    Start-WebBridge
} elseif ($Stop) {
    Stop-WebBridge
} elseif ($Status) {
    Get-WebBridgeStatus
} else {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\web_bridge.ps1 -Start   # Start the web bridge service" -ForegroundColor White
    Write-Host "  .\web_bridge.ps1 -Stop    # Stop the web bridge service" -ForegroundColor White
    Write-Host "  .\web_bridge.ps1 -Status  # Check service status" -ForegroundColor White
}
