@echo off

REM www.oreilly.com/library/view/windows-2000-quick/0596000170/ch06s08.html
color F0

cd /d "%~dp0"

set "TOOL=vmagent"
set "PROMETHEUS_CFG=prometheus_main.yml"
set "VM_AGENT_DATA_DIRECTORY="
set "HTTP_USERNAME="
set "HTTP_PASSWORD="
set "VM_AGENT_HTTP_PORT=8483"
set "VM_INSERT_HTTP_PORT=8480"
set "VM_INSERT_URL=127.0.0.1:%VM_INSERT_HTTP_PORT%"

title %TOOL%

for /L %%i in () do (
    echo Start %TOOL%
    echo Check http://127.0.0.1:%VM_AGENT_HTTP_PORT%
    "vmagent-windows-amd64-prod.exe" ^
        -httpAuth.password="%HTTP_PASSWORD%" ^
        -httpAuth.username="%HTTP_USERNAME%" ^
        -httpListenAddr="0.0.0.0:%VM_AGENT_HTTP_PORT%" ^
        -promscrape.config="%PROMETHEUS_CFG%" ^
        -promscrape.dropOriginalLabels="true" ^
        -promscrape.maxScrapeSize="671088640" ^
        -promscrape.streamParse="true" ^
        -promscrape.config.strictParse="false" ^
        -remoteWrite.queues="10" ^
        -remoteWrite.tmpDataPath="%VM_AGENT_DATA_DIRECTORY%" ^
        -remoteWrite.url="http://%VM_INSERT_URL%/insert/0/prometheus/" ^
        -remoteWrite.basicAuth.password "%HTTP_PASSWORD%" ^
        -remoteWrite.basicAuth.username "%HTTP_USERNAME%" ^
        -loggerLevel="FATAL" > "%TOOL%.log" 2>&1
)
rem    -loggerLevel="INFO" > "%TOOL%.log" 2>&1
