@echo off

REM www.oreilly.com/library/view/windows-2000-quick/0596000170/ch06s08.html
color F0

cd /d "%~dp0"

set "TOOL=grafana"
echo Do not forget to forward the %TOOL% port via Windows firewall
echo Access address: "http://127.0.0.1:3000"

bin\grafana.exe server ^
    --config="%cd%\%TOOL%.ini" > "%TOOL%.log" 2>&1

rem Do not forget to copy the INI configuration file
rem Default credentials: admin/admin
rem Finally add Prometheus Data Source
