@echo off

set "MSG=Check disk %1"

title %MSG%

echo %MSG%

timeout 1

echo Y | "%SystemRoot%\System32\chkdsk.exe" %1: /f /r /x > "logs\chkdsk-%1.log

exit
