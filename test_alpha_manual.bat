@echo off
echo ========================================
echo    ALPHA Wake Word Test Launcher
echo ========================================
echo.
echo This will open a new terminal and run ALPHA
echo.
echo Press any key to continue...
pause >nul

echo.
echo Opening new terminal...
start "ALPHA Test" cmd /k "cd /d C:\ALPHA && echo Activating virtual environment... && venv\Scripts\activate && echo Starting ALPHA... && python alpha_wake_word_assistant.py"

echo.
echo New terminal opened! 
echo Keep this window open for reference.
echo.
echo Press any key to close this launcher...
pause >nul
