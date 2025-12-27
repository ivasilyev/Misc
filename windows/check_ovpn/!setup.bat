@echo off

set "SCRIPT_DIR=%~dp0"
set "BASE_NAME=CheckOpenVPN"
set "TARGET_DIR=C:\!SCRIPTS\%BASE_NAME%\"

md "%TARGET_DIR%"

echo Create environment for admin scripts

cd /d "%SCRIPT_DIR%"

REM Add scripts to copy
for %%f in (
    %BASE_NAME%.bat
    %BASE_NAME%.ps1
) do copy "%%f" "%TARGET_DIR%"

echo Start scheduler to import the profile
powershell -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -Command "$TaskName = '%BASE_NAME%' ;$TaskXml = [xml](Get-Content '%BASE_NAME%.xml'); Register-ScheduledTask -TaskName $TaskName -Xml $TaskXml.OuterXml; Get-ScheduledTask -TaskName $TaskName"

echo Then go to Security options and use the Administrators group
start "" taskschd.msc

echo Also add the OpenVPN network connection
start "" ncpa.cpl

start "" explorer "%TARGET_DIR%"

timeout 5
