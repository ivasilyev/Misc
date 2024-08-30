@echo off

REM Run this script with elevated permissions

echo "Move download directories outside from the system drive"

set "SOURCE_DIR=%USERPROFILE%\Downloads"
set "DESTINATION_DIR=D:\Downloads\Generic"

mkdir "%DESTINATION_DIR%"
robocopy "%SOURCE_DIR%" "%DESTINATION_DIR%" /S /MOV
rmdir /S /Q "%SOURCE_DIR%"
mklink /J "%SOURCE_DIR%" "%DESTINATION_DIR%"

timeout 15
