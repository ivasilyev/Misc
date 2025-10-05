@echo off

cd "%~dp0"

powershell -NoLogo -ExecutionPolicy Bypass -File "%~n0.ps1"
