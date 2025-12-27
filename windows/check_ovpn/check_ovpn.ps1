# Define variables
# Not using "$Env:USERPROFILE" here
$userName = "User"
$vpnProfile = "MyCon"
$vpnProfileFile = "C:\Users\$userName\OpenVPN\config\${vpnProfile}.ovpn"
$vpnLogFile = "C:\Users\$userName\OpenVPN\log\${vpnProfile}.log"
$openVpnDirectoryPath = "$Env:PROGRAMFILES\OpenVPN\bin"
$vpnConnectionName = "OpenVPN TAP-Windows6"
$vpnConnectionLine = netsh int ipv4 show interfaces | findstr /C:"${vpnConnectionName}"
$vpnConnectionStatus = ${vpnConnectionLine} -Match " connected "

if ($vpnConnectionStatus) {
  Write-Host -ForegroundColor Green "VPN connection is active."
} else {

  Write-Host -ForegroundColor Red "VPN connection is DOWN! Restarting OpenVPN..."
  foreach ($serviceName in ("OpenVPNServiceInteractive", "OpenVPNService")) {
    Write-Host "Stop and disable OpenVPN service `"$serviceName`"" -ForegroundColor Yellow
    cmd /c "sc stop `"${serviceName}`""
    cmd /c "sc config `"${serviceName}`" start= disabled"
  }

  Write-Host "Kill all OpenVPN processes"
  cmd /c "taskkill /F /IM openvpn.exe /IM openvpn-gui.exe /IM openvpnserv.exe /IM openvpnserv2.exe"

  Write-Host "Flush local DNS cache"
  cmd /c "ipconfig /flushdns"

  Write-Host "Start OpenVPN with the connection profile ${vpnProfile}"
  # Start-Process -FilePath $openVpnDirectoryPath\openvpn-gui.exe -ArgumentList "--connect `"$vpnProfileFile`"" -NoNewWindow
  Start-Process `
    -FilePath "${openVpnDirectoryPath}\openvpn.exe" `
    -ArgumentList "--config `"${vpnProfileFile}`" --log `"${vpnLogFile}`"" `
    -Verb RunAs
  Start-Sleep -Seconds 5
  cmd /c "wmic process where name=`"openvpn.exe`" call setpriority `"real time`""
  Write-Host "OpenVPN restarted with profile: $vpnProfile" -ForegroundColor Yellow
}
