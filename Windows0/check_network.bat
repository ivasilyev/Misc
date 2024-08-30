@echo off

set "OUT_FILE=%HOMEDRIVE%%HOMEPATH%\Desktop\network.txt"

echo "ipconfig" > "%OUT_FILE%"

ipconfig /all >> "%OUT_FILE%"

echo "route" >> "%OUT_FILE%"

route print >> "%OUT_FILE%"

echo Check "%OUT_FILE%"

pause
