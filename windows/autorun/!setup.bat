@echo off

set "SCRIPT_DIR=%~dp0"
set "TARGET_DIR=C:\!SCRIPTS\startup\"

md "%TARGET_DIR%"

echo Create environment for admin scripts

cd /d "%SCRIPT_DIR%"

REM Add scripts to copy
for %%f in (
    startup-admin.bat
    vmware.bat
) do copy "%%f" "%TARGET_DIR%"

echo Start scheduler to import the profile
powershell -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -Command "$TaskName = '!STARTUP-ADMIN' ;$TaskXml = [xml](Get-Content '!STARTUP-ADMIN.xml'); Register-ScheduledTask -TaskName $TaskName -Xml $TaskXml.OuterXml; Get-ScheduledTask -TaskName $TaskName"

echo Then go to Security options and use the Administrators group
start "" taskschd.msc

start "" explorer "%TARGET_DIR%"

timeout 5
