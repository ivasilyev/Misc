@echo off

REM Run this script with elevated permissions

set "X=%~dp0"

rem Allow everyone to RWX a folder
rem REM echo Y | icacls "%X%" /grant ???:F /t
echo Change permissions for "%X%"
echo Y|for /D %%i in ("%X%"*) do (
    echo(
    echo Fix permissions for "%%i"
    takeown /f "%%i"* /r
    icacls "%%i" /grant Everyone:F /q /t
)
timeout 15
