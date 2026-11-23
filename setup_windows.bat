@echo off
setlocal
cd /d "%~dp0"

py -3.13 --version >nul 2>&1
if errorlevel 1 goto missing_python

if not exist ".venv\Scripts\python.exe" (
    echo Creating a local Python 3.13 environment...
    py -3.13 -m venv .venv
    if errorlevel 1 goto setup_failed
)

echo Installing the project dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto setup_failed

echo.
echo Setup complete. Start the control app with run_motor_control.bat.
pause
exit /b 0

:missing_python
echo Python 3.13 was not found.
echo Install 64-bit Python 3.13 from https://www.python.org/downloads/windows/
echo Make sure the Python Launcher is installed, then run this file again.
goto setup_failed

:setup_failed
echo.
echo Setup failed. Review the message above and rerun setup_windows.bat.
pause
exit /b 1