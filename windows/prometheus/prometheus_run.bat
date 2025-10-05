@echo off

REM www.oreilly.com/library/view/windows-2000-quick/0596000170/ch06s08.html
color F0

cd /d "%~dp0"

set "TOOL=prometheus"
set "PORT=9090"
set "TOOL_DATA_DIRECTORY=data"
set "TOOL_CFG=prometheus_main.yml"
set "TOOL_WEB_CFG=prometheus_web.yml"

echo Check configuration files
start promtool.exe "%TOOL_CFG%" "%TOOL_WEB_CFG%"
timeout 1

echo Start %TOOL%
echo Check http://127.0.0.1:%PORT%
rem curl -X POST http://127.0.0.1:9090/-/reload
rem python gen-pass.py

rem Do not set too large retention time in order to push it elsewhere
"prometheus.exe" ^
    --config.file="%TOOL_CFG%" ^
    --log.level="error" ^
    --storage.tsdb.path="%TOOL_DATA_DIRECTORY%" ^
    --storage.tsdb.retention.time="1h" ^
    --web.config.file="%TOOL_WEB_CFG%" ^
    --web.enable-lifecycle ^
    --web.listen-address "0.0.0.0:9090" > "%TOOL%.log" 2>&1
