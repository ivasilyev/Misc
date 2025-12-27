@echo off

set "VM_DIR=V:\VM\"

echo Start VMware VMs
cd "%VM_DIR%"

rem Paste VM names here without quotes
for %%i in (

) do (
    echo Clean %%i
    del /S /Q "%VM_DIR%%%i"\*.lck
    echo Start %%i
    start "" "%PROGRAMFILES(X86)%\VMware\VMware Workstation\vmware.exe" -x "%VM_DIR%%%i\%%i.vmx"
    rem start "" "%PROGRAMFILES(X86)%\VMware\VMware Workstation\vmrun.exe" -T ws start "%VM_DIR%%%i\%%i.vmx"
    timeout 5
)
