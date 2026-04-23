# Find & remove all symlinks

Get-ChildItem -Path . | Where-Object { $_.Attributes -match "ReparsePoint" } | Remove-Item -Force -Recurse
