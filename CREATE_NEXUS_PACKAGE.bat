@echo off
echo ========================================
echo Nexus AI - Package Creator
echo ========================================
echo.
echo This will create a clean deployment package
echo with ONLY essential files (~500MB)
echo.
pause

set PACKAGE_DIR=D:\NexusAI_Package
set SOURCE_DIR=D:\AIArm

echo.
echo Creating package directory...
if exist "%PACKAGE_DIR%" rmdir /s /q "%PACKAGE_DIR%"
mkdir "%PACKAGE_DIR%"

echo.
echo Copying CORE files...
xcopy "%SOURCE_DIR%\nexus_api_server.py" "%PACKAGE_DIR%\" /Y
xcopy "%SOURCE_DIR%\START_NEXUS.bat" "%PACKAGE_DIR%\" /Y
xcopy "%SOURCE_DIR%\INSTALL_FFMPEG.txt" "%PACKAGE_DIR%\" /Y
xcopy "%SOURCE_DIR%\NEXUS_ESSENTIAL_FILES.txt" "%PACKAGE_DIR%\" /Y

echo Copying NexusCore (Brain)...
xcopy "%SOURCE_DIR%\NexusCore\*.py" "%PACKAGE_DIR%\NexusCore\" /Y /I

echo Copying Agents...
xcopy "%SOURCE_DIR%\InnerLife\Agents\agent_base.py" "%PACKAGE_DIR%\InnerLife\Agents\" /Y /I
xcopy "%SOURCE_DIR%\InnerLife\Agents\real_*.py" "%PACKAGE_DIR%\InnerLife\Agents\" /Y /I

echo Copying Inner Life (Memory system)...
xcopy "%SOURCE_DIR%\InnerLife\thoughts_manager.py" "%PACKAGE_DIR%\InnerLife\" /Y /I
xcopy "%SOURCE_DIR%\InnerLife\associative_memory.py" "%PACKAGE_DIR%\InnerLife\" /Y /I
xcopy "%SOURCE_DIR%\InnerLife\emotional_state.py" "%PACKAGE_DIR%\InnerLife\" /Y /I
xcopy "%SOURCE_DIR%\InnerLife\concept_graph.py" "%PACKAGE_DIR%\InnerLife\" /Y /I

echo Copying UI...
xcopy "%SOURCE_DIR%\NexusUI_Static\*.*" "%PACKAGE_DIR%\NexusUI_Static\" /Y /I

echo Creating directories for generated content...
mkdir "%PACKAGE_DIR%\Generated\Code"
mkdir "%PACKAGE_DIR%\Generated\Music"
mkdir "%PACKAGE_DIR%\Generated\Images"
mkdir "%PACKAGE_DIR%\Generated\Videos"
mkdir "%PACKAGE_DIR%\Generated\Stories"

echo Creating Memory directory...
mkdir "%PACKAGE_DIR%\Memory"

echo Copying existing memory (if any)...
if exist "%SOURCE_DIR%\Memory\*.json" (
    xcopy "%SOURCE_DIR%\Memory\*.json" "%PACKAGE_DIR%\Memory\" /Y
)

echo.
echo Creating requirements.txt...
(
echo flask
echo flask-cors
echo requests
echo psutil
echo gtts
echo pyttsx3
echo pillow
echo scipy
echo moviepy
) > "%PACKAGE_DIR%\requirements.txt"

echo.
echo Creating README.txt...
(
echo ========================================
echo NEXUS AI - Deployment Package
echo ========================================
echo.
echo INSTALLATION:
echo 1. Install Python 3.11+
echo 2. Install Ollama from https://ollama.ai
echo 3. Run: pip install -r requirements.txt
echo 4. Pull required models:
echo    ollama pull llama3:latest
echo    ollama pull qwen2.5-coder:7b
echo 5. Create merged model:
echo    ollama create nexusai-a0-coder1.0:latest -f NexusAI-A0-coder1.0.Modelfile
echo.
echo OPTIONAL:
echo - Install FFmpeg for video generation
echo - Install Stable Diffusion WebUI for image generation
echo.
echo TO START:
echo - Double-click START_NEXUS.bat
echo - Or run: python nexus_api_server.py
echo.
echo ACCESS UI:
echo http://localhost:3002/index_simple.html
echo ========================================
) > "%PACKAGE_DIR%\README.txt"

echo.
echo Copying Modelfile for merged model...
if exist "%SOURCE_DIR%\NexusAI-A0-coder1.0.Modelfile" (
    xcopy "%SOURCE_DIR%\NexusAI-A0-coder1.0.Modelfile" "%PACKAGE_DIR%\" /Y
)

echo.
echo ========================================
echo Package created successfully!
echo ========================================
echo Location: %PACKAGE_DIR%
echo.
dir "%PACKAGE_DIR%" /s /b | find /c /v ""
echo files packaged.
echo.
pause
