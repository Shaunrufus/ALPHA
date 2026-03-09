@echo off
echo ========================================
echo    Set Groq API Key
echo ========================================
echo.
echo Please enter your Groq API key:
echo (Get it from: https://console.groq.com/)
echo.
set /p GROQ_API_KEY="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"

echo.
echo Setting environment variable...
setx GROQ_API_KEY "%GROQ_API_KEY%"

echo.
echo ========================================
echo    API Key Set Successfully!
echo ========================================
echo.
echo Please restart your terminal/PowerShell
echo Then test with: python groq_integration.py
echo.
pause
