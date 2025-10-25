@echo off
echo =====================================================================
echo                   AIARM WEB INTERFACE ONLY
echo =====================================================================
echo.

echo Starting web interface without launching additional services...
echo.

cd /D "D:\AIArm\WebInterface"

echo Checking for port availability...
set PORT=3456
netstat -ano | findstr ":%PORT%" > nul
if %ERRORLEVEL% EQU 0 (
    echo Port %PORT% is already in use. Trying alternative port 3457...
    set PORT=3457
    netstat -ano | findstr ":%PORT%" > nul
    if %ERRORLEVEL% EQU 0 (
        echo Port %PORT% is also in use. Trying alternative port 3458...
        set PORT=3458
    )
)

echo Will use port %PORT% for the web interface.
echo.

echo Starting server...
echo.
echo =====================================================================
echo     IMPORTANT: Open your browser to http://localhost:%PORT%
echo =====================================================================
echo.
echo This window must remain open while using the interface.
echo Press Ctrl+C to stop the server when you're done.
echo.

node real_server.js --port %PORT%

pause
