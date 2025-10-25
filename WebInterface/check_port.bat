@echo off
echo Checking for processes using port 45678...
netstat -ano | findstr :45678
echo.

echo Checking if winston module is installed...
cd /D D:\AIArm\WebInterface
if exist "node_modules\winston" (
  echo Winston module found.
) else (
  echo Winston module not found. Installing...
  npm install winston
)

echo Checking for other required modules...
if not exist "node_modules\express" (
  echo Express module not found. Installing...
  npm install express
)

if not exist "node_modules\cors" (
  echo CORS module not found. Installing...
  npm install cors
)

echo.
echo Module check complete.
echo.
echo Press any key to exit...
pause > nul
