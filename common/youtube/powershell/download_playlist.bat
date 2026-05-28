@echo off
chcp 65001
cd /d "%~dp0"

title download_playlist
powershell -NoLogo -ExecutionPolicy Bypass -Command "%cd%\%~n0.ps1 -playlistUrl 'https://www.youtube.com/@channel/videos' -downloadFolder 'path'"

pause
