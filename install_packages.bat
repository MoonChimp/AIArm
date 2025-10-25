@echo off
echo =====================================================================
echo            AIArm Package Installer
echo =====================================================================
echo.

echo Installing all required Node.js packages...
cd /D "D:\AIArm\WebInterface"
echo Installing express, cors, and body-parser...
call npm install express cors body-parser --silent

echo.
echo All packages installed successfully!
echo.
echo You can now run the final launcher:
echo D:\AIArm\final_launcher.bat
echo.

pause
