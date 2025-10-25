@echo off
echo =====================================================================
echo     QUICK HRM BRIDGE TEST - VERIFY CONCURRENT OPERATION
echo =====================================================================
echo.

echo Testing Surface Bridge (improved_bridge.py)...
echo Input: "Tell me about artificial intelligence"
echo.
python improved_bridge.py --input "Tell me about artificial intelligence" --agent orchestrator --user test_user
echo.
echo -----------------------------------------------------------------------
echo.

echo Testing Deep Bridge (ollama_bridge.py)...
echo Input: "Tell me about artificial intelligence"
echo.
python ollama_bridge.py --input "Tell me about artificial intelligence" --agent orchestrator --user test_user
echo.
echo -----------------------------------------------------------------------
echo.

echo Testing Concurrent Server API...
echo.
curl -X POST -H "Content-Type: application/json" -d "{\"input\": \"Tell me about artificial intelligence\", \"activeAgent\": \"orchestrator\", \"userId\": \"test_user\"}" http://localhost:45678/api/process
echo.
echo.
echo =====================================================================
echo     TEST COMPLETE
echo =====================================================================
echo.
echo If you see three different responses above, the HRM system is working correctly:
echo 1. Surface Bridge response (structured)
echo 2. Deep Bridge response (reasoning-focused)
echo 3. Combined response from the concurrent server
echo.
pause
