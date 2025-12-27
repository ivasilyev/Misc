@echo off

REM Script to backup configuration DAT files (e.g. from BitTorrent / uTorrent)
REM Requires installed 7z

echo Backup .DAT files into %1
set "PREVIOUS_DIR=%cd%"
cd /d "%1"

set "TOOL=%PROGRAMFILES%\7-Zip\7z.exe"
set "BACKUP_DIR=%cd%\backup\"

mkdir "%BACKUP_DIR%"
for %%F in ("%cd%") do set "DIRNAME=%%~nF"
for /f "tokens=1-4 delims=/. " %%a in ("%date%") do (set "NOW_DATE=%%c-%%b-%%a")
for /f "tokens=1-4 delims=/:." %%a in ("%time%") do (set "NOW_TIME=%%a-%%b-%%c-%%d")
rem set "ZIP=%BACKUP_DIR%%DIRNAME%_%NOW_DATE%-%NOW_TIME%.zip"
set "ARCHIVE=%BACKUP_DIR%%DIRNAME%_%NOW_DATE%-%NOW_TIME%.7z"

echo Create backup archive: %ARCHIVE%

rem "%TOOL%" a "%ZIP%" -bb3 -mx=9 *.dat
"%TOOL%" a -m0=lzma2 -mx "%ARCHIVE%" *.dat

cd /d "%PREVIOUS_DIR%"
echo Done backup .DAT files into %1
