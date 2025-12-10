@echo off
chcp 65001
cd /d "%~dp0"

title download_playlist
powershell -NoLogo -ExecutionPolicy Bypass -Command "%cd%\%~n0.ps1 -sourceRoot 'D:\test' -targetRoot 'C:\test'"
rem powershell -NoLogo -ExecutionPolicy Bypass -Command "%cd%\%~n0.ps1 -sourceRoot 'E:\test' -targetRoot 'C:\test'"
rem powershell -NoLogo -ExecutionPolicy Bypass -Command "%cd%\%~n0.ps1 -sourceRoot 'F:\test' -targetRoot 'C:\test'"

pause
