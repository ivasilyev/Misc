@echo off
set BAR=========================================================================

echo(
echo %BAR%
echo Enter video (or playlist) URL: 
echo %BAR%
echo(
echo(
echo(

set /p URL=
echo(
echo(
echo(

rem Download youtube-dl: https://yt-dl.org/downloads/latest/youtube-dl.exe
rem Download ffdshow: https://ffmpeg.zeranoe.com/builds/
rem Put youtube-dl.exe and ffdshow.exe into the same folder!
rem Windows executable binary files require Microsoft Visual C++ 2010 Redistributable Package (x86) 

echo %BAR%
echo Downloading video with highest quality.
echo %BAR%
echo(
echo(
echo(

cd /D "%~dp0"
rem mkdir download
rem youtube-dl.exe --verbose --all-subs -f bestvideo+bestaudio/best -o download\%%(title)s__%%(id)s.%%(ext)s "%URL%" 
rem echo Done, check the folder: '%cd%\download'.
rem set DL_DIR="%HOMEDRIVE%%HOMEPATH%\Videos\youtube-dl"

set "DL_DIR=%USERPROFILE%\Videos\youtube-dl"


mkdir %DL_DIR%

yt-dlp.exe ^
    --abort-on-unavailable-fragment ^
    --embed-chapters ^
    --embed-metadata ^
    --no-skip-unavailable-fragments ^
    --no-check-certificates ^
    --retries 100 ^
    --add-metadata ^
    --all-subs ^
    --convert-subs=ass ^
    --embed-subs ^
    --format bestvideo+bestaudio/best ^
    --preset-alias mkv ^
    --merge-output-format mkv ^
    --remux-video mkv ^
    --output "%DL_DIR%\%%(title)s__%%(id)s.%%(ext)s" ^
    --verbose "%URL%"


rem ^  --restrict-filenames

echo(
echo(
echo(

echo %BAR%
echo Done, check the folder: %DL_DIR%
echo %BAR%
echo(
echo(
echo(

start "" %DL_DIR%
pause
