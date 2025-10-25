@echo off
title Nexus AI - FileSystem Test
echo Testing Nexus AI FileSystem operations...
echo.

echo Testing connection to server...
curl -s http://localhost:45678/api/status
if %errorlevel% neq 0 (
    echo ERROR: Server is not running. Please start the server first with start_nexus_fs.bat
    pause
    exit /b 1
)

echo.
echo Testing read operation...
curl -s -X POST -H "Content-Type: application/json" -d "{\"operation\":\"read_file\",\"path\":\"D:/AIArm/WebInterface/test_nexus_fs.txt\"}" http://localhost:45678/api/filesystem
echo.

echo.
echo Testing list directory operation...
curl -s -X POST -H "Content-Type: application/json" -d "{\"operation\":\"list_directory\",\"path\":\"D:/AIArm/WebInterface\"}" http://localhost:45678/api/filesystem
echo.

echo.
echo Testing file info operation...
curl -s -X POST -H "Content-Type: application/json" -d "{\"operation\":\"get_file_info\",\"path\":\"D:/AIArm/WebInterface/test_nexus_fs.txt\"}" http://localhost:45678/api/filesystem
echo.

echo.
echo All tests completed.
echo.
pause