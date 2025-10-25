@echo off
title Ollama Connection Test
echo Ollama Connection Test
echo ====================
echo.
echo This script will check if Ollama is running on the expected port.
echo.

echo Step 1: Checking if Ollama is running on port 11434...
curl -s http://localhost:11434/api/version
if %errorlevel% equ 0 (
  echo.
  echo SUCCESS: Ollama is running and responding on port 11434.
  echo The version information is displayed above.
  echo.
  echo You can now start your NexusAI application using the start_nexus_core.bat script.
) else (
  echo.
  echo ERROR: Could not connect to Ollama on port 11434.
  echo.
  echo Troubleshooting steps:
  echo 1. Make sure Ollama is running with the command: ollama serve
  echo 2. Check if your firewall is blocking port 11434
  echo 3. Verify that no other application is using port 11434
  echo.
  echo Try running 'ollama serve' in a separate command prompt before starting NexusAI.
)

echo.
pause