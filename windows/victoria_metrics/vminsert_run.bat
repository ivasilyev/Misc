@echo off

REM www.oreilly.com/library/view/windows-2000-quick/0596000170/ch06s08.html
color F0

cd /d "%~dp0"

set "TOOL=vminsert"
set "HTTP_USERNAME="
set "HTTP_PASSWORD="
set "VM_INSERT_HTTP_PORT=8480"
set "VM_STORAGE_INSERT_PORT=8400"
set "VM_STORAGE_URL=127.0.0.1:%VM_STORAGE_INSERT_PORT%"

title %TOOL%

for /L %%i in () do (
    echo Start %TOOL%
    echo Check http://127.0.0.1:%VM_INSERT_HTTP_PORT%
    "vminsert-windows-amd64-prod.exe" ^
        -httpAuth.password="%HTTP_PASSWORD%" ^
        -httpAuth.username="%HTTP_USERNAME%" ^
        -storageNode="%VM_STORAGE_URL%" ^
        -httpListenAddr="0.0.0.0:%VM_INSERT_HTTP_PORT%" ^
        -insert.maxQueueDuration="5m0s" ^
        -maxConcurrentInserts="128" ^
        -maxLabelsPerTimeseries="36" ^
        -loggerLevel="FATAL" > "%TOOL%.log" 2>&1
)
rem    -loggerLevel="INFO" > "%TOOL%.log" 2>&1
