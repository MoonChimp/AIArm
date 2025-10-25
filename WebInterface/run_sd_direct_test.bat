@echo off
echo.
echo === Direct StableDiffusion API Test ===
echo.

echo Running Python script to test direct connection to StableDiffusion WebUI API...
echo This will provide detailed diagnostics about what's happening.
echo.

python "D:\AIArm\WebInterface\test_sd_direct.py"

echo.
echo Test complete. Please check the output above for details.
echo.
echo If images were generated successfully, they should be in:
echo - D:\AIArm\Images
echo - D:\AIArm\WebInterface\static\images
echo.
echo Press any key to exit...
pause >nul