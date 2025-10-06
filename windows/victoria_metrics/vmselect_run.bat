@echo off

REM www.oreilly.com/library/view/windows-2000-quick/0596000170/ch06s08.html
color F0

cd /d "%~dp0"

set "TOOL=vmselect"
set "HTTP_USERNAME="
set "HTTP_PASSWORD="
set "VM_SELECT_HTTP_PORT=8481"
set "VM_STORAGE_SELECT_PORT=8401"
set "VM_STORAGE_URL=127.0.0.1:%VM_STORAGE_SELECT_PORT%"

echo Start %TOOL%
echo Check http://127.0.0.1:%VM_SELECT_HTTP_PORT%/select/0/prometheus/
"vmselect-windows-amd64-prod.exe" ^
    -httpAuth.password="%HTTP_PASSWORD%" ^
    -httpAuth.username="%HTTP_USERNAME%" ^
    -httpListenAddr="0.0.0.0:%VM_SELECT_HTTP_PORT%" ^
    -search.maxConcurrentRequests="100" ^
    -search.maxQueryDuration=120s ^
    -search.maxQueryLen="510000" ^
    -search.maxSeries="1000000" ^
    -search.maxUniqueTimeseries="900000" ^
    -search.maxQueueDuration="5m" ^
    -search.logSlowQueryDuration=180s ^
    -storageNode="%VM_STORAGE_URL%" ^
    -loggerLevel="INFO" > "%TOOL%.log" 2>&1
rem    -loggerLevel="FATAL" > "%TOOL%.log" 2>&1
