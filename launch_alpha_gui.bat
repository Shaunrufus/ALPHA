@echo off
echo ========================================
echo    ALPHA GUI Voice Assistant
echo ========================================
echo.
echo This will open ALPHA with a beautiful GUI!
echo.
echo Press any key to continue...
pause >nul

echo.
echo Opening ALPHA GUI...
start "ALPHA GUI" cmd /k "cd /d C:\ALPHA && venv\Scripts\activate && python alpha_gui_assistant.py"

echo.
echo ALPHA GUI launched! 
echo Keep this window open for reference.
echo.
echo Press any key to close this launcher...
pause >nul
