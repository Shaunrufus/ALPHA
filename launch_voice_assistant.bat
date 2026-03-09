@echo off
echo Starting Voice Assistant in new terminal...
start "Voice Assistant" cmd /k "cd /d C:\ALPHA && venv\Scripts\activate && python realtime_voice_assistant.py"
echo New terminal opened! Keep this one running for your server.
pause
