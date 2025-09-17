@echo off

:: Set the path for the OSSEC/Wazuh active response log file.
set LOG_FILE="C:\Program Files (x86)\ossec-agent\active-response\active-responses.log"

:: Use PowerShell to get a list of network adapters and loop through them.
:: For each adapter found, disable it and write a log entry.
for /f "tokens=*" %%a in ('powershell -NoProfile -Command "Get-NetAdapter | Select-Object -ExpandProperty Name"') do (
    
    :: 1. Disable the network interface using netsh.
    netsh interface set interface name="%%a" admin=disable

    :: 2. Log the action to the active-responses.log file with a timestamp.
    echo %date% %time% - firewall-drop: Disabling network interface "%%a" >> %LOG_FILE%
)

:: Exit the script.
exit /b
