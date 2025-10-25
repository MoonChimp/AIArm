# PowerShell script to remove auto-save functionality from renderer.js
# This removes the problematic auto-save that causes disconnections

$rendererPath = "D:\AIArm\nexusai-agent\packages\core-assistant\src\renderer.js"

Write-Host "Removing auto-save functionality from renderer.js..." -ForegroundColor Yellow

# Check if file exists
if (-not (Test-Path $rendererPath)) {
    Write-Host "Error: renderer.js not found at $rendererPath" -ForegroundColor Red
    exit 1
}

# Read the file content
$content = Get-Content $rendererPath -Raw

# Remove the auto-save call from addMessage function
$content = $content -replace '\s*this\.autoSaveConversation\(\);\s*', ''

# Replace the entire autoSaveConversation function with an empty stub
$autoSavePattern = 'async autoSaveConversation\(\) \{[^}]*\{[^}]*\}[^}]*\}'
$content = $content -replace $autoSavePattern, 'async autoSaveConversation() {
        // Auto-save disabled to prevent disconnection issues
        // Memory retention will be handled by external monitor if needed
    }'

# Also remove any other auto-save calls that might exist
$content = $content -replace 'this\.autoSaveConversation\(\);?', '// Auto-save disabled'

# Write the corrected content back to the file
Set-Content -Path $rendererPath -Value $content -NoNewline

Write-Host "✅ Auto-save functionality removed successfully!" -ForegroundColor Green
Write-Host "Changes made:" -ForegroundColor Cyan
Write-Host "  1. Removed autoSaveConversation() calls from addMessage function" -ForegroundColor White
Write-Host "  2. Replaced autoSaveConversation function with empty stub" -ForegroundColor White
Write-Host "  3. Added comments explaining the change" -ForegroundColor White
Write-Host ""
Write-Host "Your agent should now maintain consistent connection!" -ForegroundColor Green
Write-Host "Run: npm run start:essential" -ForegroundColor Green
