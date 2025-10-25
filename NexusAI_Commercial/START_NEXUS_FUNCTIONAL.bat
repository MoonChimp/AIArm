@echo off
echo ============================================================
echo      NexusAI ULTIMATE Edition - Startup
echo ============================================================
echo.
echo ULTIMATE AI Assistant with:
echo   - Ollama LLM Integration (REAL responses)
echo   - Cinema Agent (REAL SDXL image generation)
echo   - Personality System (REAL bond tracking)
echo   - Memory System (REAL conversation context)
echo   - Learning System (REAL adaptation)
echo   - Self-Education (REAL research & learning)
echo   - ML Integration (REAL model training)
echo   - Professional Web Interface
echo.
echo ============================================================
echo.

echo [IMPORTANT] Prerequisites Check:
echo.
echo 1. Ollama must be running:
echo    Start with: ollama serve
echo    (In a separate terminal)
echo.
echo 2. Python packages required:
echo    pip install flask flask-cors requests
echo.
echo 3. For Cinema Agent (optional but recommended):
echo    Run: D:\AIArm\INSTALL_CINEMA_DEPENDENCIES.bat
echo.
pause

echo.
echo [1/2] Starting NexusAI FUNCTIONAL Backend...
start "NexusAI Functional Backend" cmd /k "cd /d D:\AIArm\NexusAI_Commercial\backend && python nexus_functional_api.py"

echo.
echo Waiting for backend to initialize...
timeout /t 8 /nobreak

echo.
echo [2/2] Opening NexusAI PROFESSIONAL Interface...
start "" "D:\AIArm\NexusAI_Commercial\html\chat.html"

echo.
echo ============================================================
echo      NexusAI ULTIMATE Edition STARTED!
echo ============================================================
echo.
echo Backend API: http://localhost:5000
echo Test Interface: Opened in browser
echo.
echo ULTIMATE Features Active:
echo   - Chat with Ollama (real LLM responses)
echo   - Cinema Agent (real SDXL generation)
echo   - Personality tracking (real bond system)
echo   - Memory System (real conversation context)
echo   - Learning System (real adaptation)
echo   - Self-Education (real research & learning)
echo   - ML Integration (real model training)
echo   - Code Execution (real Python/Node.js)
echo   - File Management (real system access)
echo.
echo To test:
echo   1. Chat: Type any message (remembers context!)
echo   2. Generate image: "generate image a sunset over mountains"
echo   3. Change personality: Use dropdown selector
echo   4. Test memory: Ask about previous topics
echo   5. Test learning: Ask about unknown subjects
echo   6. Test coding: "Create a Python function"
echo.
echo Make sure Ollama is running:
echo   ollama serve
echo.
echo API Endpoints Available:
echo   - /api/chat - Conversational AI with memory
echo   - /api/cinema/generate - Image generation
echo   - /api/execute - Code execution
echo   - /api/files/* - File management
echo   - /api/memory/* - Conversation memory
echo   - /api/learning/* - Learning system
echo   - /api/research/* - Web research
echo   - /api/ml/* - Machine learning integration
echo.
echo Press any key to continue...
pause >nul
