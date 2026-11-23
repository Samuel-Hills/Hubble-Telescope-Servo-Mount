@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Run setup_windows.bat once before starting the app.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" src\motor_control_web.py
if errorlevel 1 pause
exit /b 0