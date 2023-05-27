@echo off

setlocal ENABLEDELAYEDEXPANSION

set "CWD=%cd%"

cd /d "%~dp0"

mkdir "logs"

for /f "skip=1 delims=" %%i in ('"%SystemRoot%\System32\wbem\wmic.exe" logicaldisk get caption') do (
    set j=%%i
    set j=!j::=!
    echo Process !j!
    timeout 1
    
    start "" check_disk.bat !j!
)

cd /d "%CWD%"

pause
