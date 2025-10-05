$repository = 'prometheus/prometheus'
Write-Host 'Update repository $repository' -ForegroundColor Green
$releases_url = "https://api.github.com/repos/$repository/releases"
Write-Host "Determine latest release" -ForegroundColor Green
$release_tag = (Invoke-WebRequest "${releases_url}" | ConvertFrom-Json)[0].tag_name
$trimmed_release_tag = "${release_tag}" -replace "^v" , ""
$folder = "prometheus-${trimmed_release_tag}.windows-amd64"
$file = "${folder}.zip"
Write-Host "Dowload latest release: ${release_tag}"  -ForegroundColor Green
Invoke-WebRequest "https://github.com/$repository/releases/download/${release_tag}/${file}" -OutFile "${file}"
Expand-Archive "${file}" -DestinationPath .
Get-ChildItem -Path "${folder}" -Recurse -File | Move-Item -Force -Destination .
Remove-Item -LiteralPath "${folder}", "${file}" -Force -Recurse
