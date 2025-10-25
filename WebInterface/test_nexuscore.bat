@echo off
echo Testing NexusCore Functionality...
echo.

echo 1. Testing test file creation...
curl -s http://localhost:45678/api/nexuscore/test-file
echo.
echo.

echo 2. Testing directory listing...
curl -s -X POST -H "Content-Type: application/json" -d "{\"operation\":\"listDirectory\",\"path\":\"D:\\AIArm\\Test\"}" http://localhost:45678/api/nexuscore
echo.
echo.

echo 3. Testing file read operation...
curl -s -X POST -H "Content-Type: application/json" -d "{\"operation\":\"readFile\",\"path\":\"D:\\AIArm\\WebInterface\\nexuscore.js\"}" http://localhost:45678/api/nexuscore
echo.
echo.

echo 4. Testing administrative capabilities detection...
curl -s -X POST -H "Content-Type: application/json" -d "{\"input\":\"Can you help me with some file system operations?\"}" http://localhost:45678/api/process
echo.
echo.

echo NexusCore tests complete!
pause