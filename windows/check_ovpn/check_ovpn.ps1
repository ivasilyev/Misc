# Define variables
$vpnProfile = "MyCon.ovpn"
$openVpnGuiPath = "$Env:programfiles\OpenVPN\bin\openvpn-gui.exe"
$vpnConnectionName = "OpenVPN TAP-Windows6"
$vpnConnectionLine = netsh int ipv4 show interfaces | findstr /C:"$vpnConnectionName"
$vpnConnectionStatus = $vpnConnectionLine -Match " connected "

if ($vpnConnectionStatus) {
    Write-Host "VPN connection is active." -ForegroundColor Green
} else {
    Write-Host "VPN connection is DOWN! Restarting OpenVPN..." -ForegroundColor Red

    Write-Host "Kill all OpenVPN processes using taskkill"
    cmd /c "taskkill /F /IM openvpn.exe /IM openvpn-gui.exe"

    Write-Host "Start OpenVPN GUI with the connection profile"
    Start-Process -FilePath $openVpnGuiPath -ArgumentList "--connect `"$vpnProfile`"" -NoNewWindow

    Write-Host "OpenVPN restarted with profile: $vpnProfile" -ForegroundColor Yellow
}
