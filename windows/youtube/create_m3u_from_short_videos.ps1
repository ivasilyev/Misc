param(
    [Parameter(Mandatory=$true)]
    [string] $folderPath,

    [Parameter(Mandatory=$true)]
    [string] $playlistPath
)
$thresholdMinutes = 5

# Create a new COM Shell object
$shell = New-Object -ComObject Shell.Application

# Prepare to write the playlist file
"`#EXTM3U" | Out-File -FilePath ${playlistPath} -Encoding UTF8

# Get all .mkv files in the folder (non-recursive; remove -Recurse if you want subfolders)
Get-ChildItem -Path ${folderPath} -Filter *.mkv -File | ForEach-Object {
    $file = $_
    # Get the folder namespace for the file's directory
    $ns   = ${shell}.Namespace(${file}.DirectoryName)
    $item = ${ns}.ParseName(${file}.Name)
    # The magic index (27) is used for "Length/Duration" metadata in many cases
    $durationStr = ${ns}.GetDetailsOf($item, 27)
    if ([string]::IsNullOrWhiteSpace(${durationStr})) {
        # could not read duration ⇒ skip
        return
    }

    # Parse durationStr which is typically "hh:mm:ss" or "mm:ss"
    # Convert to [TimeSpan]
    try {
        $ts = [TimeSpan]::Parse(${durationStr})
    }
    catch {
        # If parse fails (maybe format is mm:ss), attempt fallback
        if (${durationStr} -match '^(?<m>\d+):(?<s>\d+)$') {
            $ts = New-Object TimeSpan 0, [int]${matches}['m'], [int]${matches}['s']
        }
        else {
            # Unknown format ⇒ skip
            return
        }
    }

    # Check if duration ≤ n minutes
    if (${ts}.TotalMinutes -le ${thresholdMinutes}) {
        # Write entry to the playlist: you can optionally include #EXTINF line
        # #EXTINF:<seconds>,<title>
        $seconds = [int]${ts}.TotalSeconds
        $title   = ${file}.BaseName
        "#EXTINF:${seconds},${title}" | Out-File -FilePath "${playlistPath}" -Encoding UTF8 -Append
        ${file}.FullName        | Out-File -FilePath "${playlistPath}" -Encoding UTF8 -Append
        Write-Host "Added short file: "$(${file}.Name)" – Duration: ${durationStr}"
    }
    else {
        Write-Host "Skipped (too long): "$($file.Name)" – Duration: ${durationStr}"
    }
}

Write-Host -ForeGroundColor Green "Playlist created: ${playlistPath}"
