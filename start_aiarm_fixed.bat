@echo off
color 0B
cls

echo ================================================================================
echo                       AIARM MULTI-AGENT SYSTEM LAUNCHER                       
echo ================================================================================
echo.
echo This launcher will start the AIArm multi-agent system with continuous thinking,
echo hierarchical reasoning, and specialized agents for web development, mobile apps,
echo database architecture, and more.
echo.
echo The system implements:
echo.
echo 1. Central orchestration system coordinating all agents
echo 2. Multiple specialized AI models working collaboratively
echo 3. Real-time continuous thought processing
echo 4. Hierarchical reasoning across different abstraction levels
echo 5. Project continuity with memory persistence
echo.
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    color 0C
    echo ERROR: Python is not installed or not in your PATH.
    echo        Please install Python 3.8 or higher.
    goto :error
)

REM Check for critical file
if not exist "D:\AIArm\MultiAgent\orchestrator.py" (
    color 0C
    echo ERROR: Could not find D:\AIArm\MultiAgent\orchestrator.py
    echo        Please ensure all AIArm files are in the correct location.
    goto :error
)

REM Create memory directories
if not exist "D:\AIArm\MultiAgent\Memory" (
    echo Creating Memory directory...
    mkdir "D:\AIArm\MultiAgent\Memory"
)

if not exist "D:\AIArm\MultiAgent\Projects" (
    echo Creating Projects directory...
    mkdir "D:\AIArm\MultiAgent\Projects"
)

REM Check for required modules
echo.
echo Checking Python dependencies...
python -c "import json, threading, queue, uuid, random" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    color 0E
    echo WARNING: Some Python modules may be missing.
    echo          The system will attempt to run anyway.
)

echo.
echo Starting AIArm Multi-Agent System...
echo.

REM Start the system with error handling
python D:\AIArm\MultiAgent\orchestrator.py
if %ERRORLEVEL% neq 0 (
    color 0C
    echo.
    echo ERROR: The AIArm system encountered an error and has stopped.
    echo        Please check the error message above.
    goto :error
)

goto :end

:error
echo.
echo ================================================================================
echo                                ERROR OCCURRED                               
echo ================================================================================
pause
exit /b 1

:end
echo.
echo ================================================================================
echo                          AIARM SYSTEM SHUTDOWN                          
echo ================================================================================
echo.
echo The system has shut down. To restart, run this launcher again.
echo.
pause
