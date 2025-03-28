# Define variables
# Not using "$Env:USERPROFILE" here
$userName = "User"
$vpnProfile = "MyCon"
$vpnProfileFile = "C:\Users\$userName\OpenVPN\config\$vpnProfile.ovpn"
$vpnLogFile = "C:\Users\$userName\OpenVPN\log\$vpnProfile.log"
$openVpnDirectoryPath = "$Env:PROGRAMFILES\OpenVPN\bin"
$vpnConnectionName = "OpenVPN TAP-Windows6"
$vpnConnectionLine = netsh int ipv4 show interfaces | findstr /C:"$vpnConnectionName"
$vpnConnectionStatus = $vpnConnectionLine -Match " connected "

if ($vpnConnectionStatus) {
    Write-Host "VPN connection is active." -ForegroundColor Green
} else {
    Write-Host "VPN connection is down! Restarting OpenVPN..." -ForegroundColor Red

    Write-Host "Kill all OpenVPN processes using taskkill"
    cmd /c "taskkill /F /IM openvpn.exe /IM openvpn-gui.exe"

    Write-Host "Start OpenVPN GUI with the connection profile"
    # Start-Process -FilePath $openVpnDirectoryPath\openvpn-gui.exe -ArgumentList "--connect `"$vpnProfileFile`"" -NoNewWindow
    Start-Process -FilePath $openVpnDirectoryPath\openvpn.exe -ArgumentList "--config `"$vpnProfileFile`" --log `"$vpnLogFile`"" -NoNewWindow

    Write-Host "OpenVPN restarted with profile: $vpnProfile" -ForegroundColor Yellow
}
