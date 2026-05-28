param(
  [Parameter(Mandatory=$true)]
  [string] $folderPath,

  [Parameter(Mandatory=$true)]
  [string] $playlistPath
)

# Usage: 
# powershell -NoLogo -ExecutionPolicy Bypass -Command "create_m3u_from_short_videos.ps1 -folderPath 'C:\video' -playlistPath 'C:\playlist.m3u'"

$thresholdSeconds = 5 * 60
$ffprobePath = ".\ffprobe.exe"

$scriptPath = split-path -parent ${MyInvocation}.MyCommand.Definition
Set-Location -Path "${scriptPath}"

# Create a new COM Shell object
$shell = New-Object -ComObject Shell.Application

# Prepare to write the playlist file
"`#EXTM3U" | Out-File -FilePath "${playlistPath}" -Encoding UTF8

# Get all files recursively and store them in an array
$files = Get-ChildItem `
  -File `
  -Path "${folderPath}" `
  -Recurse

# Loop through each file and print its absolute path (FullName)
foreach ($file in ${files}) {
  if (! (${file}.Extension -in ".mkv", ".avi", ".mp4" ) ) {
    continue
  }

  $fullName = ${file}.FullName
  Write-Host -ForeGroundColor White "Processing file ${fullName}"
  # Check if duration ≤ n minutes
  $durationString = &"${ffprobePath}" -i "${fullName}" -show_format -v quiet | Select-String -Pattern 'duration'
  $found = "${durationString}" -match '(?<=duration\=).+(?=\.)'

  if ( ${found} ) {
    $durationSeconds = [int]${matches}[0]
    Write-Host -ForeGroundColor Gray $durationSeconds
  }

  if ( ${durationSeconds} -gt ${thresholdSeconds} ) {
    Write-Host "Skipped (too long): '${fullName}' - Duration: ${durationSeconds}s."
    continue
  }

  # Write entry lines to the playlist
  # #EXTINF:<seconds>,<title>
  "#EXTINF:${durationSeconds},${file}" | Out-File -FilePath "${playlistPath}" -Encoding UTF8 -Append
  # <url>
  "${fullName}" | Out-File -FilePath "${playlistPath}" -Encoding UTF8 -Append
  Write-Host -ForeGroundColor Cyan "Added short file: '${fullName}' - Duration: ${durationSeconds}s."
}

Write-Host -ForeGroundColor Green "Playlist created: ${playlistPath}"
