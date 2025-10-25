@echo off
echo.
echo === AIArm HRM Diagnostic Tool ===
echo.

REM Create log file for diagnostic results
set DIAGNOSTIC_LOG=D:\AIArm\WebInterface\Logs\diagnostic_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
set DIAGNOSTIC_LOG=%DIAGNOSTIC_LOG: =0%

echo Running diagnostics at %date% %time% > "%DIAGNOSTIC_LOG%"
echo ======================================== >> "%DIAGNOSTIC_LOG%"
echo. >> "%DIAGNOSTIC_LOG%"

echo Running system diagnostics...

REM Check server process
echo Checking server process... >> "%DIAGNOSTIC_LOG%"
tasklist /FI "IMAGENAME eq node.exe" >> "%DIAGNOSTIC_LOG%"

REM Check port usage
echo. >> "%DIAGNOSTIC_LOG%"
echo Checking port usage... >> "%DIAGNOSTIC_LOG%"
netstat -ano | findstr "45678 11434" >> "%DIAGNOSTIC_LOG%"

REM Check file structure
echo. >> "%DIAGNOSTIC_LOG%"
echo Checking file structure... >> "%DIAGNOSTIC_LOG%"
echo Main server file: >> "%DIAGNOSTIC_LOG%"
if exist "D:\AIArm\WebInterface\concurrent_server.js" (
  echo - concurrent_server.js exists >> "%DIAGNOSTIC_LOG%"
  echo - Size: >> "%DIAGNOSTIC_LOG%"
  dir "D:\AIArm\WebInterface\concurrent_server.js" | findstr /B /C:"  " >> "%DIAGNOSTIC_LOG%"
) else (
  echo - concurrent_server.js NOT FOUND >> "%DIAGNOSTIC_LOG%"
)

echo. >> "%DIAGNOSTIC_LOG%"
echo Bridge files: >> "%DIAGNOSTIC_LOG%"
if exist "D:\AIArm\WebInterface\improved_bridge.py" (
  echo - improved_bridge.py exists >> "%DIAGNOSTIC_LOG%"
  echo - Size: >> "%DIAGNOSTIC_LOG%"
  dir "D:\AIArm\WebInterface\improved_bridge.py" | findstr /B /C:"  " >> "%DIAGNOSTIC_LOG%"
) else (
  echo - improved_bridge.py NOT FOUND >> "%DIAGNOSTIC_LOG%"
)

if exist "D:\AIArm\WebInterface\ollama_bridge.py" (
  echo - ollama_bridge.py exists >> "%DIAGNOSTIC_LOG%"
  echo - Size: >> "%DIAGNOSTIC_LOG%"
  dir "D:\AIArm\WebInterface\ollama_bridge.py" | findstr /B /C:"  " >> "%DIAGNOSTIC_LOG%"
) else (
  echo - ollama_bridge.py NOT FOUND >> "%DIAGNOSTIC_LOG%"
)

REM Check for config file
echo. >> "%DIAGNOSTIC_LOG%"
echo Config files: >> "%DIAGNOSTIC_LOG%"
if exist "D:\AIArm\WebInterface\config.js" (
  echo - config.js exists >> "%DIAGNOSTIC_LOG%"
) else (
  echo - config.js NOT FOUND >> "%DIAGNOSTIC_LOG%"
)

if exist "D:\AIArm\WebInterface\config.json" (
  echo - config.json exists >> "%DIAGNOSTIC_LOG%"
  echo - Contents: >> "%DIAGNOSTIC_LOG%"
  type "D:\AIArm\WebInterface\config.json" >> "%DIAGNOSTIC_LOG%"
) else (
  echo - config.json NOT FOUND >> "%DIAGNOSTIC_LOG%"
)

REM Check for Python and Node
echo. >> "%DIAGNOSTIC_LOG%"
echo Checking environment: >> "%DIAGNOSTIC_LOG%"
echo - Python version: >> "%DIAGNOSTIC_LOG%"
python --version >> "%DIAGNOSTIC_LOG%" 2>&1
echo - Node version: >> "%DIAGNOSTIC_LOG%"
node --version >> "%DIAGNOSTIC_LOG%" 2>&1

