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

$scriptPath = split-path -parent ${MyInvocation}.MyCommand.Definition
Set-Location -Path "${scriptPath}"

$videoUrlPrefix=${videoUrlPrefix}.Trim()

Write-Host "Params: playlistUrl='${playlistUrl}' downloadFolder='${downloadFolder}' videoUrlPrefix='${videoUrlPrefix}'"

$timestamp = Get-Date -Format "yyyy-MM-dd-HH-mm-ss"
$tempFile = Join-Path -Path $env:TEMP -ChildPath ("yt_ids_{0}.txt" -f "${timestamp}")

$yt = Join-Path "${PSScriptRoot}" "yt-dlp.exe"
&"${yt}" `
  "--cookies-from-browser=${cookiesBrowser}" `
  "--ignore-errors" `
  "--flat-playlist" `
  "--print-to-file=%(id)s" `
  "${tempFile}" `
  "${playlistUrl}"

Write-Host "Saved video IDs to temp file: '${tempFile}'"

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
    Write-Host -ForegroundColor Cyan "Skip ID '${id}'"
  }
}

Write-Host "Remove temp file '${tempFile}'"
Remove-Item -Path "${tempFile}" -ErrorAction SilentlyContinue
