param(
    [Parameter(Mandatory=$true)]
    [string] $playlistUrl,

    [Parameter(Mandatory=$true)]
    [string] $downloadFolder,

    [Parameter(Mandatory=$true)]
    [string] $videoUrlPrefix
)

# Usage: 
# powershell -NoLogo -ExecutionPolicy Bypass -Command "download_playlist.ps1 -playlistUrl 'https://www.youtube.com/@playlist/videos' -downloadFolder 'C:\playlist' -videoUrlPrefix 'https://www.youtube.com/watch?v='"

$cookiesBrowser = "firefox:sessionId.default-release"

$videoUrlPrefix=${videoUrlPrefix}.Trim()
$timestamp = Get-Date -Format "yyyy-MM-dd-HH-mm-ss"
$tempFile = Join-Path -Path $env:TEMP -ChildPath ("yt_ids_{0}.txt" -f "${timestamp}")
$yt = Join-Path "${PSScriptRoot}" "yt-dlp.exe"

Write-Host -ForegroundColor Cyan "Params: playlistUrl='${playlistUrl}' downloadFolder='${downloadFolder}' videoUrlPrefix='${videoUrlPrefix}'"

Write-Host -ForegroundColor Cyan "Get video IDs to temp file: '${tempFile}'"
Write-Host -ForegroundColor Cyan "The current time is: $(Get-Date -UFormat "%Y.%m.%d %H:%M:%S")"
Set-Location -Path "${PSScriptRoot}"
&"${yt}" `
    "--cookies-from-browser=${cookiesBrowser}" `
    "--ignore-errors" `
    "--flat-playlist" `
    "--print-to-file=%(id)s" `
    "${tempFile}" `
    "${playlistUrl}"
#     "--proxy=socks5://127.0.0.1:1080" `

Write-Host -ForegroundColor Cyan "Saved video IDs to temp file: '${tempFile}'"

$ids = Get-Content -Path "${tempFile}" | Where-Object { $_.Trim().Length -gt 0 }
New-Item -ItemType Directory -Force -Path "${downloadFolder}"
$downloader = Join-Path "${PSScriptRoot}" "download_video.ps1"
foreach ($id in $ids) {
    $exists = Get-ChildItem `
        -Path "${downloadFolder}" `
        -Recurse `
        -Filter "*__${id}.mkv" `
        -File `
        -ErrorAction SilentlyContinue
    if (!$exists) {
        Write-Host -ForegroundColor Green "Download ID '${id}'"
        $videoUrl = "${videoUrlPrefix}${id}"
        &"${downloader}" -videoUrl "${videoUrl}" -downloadFolder "${downloadFolder}"
    } else {
        Write-Host -ForegroundColor Yellow "Skip ID '${id}'"
    }
}

Write-Host -ForegroundColor Cyan "Remove temp file '${tempFile}'"
Remove-Item -Path "${tempFile}" -ErrorAction SilentlyContinue
