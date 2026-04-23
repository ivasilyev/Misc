Set-Location -Path "$PSScriptRoot"

Write-Host "Scan broken links into the directory: $PWD" -ForegroundColor Cyan

$links = Get-ChildItem -Path . -Recurse -Force | Where-Object { $_.Attributes -match "ReparsePoint" }

foreach ($link in ${links}) {
    $target = (Get-Item ${link}).Target
    if (-not (Test-Path -Path "${target}")) {
        try {
            Remove-Item -Path ${link}.FullName -Force -ErrorAction Stop
            Write-Host "Removed broken link: $(${link}.FullName)" -ForegroundColor Yellow
        }
        catch {
            Write-Warning "Unable to remove broken link $(${link}.FullName): $($_.Exception.Message)"
        }
    }
}

Write-Host "Done" -ForegroundColor Green
