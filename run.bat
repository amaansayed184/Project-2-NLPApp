@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Set up the app using the Quick start instructions in readme.md first.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" app.py
