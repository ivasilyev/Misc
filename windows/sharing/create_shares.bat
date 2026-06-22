@echo off
chcp 65001 > NULL
cd /d "%~dp0"

powershell -NoLogo -ExecutionPolicy Bypass -File "%~n0.ps1"

pause
