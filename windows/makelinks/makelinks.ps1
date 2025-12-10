param(
    [Parameter(Mandatory=$true)]
    [string] $sourceRoot,

    [Parameter(Mandatory=$true)]
    [string] $targetRoot
)

# Ensure target root exists
if (-not (Test-Path -Path "${targetRoot}" -PathType Container)) {
    New-Item -Path "${targetRoot}" -ItemType Directory | Out-Null
}

# Get first-level directories in source
$sourceDirs = Get-ChildItem -Directory -Path "${sourceRoot}"

foreach ($dir in ${sourceDirs}) {
    $linkName = ${dir}.Name
    $linkPath = Join-Path "${targetRoot}" "${linkName}"

    # If linkPath already exists, skip
    if (Test-Path -LiteralPath "${linkPath}") {
        $existing = Get-Item `
            -ErrorAction SilentlyContinue `
            -Force `
            -LiteralPath "${linkPath}"

        if (${existing}.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            # If it's a symlink — remove
            try {
                Write-Host `
                    -ForegroundColor Yellow `
                    "Remove symlink '${linkPath}'"
                (Get-Item "${linkPath}").Delete()
            }
            catch {
                Write-Warning "Could not remove existing symlink '${linkPath}' — skipping"
                continue
            }
        } else {
            # Exists but not a symlink
            Write-Host `
                -ForegroundColor Gray `
                "Skipping: '${linkName}' already exists in target"
            continue
        }
    }

    # Create junction
    try {
        New-Item -Path "${linkPath}" -ItemType Junction -Target ${dir}.FullName | Out-Null
        Write-Host -ForegroundColor Green "Created junction: '${linkPath}' <-> '$(${dir}.FullName)'"
    }
    catch {
        Write-Warning "Failed to create symlink for '${linkName}': $_"
    }
}
