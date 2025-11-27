@echo off

cd /d "%~dp0"

echo Get Virtual Machine Audio Back
set PATH=C:\Program Files\Oracle\VirtualBox;%PATH%
vboxmanage unregistervm VMAudioBack 2>nul
vboxmanage registervm "VMAudioBack.vbox"
start /MIN /B "" VBoxHeadless.exe -s VMAudioBack -start-paused
