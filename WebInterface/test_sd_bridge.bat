@echo off
echo.
echo === Testing Direct StableDiffusion Bridge ===
echo.

REM Test input
set TEST_PROMPT=A colorful sunset over a peaceful lake with mountains in the background, photorealistic, highly detailed

echo Testing SD bridge with prompt: "%TEST_PROMPT%"
echo.

python "D:\AIArm\WebInterface\sd_bridge.py" --input "%TEST_PROMPT%"
echo.

echo Test with options:
python "D:\AIArm\WebInterface\sd_bridge.py" --input "{\"input\":\"A futuristic city skyline at night with flying cars\",\"options\":{\"quality\":\"high\",\"style\":\"photorealistic\"}}" --json
echo.

echo === Test complete ===
echo.
echo If the tests were successful, you should see JSON responses with image URLs.
echo The images should be saved in D:\AIArm\Images and D:\AIArm\WebInterface\static\images
echo.
echo Press any key to exit...
pause >nul