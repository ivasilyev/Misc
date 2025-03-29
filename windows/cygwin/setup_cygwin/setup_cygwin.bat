@echo off

cd /d "%~dp0"

powershell -ExecutionPolicy Bypass -File "%~n0.ps1"
