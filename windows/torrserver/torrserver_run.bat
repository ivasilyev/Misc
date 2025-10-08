@echo off

REM www.oreilly.com/library/view/windows-2000-quick/0596000170/ch06s08.html
color F0

cd /d "%~dp0"
set "TOOL=torrserver"
set "HTTP_PORT=8090"

title %TOOL%

for /L %%i in () do (
    echo Start %TOOL%
    echo Check http://127.0.0.1:%HTTP_PORT%
    "TorrServer-windows-amd64.exe" ^
        --httpauth ^
        --ip="0.0.0.0" ^
        --port="%HTTP_PORT%" > "%TOOL%.log" 2>&1
)