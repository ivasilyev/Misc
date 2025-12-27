@echo off

set "SCRIPT_DIR=%~dp0"

cd /d "%SCRIPT_DIR%"

echo Launch programs by admin

REM echo Start VM Audio fix
REM cd /d "%SCRIPT_DIR%\VMAB"
REM start cmd /c "VMAB.cmd"
REM timeout 20

echo Start VMs
cd /d "%SCRIPT_DIR%"
call "vmware.bat"
timeout 10

echo Minimize all windows and show the Desktop
cd /d "%SCRIPT_DIR%"
powershell -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -Command "(New-Object -ComObject shell.application).toggleDesktop()"
timeout 1

echo Lock PC
rundll32.exe user32.dll,LockWorkStation

REM pause
