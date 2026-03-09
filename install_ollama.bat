@echo off
echo ========================================
echo    Installing Ollama for Windows
echo ========================================
echo.

echo Downloading Ollama...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/ollama/ollama/releases/latest/download/ollama-windows-amd64.exe' -OutFile 'ollama.exe'"

echo.
echo Moving to Program Files...
if not exist "C:\Program Files\Ollama" mkdir "C:\Program Files\Ollama"
move ollama.exe "C:\Program Files\Ollama\ollama.exe"

echo.
echo Adding to PATH...
setx PATH "%PATH%;C:\Program Files\Ollama"

echo.
echo ========================================
echo    Ollama Installation Complete!
echo ========================================
echo.
echo Please restart your terminal/PowerShell
echo Then run: ollama --version
echo.
pause
