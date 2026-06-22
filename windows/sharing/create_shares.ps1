# Create the share folder

# Get all disks with assigned drive letters
$disks = Get-Volume `
| Where-Object { $_.DriveLetter -match "^[A-Z]$" } `
| Sort-Object DriveLetter

# Define folder name
$folderName = "Share"

# Define user to grant access
# $user = "user"
$user = "$(whoami)"

foreach ($disk in ${disks}) {
    Write-Host "Process disk ${disk}" -ForegroundColor Gray
    # Define full folder path
    $letter = "$($disk.DriveLetter)"
    $folderPath = "${letter}:\${folderName}"

    if (${letter} -eq $($($Env:SYSTEMDRIVE)[0])) {
        Write-Host "Cancel sharing the one on the system drive" -ForegroundColor Yellow
        continue
    }

    # Create the folder if it doesn't exist
    if (!(Test-Path -Path "${folderPath}")) {
        New-Item -Path "${folderPath}" -ItemType Directory | Out-Null
        Write-Host "Created folder: ${folderPath}" -ForegroundColor Green
    } else {
        Write-Host "Folder already exists: ${folderPath}" -ForegroundColor Yellow
    }

    # Grant NTFS permissions to the user
    icacls "${folderPath}" /grant "${user}:(OI)(CI)(F)" /T /C

    # Revoke NTFS permissions from the other users
    icacls "${folderPath}" /remove "Everyone" /inheritance:r

    # Restore some of NTFS permissions
    icacls "${folderPath}" /grant "Administrators:(OI)(CI)(F)" /T /C
    icacls "${folderPath}" /grant "SYSTEM:(OI)(CI)(F)" /T /C

    Write-Host "Granted NTFS permissions to '$user' on $folderPath" -ForegroundColor Green

    # Share the folder under the most compact name including the drive letter only
    $shareName = $("${letter}").ToLower()
    if (Get-SmbShare -Name "${shareName}" -ErrorAction SilentlyContinue) {
        Write-Host "Share ${shareName} already exists" -ForegroundColor Yellow
        Remove-SmbShare -Name "${shareName}" -Force
    }
    New-SmbShare `
        -Name "${shareName}" `
        -Description "Share on the disk ${letter}" `
        -Path "${folderPath}" `
        -FullAccess "${user}"
    Write-Host "Shared ${folderPath} as ${shareName} with full access for '$user'" -ForegroundColor Green

    # Remove access for "Everyone" from the share permissions
    Revoke-SmbShareAccess -Name "${shareName}" -AccountName "Everyone" -Force

    Write-Host "Removed 'Everyone' from share access of ${shareName}" -ForegroundColor Green
}

Write-Host "All disks processed successfully!" -ForegroundColor Cyan
