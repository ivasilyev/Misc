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
    "setup_cygwin.exe"

setup_cygwin.exe ^
    --force-current ^
    --local-package-dir "%CYGWIN_PACKAGES_DIR%" ^
    --only-site ^
    --quiet-mode ^
    --root "%CYGWIN_DIR%" ^
    --site "%SITE%" ^
    --packages ^
        ImageMagick ^
        autoconf ^
        automake ^
        bash-completion ^
        bash-completion-cmake ^
        binutils ^
        build-essential ^
        bzip2 ^
        ca-certificates ^
        chere ^
        cmake ^
        cmake-gui ^
        coreutils ^
        cron ^
        curl ^
        cygutils ^
        diffutils ^
        gcc-core ^
        gcc-g++ ^
        git ^
        gnu-free-fonts ^
        gzip ^
        iperf ^
        jq ^
        lame ^
        lame-mp3x ^
        libboost-devel ^
        libtool ^
        libusb-devel ^
        links ^
        lynx ^
        make ^
        mercurial ^
        nano ^
        openssh ^
        p7zip ^
        patchutils ^
        python3-devel ^
        sshpass ^
        tar ^
        texlive ^
        texlive-collection-fontutils ^
        texlive-collection-latex ^
        tree ^
        unzip ^
        vim ^
        wget ^
        xinit ^
        zip

echo (
timeout 15
