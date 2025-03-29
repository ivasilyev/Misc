
Write-Host "Check permisions" -ForegroundColor Cyan

if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Not running as administrator! Please run as admin." -ForegroundColor Red
    exit
}

$url = "https://www.cygwin.com/setup-x86_64.exe"
$basename = $url.split("/")[-1]
$directory = "$Env:PROGRAMDATA\Cygwin"
$file = "$directory\$basename"
$packages_directory = "$directory\packages"
$mirror_url = "http://mirror.team-cymru.com/cygwin/"

Write-Host "Create directories" -ForegroundColor Cyan
New-Item -ItemType Directory -Path "$directory" -Force | Out-Null
Set-Location -Path "$directory"

Write-Host "Download assets" -ForegroundColor Cyan
$client = New-Object System.Net.WebClient
$client.DownloadFile($url, $file)

Write-Host "Instal software" -ForegroundColor Cyan
Start-Process -NoNewWindow -FilePath $file -ArgumentList `
    "--force-current",
    "--local-package-dir `"$packages_directory`"",
    "--only-site",
    "--quiet-mode",
    "--root `"$directory`"",
    "--site `"$mirror_url`"",
    "--upgrade-also",
    "--packages ImageMagick",
    "--packages autoconf",
    "--packages automake",
    "--packages bash-completion",
    "--packages bash-completion-cmake",
    "--packages binutils",
    "--packages build-essential",
    "--packages bzip2",
    "--packages ca-certificates",
    "--packages chere",
    "--packages cmake",
    "--packages cmake-gui",
    "--packages coreutils",
    "--packages cron",
    "--packages curl",
    "--packages cygutils",
    "--packages diffutils",
    "--packages gcc-core",
    "--packages gcc-g++",
    "--packages git",
    "--packages gnu-free-fonts",
    "--packages gzip",
    "--packages iperf",
    "--packages jq",
    "--packages lame",
    "--packages lame-mp3x",
    "--packages libboost-devel",
    "--packages libtool",
    "--packages libusb-devel",
    "--packages links",
    "--packages lynx",
    "--packages make",
    "--packages mercurial",
    "--packages nano",
    "--packages openssh",
    "--packages p7zip",
    "--packages patchutils",
    "--packages python3-devel",
    "--packages sshpass",
    "--packages tar",
    "--packages texlive",
    "--packages texlive-collection-fontutils",
    "--packages texlive-collection-latex",
    "--packages tree",
    "--packages unzip",
    "--packages vim",
    "--packages wget",
    "--packages xinit",
    "--packages zip"
