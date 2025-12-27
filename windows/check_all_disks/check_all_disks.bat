@echo off
chcp 65001 > nul
cd /d "%~dp0"

title Backup
powershell -NoLogo -ExecutionPolicy Bypass -Command "%cd%\%~n0.ps1"

pause
