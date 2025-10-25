@echo off
echo Starting basic test server on port 45680...

cd /D D:\AIArm\WebInterface
node basic_server.js

echo.
echo Press any key to exit...
pause > nul