REM Check logs directory
echo. >> "%DIAGNOSTIC_LOG%"
echo Checking logs: >> "%DIAGNOSTIC_LOG%"
if exist "D:\AIArm\WebInterface\Logs" (
  echo - Logs directory exists >> "%DIAGNOSTIC_LOG%"
  echo - Latest log files: >> "%DIAGNOSTIC_LOG%"
  dir "D:\AIArm\WebInterface\Logs" /O-D /B >> "%DIAGNOSTIC_LOG%"
  
  REM Check for errors in the most recent log file
  echo. >> "%DIAGNOSTIC_LOG%"
  echo Checking most recent logs for errors: >> "%DIAGNOSTIC_LOG%"
  for /F "delims=" %%i in ('dir "D:\AIArm\WebInterface\Logs\server*.log" /B /O-D') do (
    echo - Errors from %%i: >> "%DIAGNOSTIC_LOG%"
    findstr /I "error exception failed" "D:\AIArm\WebInterface\Logs\%%i" >> "%DIAGNOSTIC_LOG%"
    goto :log_check_done
  )
  :log_check_done
) else (
  echo - Logs directory NOT FOUND >> "%DIAGNOSTIC_LOG%"
)

REM Check service status file
echo. >> "%DIAGNOSTIC_LOG%"
echo Checking service status: >> "%DIAGNOSTIC_LOG%"
if exist "D:\AIArm\WebInterface\service_status.txt" (
  echo - service_status.txt exists >> "%DIAGNOSTIC_LOG%"
  echo - Contents: >> "%DIAGNOSTIC_LOG%"
  type "D:\AIArm\WebInterface\service_status.txt" >> "%DIAGNOSTIC_LOG%"
) else (
  echo - service_status.txt NOT FOUND >> "%DIAGNOSTIC_LOG%"
)

REM Check enhanced_orchestrator.py
echo. >> "%DIAGNOSTIC_LOG%"
echo Checking orchestrator: >> "%DIAGNOSTIC_LOG%"
if exist "D:\AIArm\WebInterface\enhanced_orchestrator.py" (
  echo - enhanced_orchestrator.py exists >> "%DIAGNOSTIC_LOG%"
) else (
  echo - enhanced_orchestrator.py NOT FOUND >> "%DIAGNOSTIC_LOG%"
)

REM Try a simple test of improved_bridge.py
echo. >> "%DIAGNOSTIC_LOG%"
echo Testing improved_bridge.py: >> "%DIAGNOSTIC_LOG%"
if exist "D:\AIArm\WebInterface\improved_bridge.py" (
  echo - Running test... >> "%DIAGNOSTIC_LOG%"
  python "D:\AIArm\WebInterface\improved_bridge.py" --input "This is a diagnostic test" --agent diagnostic --user diagnostic_test >> "%DIAGNOSTIC_LOG%" 2>&1
) else (
  echo - Cannot test: improved_bridge.py NOT FOUND >> "%DIAGNOSTIC_LOG%"
)

REM Test with JSON input
echo. >> "%DIAGNOSTIC_LOG%"
echo Testing improved_bridge.py with JSON input: >> "%DIAGNOSTIC_LOG%"
if exist "D:\AIArm\WebInterface\improved_bridge.py" (
  echo - Running JSON input test... >> "%DIAGNOSTIC_LOG%"
  python "D:\AIArm\WebInterface\improved_bridge.py" --input "{\"input\":\"This is a JSON diagnostic test\",\"agent\":\"diagnostic\",\"user_id\":\"json_diagnostic_test\"}" --json >> "%DIAGNOSTIC_LOG%" 2>&1
) else (
  echo - Cannot test: improved_bridge.py NOT FOUND >> "%DIAGNOSTIC_LOG%"
)

REM Make an API call to the server
echo. >> "%DIAGNOSTIC_LOG%"
echo Testing API: >> "%DIAGNOSTIC_LOG%"
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:45678/api/status' -Method 'GET'; $responseJson = ConvertTo-Json $response -Depth 10; $responseJson } catch { Write-Output \"API test failed: $_\" }" >> "%DIAGNOSTIC_LOG%"

echo Diagnostic complete. Results saved to:
echo %DIAGNOSTIC_LOG%
echo.

REM Offer to view the log
echo Would you like to view the diagnostic log? (Y/N)
choice /C YN /M "View log"
if %ERRORLEVEL% EQU 1 (
  notepad "%DIAGNOSTIC_LOG%"
)

echo.
echo Press any key to exit...
pause >nul