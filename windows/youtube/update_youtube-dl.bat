@echo off
chcp 65001 > NUL
cd /d "%~dp0"

title Update Youtube-DL
powershell -NoLogo -ExecutionPolicy Bypass -File "%cd%\%~n0.ps1"

pause
