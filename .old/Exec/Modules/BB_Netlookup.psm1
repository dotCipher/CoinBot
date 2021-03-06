#####################################################################################
# File: BB_Netlookup.psm1
# Purpose: Module for using:
#          http://netlookup.se/free-bitcoins/57198
# Constraints: Must be run using Windows Powershell v2.0 with access 
#              to Internet Explorer
# Syntax: .\Bitcoiner_Bot.ps1 (called as module)
#####################################################################################
# Command Line Params
#####################################################################################
param($ini)

#####################################################################################
# Script localization function
#####################################################################################
function Get-ScriptDirectory(){
    $Invocation = (Get-Variable MyInvocation -Scope 1).Value
    return (Split-Path $Invocation.MyCommand.Path)
}

#####################################################################################
# Site Link
#####################################################################################
$SITE_LINK = "http://netlookup.se/free-bitcoins/"

#####################################################################################
# Global Variables
#####################################################################################
$MOD_DIR = Get-ScriptDirectory
$LOG_DIR = "$MOD_DIR\ModLogs"
$LOG_FILE = "$LOG_DIR\BB_Netlookup.log"

#####################################################################################
# Utility Functions
#####################################################################################
# Return: String
function getDateAndTimeStr(){
    # Get Date Object
    $date = Get-Date
    # Return formed string
    return $date.ToShortDateString() + " - " + $date.ToShortTimeString()
}

# Return: void
function writeToModLog($type, $datetime, $desc){
    # Force out spaces from $type
    $type = $type -replace ' ', '_'
    
    # Check existance of ModLog dir
    if((Test-Path $LOG_DIR) -ne $true){
        New-Item -ItemType Directory "$LOG_DIR" | Out-Null
    }
    
    # Check existance of log
    if((Test-Path $LOG_FILE) -ne $true){
        New-Item -ItemType File "$LOG_FILE" | Out-Null
    }
    
    # Write string to log
    # [<DATE> - <TIME>] <TYPE> <DESC>
    $str = "[" + $datetime + "] " + $type + " " + $desc
    Add-Content $LOG_FILE $str
}
#####################################################################################
# Run Module
#####################################################################################
Write-Host "IN NETLOOKUP MODULE"
Write-Host "INI FILE:"
Write-Host $ini
Write-Host "MOD_DIR:"
Write-Host $MOD_DIR
$wallet_addr = $ini['Bitcoiner-Bot']['Wallet-Address']
$wallet_addr = $wallet_addr.substring(1,$wallet_addr.length-2)
Write-Host "wallet-addr:"
Write-Host $wallet_addr

# Open page
$ie = New-Object -com "InternetExplorer.Application"
$ie.navigate($SITE_LINK)
Write-Host -nonewline "Opening Netlookup...`t`t"
while($ie.ReadyState -ne 4){
    Start-Sleep -m 100
}
$doc = $ie.Document
Write-Host -foregroundcolor green "Success!`n"

# Submit information
Write-Host -nonewline "Entering Wallet-Address...`t`t"
$addr_field = $doc.getElementByID("reciver")
$submit_btn = ($doc.getElementsByTagName("input") | where {$_.Value -eq "Recive bitcoins!"})
$addr_field.value = $wallet_addr
$submit_btn.click()
Write-Host -foregroundcolor green "Success!`n"

# Get date for log entry
$datetime = getDateAndTimeStr

# Check if submission was successful
$doc = $ie.Document
$check = ($doc.getElementsByTagName("h1") | Where {$_.innerText -eq "Got it!"})
if($check){
    # Successful
    $successStr = "BB_Netlookup for address of $wallet_addr"
    writeToModLog "SUBMIT_SUCCESS" $datetime $successStr
} else {
    # Not successful
    $failureStr = "BB_Netlookup for address of $wallet_addr"
    writeToModLog "SUBMIT_FAILURE" $datetime $failureStr
}

# Close page
Stop-Process -processname 'iexplore' -force
