@echo off

set "SCRIPT_DIR=%~dp0"
set "BASE_NAME=StartupAdmin"
set "TARGET_DIR=C:\!SCRIPTS\%BASE_NAME%\"

md "%TARGET_DIR%"

echo Create environment for admin scripts

cd /d "%SCRIPT_DIR%"

REM Add scripts to copy
for %%f in (
    %BASE_NAME%.bat
    vmware.bat
) do copy "%%f" "%TARGET_DIR%"

Robocopy "VMAB" "%TARGET_DIR%VMAB" /E /ZB /R:1 /W:1

echo Start scheduler to import the profile
powershell -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -Command "$TaskName = '%BASE_NAME%' ;$TaskXml = [xml](Get-Content '%BASE_NAME%.xml'); Register-ScheduledTask -TaskName $TaskName -Xml $TaskXml.OuterXml; Get-ScheduledTask -TaskName $TaskName"

echo Then go to Security options and use the Administrators group
start "" taskschd.msc

start "" explorer "%TARGET_DIR%"

timeout 5
