
Set-Location -Path "${PSScriptRoot}"

mkdir "logs" -Force

wmic logicaldisk get name /value 2>&1 | ForEach-Object {
    $string = $_.Trim()
    if ( ${string}.Length -gt 0 ) {
        $letter = $string.Split("=")[-1]
        if ( ${letter}.equals("C:") ) {
            # Do not check the system disk
            Write-Host -ForegroundColor Gray "Skip ${letter}";
        } else {
            Start-Process powershell "
                `$logFile = 'logs\chkdsk-$($letter.Trim(':')).log'
                `$msg = 'Check disk ${letter}';
                `${Host}.UI.RawUI.WindowTitle=`${msg};
                Write-Host -ForegroundColor Cyan `"`${msg}`";
                chkntfs /c ${letter}.ToLower() 2>&1 | Tee-Object '${logFile}';
                & echo Y | chkdsk /x /f /r $letter 2>&1 | Tee-Object '${logFile}';
                Start-Sleep -Seconds 5;
            "
        }
    }
}

Write-Host -NoNewLine "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
