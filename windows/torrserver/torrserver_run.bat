@echo off

REM www.oreilly.com/library/view/windows-2000-quick/0596000170/ch06s08.html
color 0E

cd /d "%~dp0"
set "TOOL=torrserver"
echo Start %TOOL%
"TorrServer-windows-amd64.exe" ^
  --port 8090 ^
  --ip 0.0.0.0  > "%TOOL%.log" 2>&1
