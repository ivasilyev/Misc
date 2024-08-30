@echo off

REM Run this script with elevated permissions

set "SEP=------------------------------------------"

echo %SEP%
echo Sync directories content. Requires escalation!
echo %SEP%
echo(

echo(
echo %SEP%
echo Enter source:
echo %SEP%
set /p "SRC="
echo(

echo(
echo %SEP%
echo Enter destination:
echo %SEP%
set /p "DST="
echo(

echo(
echo %SEP%
echo Sync between "%SRC%" and "%DST%"...
echo %SEP%
echo(

timeout 10

echo(

for /D %%i in ("%SRC%\"*) do (
    echo Copying "%%~ni"
    Robocopy "%%i" "%DST%\%%~ni" /DCOPY:T /COPYALL /E /R:5
)

echo(

echo(
echo %SEP%
echo Done syncing between "%SRC%" and "%DST%"
echo %SEP%
echo(

timeout 15
