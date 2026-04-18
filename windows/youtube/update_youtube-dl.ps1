
Set-Location -Path "${PSScriptRoot}"

function downloadGitRelease {
    param (
        [string]$repository,
        [string]$file
    )
    Write-Host -ForegroundColor Cyan "The current time is: $(Get-Date -UFormat "%Y.%m.%d %H:%M:%S")"
    Write-Host -ForegroundColor Cyan "Update repository ${repository}"
    $releases_url = "https://api.github.com/repos/${repository}/releases"
    Write-Host -ForegroundColor Cyan "Get latest release"
    $release_json = Invoke-WebRequest "${releases_url}"
    $release_tag = ("${release_json}" | ConvertFrom-Json)[0].tag_name
    Write-Host -ForegroundColor Cyan "Download latest release: ${release_tag}"
    $wc = New-Object net.webclient
    $wc.Downloadfile("https://github.com/${repository}/releases/download/${release_tag}/${file}", "${file}")
}

# youtube-dl
Stop-Process -Force -Name "youtube-dl" 2>"${NULL}"
downloadGitRelease -repository "ytdl-org/youtube-dl" -file "youtube-dl.exe"

# yt-dlp
Stop-Process -Force -Name "yt-dlp" 2>"${NULL}"
downloadGitRelease -repository "yt-dlp/yt-dlp" -file "yt-dlp.exe"

# FFmpeg
$repository = "BtbN/FFmpeg-Builds"
Write-Host -ForegroundColor Cyan "Update repository ${repository}"
$releases_url = "https://api.github.com/repos/${repository}/releases"
Write-Host -ForegroundColor Cyan "Get latest release"
$release_tag = (Invoke-WebRequest "${releases_url}" | ConvertFrom-Json)[0].tag_name
Write-Host -ForegroundColor Cyan "Dowload latest release: ${release_tag}"
Stop-Process -Force -Name "ffmpeg" 2>"${NULL}"
$folder = "ffmpeg-master-${release_tag}-win64-gpl"
$file = "${folder}.zip"
$wc = New-Object net.webclient
$wc.Downloadfile("https://github.com/${repository}/releases/download/${release_tag}/${file}", "${file}")
Expand-Archive `
    -DestinationPath . `
    -Force `
    "${file}"
foreach ($processName in @("ffmpeg", "ffplay", "ffprobe")) {
    Stop-Process -Force -Name ${processName} 2>"${NULL}"
}
Get-ChildItem `
    -File `
    -Path "${folder}\bin" `
    -Recurse `
| Move-Item `
    -Destination . `
    -Force
Write-Host -ForegroundColor Cyan "Cleanup"
foreach ($path in @("${folder}", "${file}")) {
    Remove-Item `
        -Force `
        -LiteralPath "${path}" `
        -Recurse
}

# deno
$file = "deno-x86_64-pc-windows-msvc.zip"
Stop-Process -Force -Name "deno" 2>"${NULL}"
downloadGitRelease -repository "denoland/deno" -file "${file}"
Expand-Archive `
    -DestinationPath . `
    -Force `
    "${file}"
Write-Host -ForegroundColor Cyan "Cleanup"
Remove-Item `
    -Force `
    -LiteralPath "${file}" `
    -Recurse

# bun
$folder = "bun-windows-x64-baseline-profile"
$file = "${folder}.zip"
Stop-Process -Force -Name "bun" 2>"${NULL}"
downloadGitRelease -repository "oven-sh/bun" -file "${file}"
Expand-Archive `
    -DestinationPath . `
    -Force `
    "${file}"
Get-ChildItem `
    -File `
    -Path "${folder}" `
    -Recurse `
| Move-Item `
    -Destination . `
    -Force
Write-Host -ForegroundColor Cyan "Cleanup"
foreach ($path in @("${folder}", "${file}")) {
    Remove-Item `
        -Force `
        -LiteralPath "${path}" `
        -Recurse
}

# quickjs
Stop-Process -Force -Name "qjs-windows-x86_64" 2>"${NULL}"
downloadGitRelease -repository "quickjs-ng/quickjs" -file "qjs-windows-x86_64.exe"
