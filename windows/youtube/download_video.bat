@echo off
chcp 65001 > NUL
cd /d "%~dp0"

set BAR=========================================================================

echo(
echo %BAR%
echo Enter the video (NOT playlist) URL:
echo %BAR%
echo(
echo(
echo(

set /p URL=
echo(
echo(
echo(

echo %BAR%
echo Download video with highest quality.
echo %BAR%
echo(
echo(
echo(

set "DL_DIR=%USERPROFILE%\Videos\youtube-dl"
mkdir "%DL_DIR%"

powershell -NoLogo -ExecutionPolicy Bypass -File "%cd%\%~n0.ps1"

echo(
echo(
echo(

echo %BAR%
echo Done, check the folder: %DL_DIR%
echo %BAR%
echo(
echo(
echo(

start "" %DL_DIR%
pause
