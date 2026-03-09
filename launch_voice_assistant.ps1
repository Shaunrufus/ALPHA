Write-Host "Starting Voice Assistant in new terminal..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\ALPHA; venv\Scripts\activate; python realtime_voice_assistant.py" -WindowStyle Normal
Write-Host "New terminal opened! Keep this one running for your server." -ForegroundColor Yellow
Read-Host "Press Enter to continue..."
