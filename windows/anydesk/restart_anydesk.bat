@echo off

REM Run this script with elevated permissions

echo Restart AnyDesk with real-tme priority
taskkill /IM "AnyDesk.exe" /F
start "" "%PROGRAMFILES(x86)%\AnyDesk\AnyDesk.exe"
timeout 7
wmic process where name="AnyDesk.exe" CALL setpriority 256

timeout 15
