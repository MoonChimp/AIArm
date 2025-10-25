@echo off
echo.
echo === Testing AIArm Improved Bridge ===
echo.

REM Set the bridge file to test
set BRIDGE_FILE=D:\AIArm\WebInterface\improved_bridge.py

REM Test input
set TEST_INPUT=Hello, this is a test message from the improved bridge test script.

echo Testing bridge with direct input...
python "%BRIDGE_FILE%" --input "%TEST_INPUT%" --agent orchestrator --user test_user
echo.
echo === Test complete ===
echo.

echo Testing bridge with JSON input...
python "%BRIDGE_FILE%" --input "{\"input\":\"This is a JSON test\",\"agent\":\"orchestrator\",\"user_id\":\"json_test_user\"}" --json
echo.
echo === Test complete ===
echo.

echo Press any key to exit...
pause >nul