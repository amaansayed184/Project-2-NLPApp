@echo off
setlocal
cd /d "%~dp0"
py -3.12 -c "import sys" >nul 2>&1
if not errorlevel 1 (
    py -3.12 scripts\setup_project.py
    goto finished
)
py -3.11 -c "import sys" >nul 2>&1
if not errorlevel 1 (
    py -3.11 scripts\setup_project.py
    goto finished
)
python scripts\setup_project.py
:finished
if errorlevel 1 (
    echo.
    echo Setup failed. Read the message above and the Troubleshooting section in readme.md.
    pause
    exit /b 1
)
echo.
echo Setup complete. Double-click run.bat to open NLPApp.
pause
