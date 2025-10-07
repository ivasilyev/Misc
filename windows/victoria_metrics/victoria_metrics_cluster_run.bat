@echo off

cd /d "%~dp0"

echo Start VictoriaMetrics storage
cmd /c start "" "vmstorage_run.bat"
timeout 3

echo Start VictoriaMetrics inserter
cmd /c start "" "vminsert_run.bat"
timeout 1

echo Start VictoriaMetrics selector
cmd /c start "" "vmselect_run.bat"
timeout 1

echo Start VictoriaMetrics agent
cmd /c start "" "vmagent_run.bat"
timeout 1

exit
