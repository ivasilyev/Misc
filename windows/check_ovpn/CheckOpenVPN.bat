@echo off

cd /d "%~dp0"

powershell -NoLogo -ExecutionPolicy Bypass -File "%~n0.ps1"

rem pause
