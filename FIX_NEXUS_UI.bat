@echo off
echo ============================================================
echo     NEXUS UI - Dependency Fix Script
echo ============================================================
echo.
echo This will fix the Rollup/Vite dependency issue...
echo.

cd /d D:\AIArm\NexusUI

echo [1/4] Removing old node_modules...
if exist node_modules (
    rmdir /s /q node_modules
    echo Removed node_modules
) else (
    echo node_modules not found, skipping...
)

echo.
echo [2/4] Removing package-lock.json...
if exist package-lock.json (
    del /f package-lock.json
    echo Removed package-lock.json
) else (
    echo package-lock.json not found, skipping...
)

echo.
echo [3/4] Installing dependencies with npm...
echo This may take a few minutes...
call npm install

echo.
echo [4/4] Verifying installation...
if exist node_modules\rollup (
    echo ✓ Rollup installed successfully
) else (
    echo ✗ Rollup installation failed
)

if exist node_modules\vite (
    echo ✓ Vite installed successfully
) else (
    echo ✗ Vite installation failed
)

echo.
echo ============================================================
echo     FIX COMPLETE
echo ============================================================
echo.
echo The dependencies should now be fixed.
echo You can now run: npm run dev
echo.
echo Or use the master startup script:
echo D:\AIArm\MASTER_START_NEXUS_AI.bat
echo.
pause
