param(
    [Parameter(Mandatory=$true)]
    [string] $playlistUrl,

    [Parameter(Mandatory=$true)]
    [string] $downloadFolder
)

# Usage: 
# powershell -NoLogo -ExecutionPolicy Bypass -Command "download_playlist.ps1 -playlistUrl 'https://www.youtube.com/@playlist/videos' -downloadFolder 'C:\playlist'"

Write-Host "Params: playlistUrl=$playlistUrl downloadFolder=$downloadFolder"

$yt = "yt-dlp.exe"

$timestamp = Get-Date -Format "yyyy-MM-dd-HH-mm-ss"
$tempFile = Join-Path -Path $env:TEMP -ChildPath ("yt_ids_{0}.txt" -f "${timestamp}")

&"${yt}" `
	'--ignore-errors' `
	'--flat-playlist' `
	'--print-to-file' "%(id)s" `
	"${tempFile}" `
	"${playlistUrl}"

Write-Host "Saved video IDs to temp file: '${tempFile}'"

$ids = Get-Content -Path "${tempFile}" | Where-Object { $_.Trim().Length -gt 0 }
New-Item -ItemType Directory -Force -Path "${downloadFolder}"

foreach ($id in $ids) {
    $exists = Get-ChildItem `
		-Path "${downloadFolder}" `
		-Recurse `
		-Filter "*__${id}.mkv" `
		-File `
		-ErrorAction SilentlyContinue
    if (!$exists) {
        Write-Host -ForegroundColor Green "Download ID '${id}'"
        $videoUrl = "https://www.youtube.com/watch?v=${id}"
		&"${yt}" `
			'--abort-on-unavailable-fragment' `
			'--mtime' `
			'--embed-chapters' `
			'--embed-metadata' `
			'--min-sleep-interval=60' `
			'--max-sleep-interval=90' `
			'--sleep-interval=15' `
			'--sleep-requests=3' `
			'--sleep-subtitles=3' `
			'--proxy=socks5://127.0.0.1:8080' `
			'--cookies-from-browser=firefox:12345678.default-release' `
			'--no-skip-unavailable-fragments' `
			'--no-abort-on-unavailable-fragments' `
			'--no-skip-unavailable-fragments' `
			'--no-check-certificates' `
			'--retries=100' `
			'--fragment-retries=100' `
			'--add-metadata' `
			'--all-subs' `
			'--convert-subs=ass' `
			'--embed-subs' `
			'--format=bestvideo+bestaudio/best' `
			'--preset-alias=mkv' `
			'--merge-output-format=mkv' `
			'--remux-video=mkv' `
			'--output' `
			"${downloadFolder}\%(title)s__%(id)s.%(ext)s" `
			'--verbose' `
			"${videoUrl}"
    } else {
        Write-Host -ForegroundColor Cyan "Skip ID '${id}'"
    }
}

Write-Host "Remove temp file '${tempFile}'"
Remove-Item -Path "${tempFile}" -ErrorAction SilentlyContinue
