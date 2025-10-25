# PowerShell script to fix syntax errors in renderer.js
# This script fixes two specific syntax issues

$rendererPath = "D:\AIArm\nexusai-agent\packages\core-assistant\src\renderer.js"

Write-Host "Fixing syntax errors in renderer.js..." -ForegroundColor Yellow

# Check if file exists
if (-not (Test-Path $rendererPath)) {
    Write-Host "Error: renderer.js not found at $rendererPath" -ForegroundColor Red
    exit 1
}

# Read the file content
$content = Get-Content $rendererPath -Raw

# Fix 1: Replace incomplete .replace(/\n/g, ''); with .replace(/\n/g, '<br>');
$content = $content -replace '\.replace\(/\\n/g, ''\);', '.replace(/\n/g, ''<br>'');'

# Fix 2: Remove extra space in function declaration async autoSaveConversation( ) {
$content = $content -replace 'async autoSaveConversation\( \) \{', 'async autoSaveConversation() {'

# Write the corrected content back to the file
Set-Content -Path $rendererPath -Value $content -NoNewline

Write-Host "✅ Syntax errors fixed successfully!" -ForegroundColor Green
Write-Host "Fixed issues:" -ForegroundColor Cyan
Write-Host "  1. Completed .replace(/\n/g, '<br>'); in formatMessage function" -ForegroundColor White
Write-Host "  2. Removed extra space in autoSaveConversation() function declaration" -ForegroundColor White
Write-Host ""
Write-Host "You can now run: npm run start:essential" -ForegroundColor Green
