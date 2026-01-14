param(
    [Parameter(Mandatory=$true)]
    [string] $videoUrl,

    [Parameter(Mandatory=$true)]
    [string] $downloadFolder
)

# Usage: 
# powershell -NoLogo -ExecutionPolicy Bypass -Command "download_video.ps1 -videoUrl 'https://www.youtube.com/watch?v=xxxxxxxxxxx' -downloadFolder 'C:\playlist'"

$cookiesBrowser = "firefox:sessionId.default-release"

$scriptPath = split-path -parent ${MyInvocation}.MyCommand.Definition
Set-Location -Path "${scriptPath}"

Write-Host "Params: videoUrl='$videoUrl' downloadFolder='$downloadFolder'"
New-Item `
  -Force `
  -ItemType Directory `
  -Path "${downloadFolder}"

$yt = Join-Path "${PSScriptRoot}" "yt-dlp.exe"
&"${yt}" `
  "--abort-on-unavailable-fragment" `
  "--mtime" `
  "--embed-chapters" `
  "--embed-metadata" `
  "--min-sleep-interval=60" `
  "--max-sleep-interval=90" `
  "--sleep-interval=15" `
  "--sleep-requests=3" `
  "--sleep-subtitles=3" `
  "--cookies-from-browser=${cookiesBrowser}" `
  "--match-filter=!is_live" `
  "--no-skip-unavailable-fragments" `
  "--no-abort-on-unavailable-fragments" `
  "--no-skip-unavailable-fragments" `
  "--no-check-certificates" `
  "--retries=100" `
  "--fragment-retries=100" `
  "--add-metadata" `
  "--all-subs" `
  "--convert-subs=ass" `
  "--embed-subs" `
  "--format=bestvideo+bestaudio/best" `
  "--preset-alias=mkv" `
  "--merge-output-format=mkv" `
  "--remux-video=mkv" `
  "--output=${downloadFolder}\%(title)s__%(id)s.%(ext)s" `
  "--verbose" `
  "${videoUrl}"
