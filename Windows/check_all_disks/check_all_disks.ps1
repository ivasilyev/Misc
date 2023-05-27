
$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition
cd $scriptPath

mkdir "logs" -Force

wmic logicaldisk get name /value 2>&1 | ForEach-Object {
    $string = $_.Trim()
    if ( $string.Length -gt 0 ) {
        $letter = $string.Split("=")[-1]
        echo "$letter"
        Start-Process powershell "
            `$Host.UI.RawUI.WindowTitle=`'Check disk $letter`'
            echo 'Check disk $letter'
            chkntfs /c $($letter.ToLower())
            & echo Y | chkdsk /x /f /r $letter 2>&1 | Tee-Object logs\chkdsk-$($letter.Trim(':')).log
            timeout 5
        "
    }
}

pause
