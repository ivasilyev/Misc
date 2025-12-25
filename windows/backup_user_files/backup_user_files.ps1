Set-Location -Path "${PSScriptRoot}"
$destinationPath = "${PSScriptRoot}\$env:USERNAME"

Write-Host "${destinationPath}"
New-Item -ItemType Directory -Force -Path "${destinationPath}" | Out-Null

$msg = "Backup"
$documents = [Environment]::GetFolderPath('MyDocuments')
$desktop = [Environment]::GetFolderPath('Desktop')
$appDataRoaming = $env:APPDATA
$appDataLocal = $env:LOCALAPPDATA

Write-Host "${msg}"
${Host}.UI.RawUI.WindowTitle = ${msg}

# Use Robocopy for a more robust copy operation
# Options:
# /E (copy subdirectories including empty ones),
# /ZB (use restartable mode; if access denied, use backup mode),
Robocopy "${documents}" "${destinationPath}\Documents" /E /ZB /R:1 /W:1 | Out-Null
Robocopy "${desktop}" "${destinationPath}\Desktop" /E /ZB /R:1 /W:1 | Out-Null
Robocopy "${appDataRoaming}" "$destinationPath\AppDataRoaming" /E /ZB /R:1 /W:1 | Out-Null
Robocopy "${appDataLocal}" "${destinationPath}\AppDataLocal" /E /ZB /R:1 /W:1 | Out-Null

Write-Host "${msg} complete"
