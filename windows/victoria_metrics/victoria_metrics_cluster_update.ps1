$repository = "VictoriaMetrics/VictoriaMetrics"
Write-Host -ForegroundColor Cyan "Update repository ${repository}"
$releases_url = "https://api.github.com/repos/${repository}/releases"
Write-Host -ForegroundColor Cyan "Determine latest release"
$release_tag = (Invoke-WebRequest "${releases_url}" | ConvertFrom-Json)[0].tag_name
# $release_tag = "v1.126.0"
Write-Host -ForegroundColor Cyan "Dowload latest release: ${release_tag}"

$folder = "victoria-metrics-windows-amd64-${release_tag}-cluster"
$file = "${folder}.zip"
Invoke-WebRequest `
    "https://github.com/${repository}/releases/download/${release_tag}/${file}" `
    -OutFile "${file}"
Expand-Archive "${file}" `
    -DestinationPath . `
    -Force
Remove-Item -LiteralPath "${file}" -Force -Recurse

$folder = "vmutils-windows-amd64-${release_tag}"
$file = "${folder}.zip"
Invoke-WebRequest `
    "https://github.com/${repository}/releases/download/${release_tag}/${file}" `
    -OutFile "${file}"
Expand-Archive "${file}" `
    -DestinationPath . `
    -Force
Remove-Item -LiteralPath "${file}" -Force -Recurse
