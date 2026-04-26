
Set-Location -Path "${PSScriptRoot}"

$maxRetries = 5
$baseDelay = 2  # Initial wait in seconds

function downloadFile() {
    param (
        [string]$url,
        [string]$file
    )
    foreach ($attempt in 1..${maxRetries}) {
        $webClient = New-Object System.Net.WebClient
        try {
            Write-Host "Download ${url} for attempt ${attempt} of ${maxRetries}" -ForegroundColor Cyan
            ${webClient}.DownloadFile("${url}", "${file}")
            Write-Host "Downloaded ${file}" -ForegroundColor Cyan
            return  # Exit the script/function upon success
        }
        catch {
            Write-Warning "Attempt $attempt failed: $($_.Exception.Message)"

            if ($attempt -lt $maxRetries) {
                # Exponential Backoff: 2^1 * 2 = 4s, 2^2 * 2 = 8s, etc.
                $delay = [Math]::Pow(2, ${attempt}) * ${baseDelay}
                Write-Host "Waiting ${delay} seconds before next retry..." -ForegroundColor Yellow
                Start-Sleep -Seconds ${delay}
            }
            else {
                Write-Error "Final attempt failed. Manual intervention required."
            }
        }
        finally {
            if (${webClient}) { ${webClient}.Dispose() }
        }
    }
}


function getReleaseTag() {
    param (
        [string]$url
    )
    foreach ($attempt in 1..${maxRetries}) {
        $webClient = New-Object System.Net.WebClient
        try {
            Write-Host -ForegroundColor Cyan "Get latest release"
            $release_json = Invoke-WebRequest "${url}"
            $release_tag = ("${release_json}" | ConvertFrom-Json)[0].tag_name
            return ${release_tag} # Exit the script/function upon success
        }
        catch {
            Write-Warning "Attempt $attempt failed: $($_.Exception.Message)"
            if ($attempt -lt $maxRetries) {
                # Exponential Backoff: 2^1 * 2 = 4s, 2^2 * 2 = 8s, etc.
                $delay = [Math]::Pow(2, ${attempt}) * ${baseDelay}
                Write-Host "Waiting ${delay} seconds before next retry..." -ForegroundColor Yellow
                Start-Sleep -Seconds ${delay}
            }
            else {
                Write-Error "Final attempt failed. Manual intervention required."
            }
        }
    }
    return "latest"
}


function downloadGitRelease {
    param (
        [string]$repository,
        [string]$file
    )
    Write-Host -ForegroundColor Cyan "The current time is: $(Get-Date -UFormat "%Y.%m.%d %H:%M:%S")"
    Write-Host -ForegroundColor Cyan "Update repository ${repository}"
    $releases_url = "https://api.github.com/repos/${repository}/releases"
    $release_tag = getReleaseTag -url "${releases_url}"
    Write-Host -ForegroundColor Cyan "Download latest release: ${release_tag}"
    $url = "https://github.com/${repository}/releases/download/${release_tag}/${file}"
    downloadFile -url "${url}" -file "${file}"
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
downloadFile -url "https://github.com/${repository}/releases/download/${release_tag}/${file}" -file "${file}"
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
