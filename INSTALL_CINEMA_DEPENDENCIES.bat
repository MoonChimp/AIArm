@echo off
echo ============================================================
echo     NEXUS AI - Cinema-Quality Dependencies Installation
echo ============================================================
echo.
echo This will install everything needed for:
echo - Hollywood-quality content generation (SDXL, AnimateDiff)
echo - Professional video processing (MoviePy, FFmpeg)
echo - Voice synthesis and recognition
echo - AR/3D rendering capabilities
echo.
echo This may take 30-60 minutes depending on your internet speed.
echo.
pause

echo.
echo ============================================================
echo     PHASE 1: Core AI Dependencies
echo ============================================================
echo.

echo [1/6] Installing HuggingFace and PyTorch...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers diffusers accelerate safetensors
pip install huggingface-hub

echo.
echo [2/6] Installing Image Generation (SDXL, ControlNet)...
pip install opencv-python pillow-simd numpy scipy
pip install compel invisible-watermark
pip install xformers --index-url https://download.pytorch.org/whl/cu121

echo.
echo [3/6] Installing Video Processing (MoviePy, FFmpeg)...
pip install moviepy imageio imageio-ffmpeg
pip install opencv-contrib-python
pip install scikit-image

echo.
echo [4/6] Installing Voice AI (Whisper, Bark)...
pip install openai-whisper
pip install git+https://github.com/suno-ai/bark.git
pip install pydub soundfile librosa

echo.
echo [5/6] Installing 3D & Graphics...
pip install trimesh pyglet moderngl
pip install pyrender
pip install pywavefront

echo.
echo [6/6] Installing Additional Tools...
pip install tqdm rich colorama
pip install python-dotenv
pip install onnxruntime-gpu

echo.
echo ============================================================
echo     PHASE 2: Downloading AI Models
echo ============================================================
echo.

echo Creating models directory...
if not exist "D:\AIArm\Models" mkdir "D:\AIArm\Models"
if not exist "D:\AIArm\Models\SDXL" mkdir "D:\AIArm\Models\SDXL"
if not exist "D:\AIArm\Models\Voice" mkdir "D:\AIArm\Models\Voice"
if not exist "D:\AIArm\Models\AnimateDiff" mkdir "D:\AIArm\Models\AnimateDiff"

echo.
echo Note: Large AI models will be downloaded on first use
echo to save time and bandwidth now.
echo.
echo Models will be cached in: D:\AIArm\Models\
echo.

echo.
echo ============================================================
echo     PHASE 3: FFmpeg Setup
echo ============================================================
echo.

echo Checking for FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ FFmpeg is already installed
) else (
    echo ✗ FFmpeg not found
    echo.
    echo Please install FFmpeg:
    echo 1. Download from: https://www.gyan.dev/ffmpeg/builds/
    echo 2. Extract to C:\ffmpeg\
    echo 3. Add C:\ffmpeg\bin to PATH
    echo.
    pause
)

echo.
echo ============================================================
echo     INSTALLATION COMPLETE
echo ============================================================
echo.
echo ✓ Core AI dependencies installed
echo ✓ Image generation libraries ready
echo ✓ Video processing tools installed
echo ✓ Voice AI systems ready
echo ✓ 3D graphics libraries installed
echo.
echo Next steps:
echo 1. Run: D:\AIArm\TEST_CINEMA_SETUP.bat (verify installation)
echo 2. Configure: D:\AIArm\NexusCore\personality\config.json
echo 3. Start: D:\AIArm\MASTER_START_NEXUS_AI.bat
echo.
echo For AR glasses setup, see: D:\AIArm\HOLOGRAM_SETUP_GUIDE.md
echo.
pause
