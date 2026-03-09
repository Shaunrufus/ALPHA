Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    ALPHA Wake Word Test Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will open a new terminal and run ALPHA" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "Opening new terminal..." -ForegroundColor Green

# Launch new PowerShell window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\ALPHA; Write-Host 'Activating virtual environment...' -ForegroundColor Yellow; venv\Scripts\activate; Write-Host 'Starting ALPHA...' -ForegroundColor Green; python alpha_wake_word_assistant.py" -WindowStyle Normal

Write-Host ""
Write-Host "New terminal opened!" -ForegroundColor Green
Write-Host "Keep this window open for reference." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to close this launcher..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
