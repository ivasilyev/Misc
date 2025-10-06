@echo off

REM www.oreilly.com/library/view/windows-2000-quick/0596000170/ch06s08.html
color F0

cd /d "%~dp0"

set "TOOL=vmstorage"
set "TOOL_DATA_DIRECTORY=vmstorage-data"
set "HTTP_USERNAME="
set "HTTP_PASSWORD="
set "VM_STORAGE_HTTP_PORT=8482"
set "VM_STORAGE_INSERT_PORT=8400"
set "VM_STORAGE_SELECT_PORT=8401"

echo Start %TOOL%
echo Check http://127.0.0.1:%VM_STORAGE_HTTP_PORT%
"vmstorage-windows-amd64-prod.exe" ^
    -httpAuth.password="%HTTP_PASSWORD%" ^
    -httpAuth.username="%HTTP_USERNAME%" ^
    -httpListenAddr="0.0.0.0:%VM_STORAGE_HTTP_PORT%" ^
    -retentionPeriod="3y" ^
    -search.maxConcurrentRequests="100" ^
    -search.maxUniqueTimeseries="900000" ^
    -search.maxQueueDuration="5m" ^
    -storageDataPath="%TOOL_DATA_DIRECTORY%" ^
    -vminsertAddr="0.0.0.0:%VM_STORAGE_INSERT_PORT%" ^
    -vmselectAddr="0.0.0.0:%VM_STORAGE_SELECT_PORT%" ^
    -loggerLevel="INFO" > "%TOOL%.log" 2>&1
rem    -loggerLevel="FATAL" > "%TOOL%.log" 2>&1
