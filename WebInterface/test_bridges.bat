@echo off
echo Testing bridge connectivity...

echo.
echo Testing Surface Bridge (improved_bridge.py)...
echo {"input": "test", "agent": "orchestrator", "user_id": "test_user"} | python improved_bridge.py
if %ERRORLEVEL% NEQ 0 (
    echo Surface Bridge test failed with error code %ERRORLEVEL%
) else (
    echo Surface Bridge test completed
)

echo.
echo Testing Deep Bridge (ollama_bridge.py)...
echo {"input": "test", "agent": "orchestrator", "user_id": "test_user"} | python ollama_bridge.py
if %ERRORLEVEL% NEQ 0 (
    echo Deep Bridge test failed with error code %ERRORLEVEL%
) else (
    echo Deep Bridge test completed
)

echo.
echo Bridge tests completed
pause