@echo off
chcp 65001

REM Run this script with elevated permissions
REM Download fresh or not (I personally prefer 2.909) Cygwin binary from:
REM https://cygwin.com/setup-x86_64.exe
REM So it must be in your user's "Downloads" folder

net session >nul 2>&1
if %errorLevel% == 0 (
    echo Success: Administrative permissions confirmed.
) else (
    echo Failure: Administrative permissions required, exiting...
    timeout 15
    exit /B 1
)

set "CYGWIN_DIR=%PROGRAMDATA%/Cygwin"
set "CYGWIN_PACKAGES_DIR=%CYGWIN_DIR%/packages"
set "SITE=http://mirror.team-cymru.com/cygwin/"

mkdir "%CYGWIN_PACKAGES_DIR%"
cd /d "%CYGWIN_DIR%"

copy /Y ^
    "%USERPROFILE%\Downloads\setup-x86_64.exe" ^
    "%CYGWIN_DIR%\setup-x86_64.exe"

setup-x86_64.exe ^
    --force-current ^
    --local-package-dir "%CYGWIN_PACKAGES_DIR%" ^
    --only-site ^
    --quiet-mode ^
    --root "%CYGWIN_DIR%" ^
    --site "%SITE%" ^
    --upgrade-also ^
    --packages ImageMagick ^
    --packages autoconf ^
    --packages automake ^
    --packages bash-completion ^
    --packages bash-completion-cmake ^
    --packages binutils ^
    --packages build-essential ^
    --packages bzip2 ^
    --packages ca-certificates ^
    --packages chere ^
    --packages cmake ^
    --packages cmake-gui ^
    --packages coreutils ^
    --packages cron ^
    --packages curl ^
    --packages cygutils ^
    --packages diffutils ^
    --packages gcc-core ^
    --packages gcc-g++ ^
    --packages git ^
    --packages gnu-free-fonts ^
    --packages gzip ^
    --packages iperf ^
    --packages jq ^
    --packages lame ^
    --packages lame-mp3x ^
    --packages libboost-devel ^
    --packages libtool ^
    --packages libusb-devel ^
    --packages links ^
    --packages lynx ^
    --packages make ^
    --packages mercurial ^
    --packages nano ^
    --packages openssh ^
    --packages p7zip ^
    --packages patchutils ^
    --packages python3-devel ^
    --packages sshpass ^
    --packages tar ^
    --packages texlive ^
    --packages texlive-collection-fontutils ^
    --packages texlive-collection-latex ^
    --packages tree ^
    --packages unzip ^
    --packages vim ^
    --packages wget ^
    --packages xinit ^
    --packages zip

echo (
timeout 15
