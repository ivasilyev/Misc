@echo off

REM Run this script with elevated permissions

echo View the last 1 day Windows logons
powershell -inputformat none -NonInteractive -Command "$LastDay = (Get-Date).AddDays(-1); Get-WinEvent -FilterHashtable @{ LogName = 'Security'; ID = @(4624, 4625); StartTime = $LastDay } | Select-Object TimeCreated, Id, Message | Format-Table -AutoSize"
timeout 15
