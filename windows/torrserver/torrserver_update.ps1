Write-Host "Update FFmpeg" -ForegroundColor Green
$folder = 'ffmpeg-master-latest-win64-gpl'
$archive = "$folder.zip"
Invoke-WebRequest "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/$archive" -OutFile "$archive"
Expand-Archive "$archive" -DestinationPath .
Get-ChildItem -Path "$folder\bin" -Recurse -File | Move-Item -Destination .
Remove-Item -LiteralPath "$folder", "$archive" -Force -Recurse

$repository = 'YouROK/TorrServer'
$file = 'TorrServer-windows-amd64.exe'
Write-Host 'Update repository $repository' -ForegroundColor Green
$releases_url = "https://api.github.com/repos/$repository/releases"
Write-Host "Determine latest release" -ForegroundColor Green
$release_tag = (Invoke-WebRequest "$releases_url" | ConvertFrom-Json)[0].tag_name
Write-Host "Dowload latest release: $release_tag"  -ForegroundColor Green
Invoke-WebRequest "https://github.com/$repository/releases/download/$release_tag/$file" -OutFile "$file"
