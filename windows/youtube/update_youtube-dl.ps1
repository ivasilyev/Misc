
Set-Location -Path "${PSScriptRoot}"

$repository = "ytdl-org/youtube-dl"
Write-Host -ForegroundColor Cyan "Update repository ${repository}"
$releases_url = "https://api.github.com/repos/${repository}/releases"
Write-Host -ForegroundColor Cyan "Get latest release" 
$release_tag = (Invoke-WebRequest "${releases_url}" | ConvertFrom-Json)[0].tag_name
Write-Host -ForegroundColor Cyan "Dowload latest release: ${release_tag}"
$file = "youtube-dl.exe"
Stop-Process -Force -Name youtube-dl 2>"${NULL}"
Invoke-WebRequest "https://github.com/${repository}/releases/download/${release_tag}/${file}" -OutFile "${file}"

$repository = "yt-dlp/yt-dlp"
Write-Host -ForegroundColor Cyan "Update repository ${repository}"
$releases_url = "https://api.github.com/repos/${repository}/releases"
Write-Host -ForegroundColor Cyan "Get latest release" 
$release_tag = (Invoke-WebRequest "${releases_url}" | ConvertFrom-Json)[0].tag_name
Write-Host -ForegroundColor Cyan "Dowload latest release: ${release_tag}"
$file = "yt-dlp.exe"
Stop-Process -Force -Name yt-dlp 2>"${NULL}"
Invoke-WebRequest "https://github.com/${repository}/releases/download/${release_tag}/${file}" -OutFile "${file}"

$repository = "BtbN/FFmpeg-Builds"
Write-Host -ForegroundColor Cyan "Update repository ${repository}"
$releases_url = "https://api.github.com/repos/${repository}/releases"
Write-Host -ForegroundColor Cyan "Get latest release"
$release_tag = (Invoke-WebRequest "${releases_url}" | ConvertFrom-Json)[0].tag_name
Write-Host -ForegroundColor Cyan "Dowload latest release: ${release_tag}"
$folder = "ffmpeg-master-${release_tag}-win64-gpl"
$file = "${folder}.zip"
Invoke-WebRequest "https://github.com/${repository}/releases/download/${release_tag}/${file}" -OutFile "${file}"
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

$repository = "denoland/deno"
Write-Host -ForegroundColor Cyan "Update repository ${repository}"
$releases_url = "https://api.github.com/repos/${repository}/releases"
Write-Host -ForegroundColor Cyan "Get latest release"
$release_tag = (Invoke-WebRequest "${releases_url}" | ConvertFrom-Json)[0].tag_name
Write-Host -ForegroundColor Cyan "Dowload latest release: ${release_tag}"
$file = "deno-x86_64-pc-windows-msvc.zip"
Invoke-WebRequest "https://github.com/${repository}/releases/download/${release_tag}/${file}" -OutFile "${file}"
Stop-Process -Force -Name deno 2>"${NULL}"
Expand-Archive `
  -DestinationPath . `
  -Force `
  "${file}"
Remove-Item `
  -Force `
  -LiteralPath "${file}" `
  -Recurse
