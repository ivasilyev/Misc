@echo off

REM Run this script with elevated permissions

echo Add Windows Defender exclusion
powershell -inputformat none -NonInteractive -Command Add-MpPreference -ExclusionPath '%PROGRAM_PATH%'
timeout 15
