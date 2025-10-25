@echo off
echo ============================================================
echo      Installing Electron Dependencies for NexusAI
echo ============================================================
echo.
echo This will install all required packages for the standalone app
echo.

cd /d "%~dp0"

echo [1/3] Installing Node.js dependencies...
npm install

if errorlevel 1 (
    echo ERROR: Failed to install Node.js dependencies
    echo Please make sure Node.js is installed
    pause
    exit /b 1
)

echo.
echo [2/3] Installing Python dependencies...
pip install flask flask-cors requests

if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    echo Please make sure Python is installed
    pause
    exit /b 1
)

echo.
echo [3/3] Installing build tools...
npm install -g electron electron-builder

if errorlevel 1 (
    echo WARNING: Could not install global Electron tools
    echo You may need to run as administrator
    echo.
) else (
    echo [SUCCESS] Global tools installed
)

echo.
echo ============================================================
echo      Installation Complete!
echo ============================================================
echo.
echo You can now build the standalone app with:
echo   npm run build:win    (for Windows installer)
echo   npm run build:mac    (for macOS package)
echo   npm run build:linux  (for Linux package)
echo.
echo Or run in development mode:
echo   npm start
echo.
echo Press any key to continue...
pause >nul
