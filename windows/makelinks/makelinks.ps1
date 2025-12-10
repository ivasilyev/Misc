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
        Write-Host -ForegroundColor Gray "Skipping: '${linkName}' already exists in target."
        continue
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
