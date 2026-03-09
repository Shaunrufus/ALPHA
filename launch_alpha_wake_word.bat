@echo off
echo Starting ALPHA Wake Word Assistant in new terminal...
start "ALPHA Wake Word" cmd /k "cd /d C:\ALPHA && venv\Scripts\activate && python alpha_wake_word_assistant.py"
echo New terminal opened for ALPHA wake word detection!
echo Keep your server terminal running.
pause
