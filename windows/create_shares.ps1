# Create the share folder

# Get all disks with assigned drive letters
$disks = Get-Volume | Where-Object { $_.DriveLetter -match "^[A-Z]$" }

# Define folder name
$folderName = "Share"

# Define user to grant access
$user = "user"

foreach ($disk in $disks) {
    # Define full folder path
    $letter = "$($disk.DriveLetter)"
    $folderPath = "${letter}:\$folderName"

    # Create the folder if it doesn't exist
    if (!(Test-Path -Path $folderPath)) {
        New-Item -Path $folderPath -ItemType Directory | Out-Null
        Write-Host "Created folder: $folderPath" -ForegroundColor Green
    } else {
        Write-Host "Folder already exists: $folderPath" -ForegroundColor Yellow
    }

    # Grant NTFS permissions to the user
    icacls "${folderPath}" /grant "${user}:(OI)(CI)(F)" /T /C

    # Revoke NTFS permissions from the other users
    icacls "${folderPath}" /remove "Everyone" /inheritance:r

    # Restore some of NTFS permissions
    icacls "${folderPath}" /grant "Administrators:(OI)(CI)(F)" /T /C
    icacls "${folderPath}" /grant "SYSTEM:(OI)(CI)(F)" /T /C

    Write-Host "Granted NTFS permissions to '$user' on $folderPath" -ForegroundColor Green

    # Share the folder
    $shareName = $("${folderName}-${letter}").ToLower()
    if (Get-SmbShare -Name $shareName -ErrorAction SilentlyContinue) {
        Write-Host "Share $shareName already exists" -ForegroundColor Yellow
    }

    # Remove access for "Everyone" from the share permissions
    Revoke-SmbShareAccess -Name $shareName -AccountName "Everyone" -Force

    Write-Host "Removed 'Everyone' from share access of $shareName" -ForegroundColor Green
}

# Stop sharing the one on the system drive
Remove-SmbShare -Name $("$folderName-$($($Env:SYSTEMDRIVE)[0])").ToLower() -Force

Write-Host "All disks processed successfully!" -ForegroundColor Cyan
