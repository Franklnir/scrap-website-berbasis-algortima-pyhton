@echo off
cd /d "%~dp0"
py -3 -m venv .venv
if errorlevel 1 exit /b 1
.venv\Scripts\python.exe -m pip install .
if errorlevel 1 exit /b 1
echo.
echo Selesai. Di CMD: .venv\Scripts\activate.bat lalu scrapmcp
 echo Di PowerShell: .\.venv\Scripts\scrapmcp.exe
pause
