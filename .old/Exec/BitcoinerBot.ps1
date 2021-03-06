#####################################################################################
# File: BitcoinerBot.ps1
# Purpose: An 'Ub3r31337' way to automatically visit certain free bitcoin sites 
#          and enter valid address information for payouts.
# Constraints: Must be run using Windows Powershell v2.0 with access 
#              to Internet Explorer and on Windows Vista or higher OS
# Syntax: .\BitcoinerBot.ps1
#####################################################################################
# Get-Help Block
#####################################################################################

<#
    .SYNOPSIS
    BitcoinerBot.ps1 is used to automatically visit certain free bitcoin sites and
    enter valid information for payouts to a given wallet address specified in the
    config file

    .DESCRIPTION
    The script can be 'hooked up' with any set of given power shell modules that are 
    set up for any given free bitcoin site.  Essentially it will allow the user to 
    automatically enter in whatever information needed in the site in whatever format 
    needed to get the payouts from that site.

    .EXAMPLE
    ./BitcoinerBot.ps1
    This example is the default use of running Bitcoiner Bot

    .NOTES
    Author:  dot_Cipher
    Email:   dot_cipher@null-sec.net
    Date:    May 9, 2013
    Version: 1.1
#>
#####################################################################################
# Command Line Params
#####################################################################################
param(
    [switch]$EXECUTE_MODULES = $false
)
#####################################################################################
# Script localization function
#####################################################################################
function Get-ScriptDirectory(){
    $Invocation = (Get-Variable MyInvocation -Scope 1).Value
    return (Split-Path $Invocation.MyCommand.Path)
}

#####################################################################################
# Global Variables
#####################################################################################
########### Static Location variables ###########
$MAIN_DIR = Get-ScriptDirectory
$SCRIPT = "$MAIN_DIR\BitcoinerBot.ps1"

# Folder Location variables
$MODULES_DIR = "$MAIN_DIR\Modules"
$SETUP_DIR = "$MAIN_DIR\Setup"
$LIB_DIR = "$MAIN_DIR\Libs"

# File Location variables
$LOG_FILE = "$MAIN_DIR\BitcoinerBot.log"
$CONFIG_FILE = "$MAIN_DIR\BitcoinerBot_Config.ini"

# Misc Location variables
$XML_TASKFORMAT_PATH = "$SETUP_DIR\TaskFormat.xml"

########### Log values ###########
$WADDR_VALID = "WADDR_VALID"
$WADDR_INVALID_SIZE = "WADDR_INVALID_SIZE"
$WADDR_INVALID_BASE58 = "WADDR_INVALID_BASE58"
$WADDR_INVALID_HASHCHK = "WADDR_INVALID_HASHCHK"

########### Menu option values ###########
$MENU_TITLE = "Add or Remove a scheduled task for BitcoinerBot"
$MENU_MESSAGE = "Please select an option below and press enter:"
$MENU_ADDTASK = New-Object System.Management.Automation.Host.ChoiceDescription `
    "&Add Task", "Adds a scheduled task for BitcoinerBot to run automatically."
$MENU_REMTASK = New-Object System.Management.Automation.Host.ChoiceDescription `
    "&Remove Task", "Removes a scheduled task of BitcoinerBot."
$MENU_QUIT = New-Object System.Management.Automation.Host.ChoiceDescription `
    "&Quit", "Quits the BitcoinerBot scheduling system."
$MENU_OPTS = [System.Management.Automation.Host.ChoiceDescription[]]`
    ($MENU_ADDTASK, $MENU_REMTASK, $MENU_QUIT)

########### API values ###########
$WALLETCHECK_API = 'http://blockexplorer.com/q/checkaddress/'

########### Misc values ###########
$EXECUTE_MODULES_PARAM_STR = "-EXECUTE_MODULES"
$MAX_LOG_LINES = 100
$OUTPUT_COLOR = "cyan"

#####################################################################################
# File IO Functions
#####################################################################################
# Return: $ini object
function loadINIFile(){
    # $ini['SectionName']['FieldName'] == Value
    $ini = @{}
    #$fullConfigPath = (Resolve-Path $CONFIG_FILE | Out-String)
    switch -regex -file $CONFIG_FILE {
        # Section
        "^\[(.+)\]$" {
            $section = $matches[1].Trim()
            $ini[$section] = @{}
            continue
        }
        # Int
        "^\s*([^#].+?)\s*=\s*(\d+)\s*$" {
            $name, $value = $matches[1..2]
            $ini[$section][$name] = [int]$value
            continue
        }
        # Decimal
        "^\s*([^#].+?)\s*=\s*(\d+\.\d+)\s*$" {
            $name, $value = $maches[1..2]
            $ini[$section][$name] = [decimal]$value
            continue
        }
        # Everything else
        "^\s*([^#].+?)\s*=\s*(.*)" {
            $name,$value = $matches[1..2]
            $ini[$section][$name] = $value.Trim()
        }
    }
    return $ini
}

# Return: $log object
function loadLogFile(){
    # $log_arr[$i][0] = Date and time
    # $log_arr[$i][1] = Type
    # $log_arr[$i][2] = Description
    $log = @{}
    $exists = Test-Path $LOG_FILE
    if($exists -eq $true){
        $path = Resolve-Path $LOG_FILE
        $reader = [System.IO.File]::OpenText($path)
        try{
            for($c=0; ; $c++){
                $line = $reader.ReadLine()
                # Break out of loop if null
                if($line -eq $null){ break }
                # Process Line
                $dnt = $line | Select-String -Pattern "\[(.*?)\]" |`
                    % { $_.Matches } | % { $_.Value }
                $substr_arr = ($line.Substring($line.IndexOf(']')+2)).split()
                $type = $substr_arr[0]
                $desc = ""
                for($i=1; $i -le $substr_arr.length; $i=$i+1){
                    if($i -eq 1){
                        $desc = $substr_arr[$i]
                    } else {
                        $desc = $desc + " " + $substr_arr[$i]
                    }
                }
                $log[$c] = @($dnt, $type, $desc.Trim())
            }
        } finally {
            $reader.Close()
        }
        return $log
    } else {
        return $null
    }
}

# Return: void
function clearLog(){
    $exists = Test-Path $LOG_FILE
    if($exists){
        Remove-Item $LOG_FILE
    }
}

# Return: $modules String Array
function loadModules(){
    # $modules[$i] == Module Name
    # Is there a Modules folder?
    $mexists = Test-Path $MODULES_DIR
    if($mexists -eq $true){
        # Scan all files in modules folder with psm1
        $dir = Get-ChildItem $MODULES_DIR
        $list = $dir | where { $_.extension -eq ".psm1" }
        $modules = @()
        # Check if there are multiple files
        if($list.toString().CompareTo("System.Object[]") -ne 0){
            # Single file
            $modules += $list.toString()
        } else { # Multiple files
            for($i=0; $i -lt $list.Length; $i++){
                # Parse each Module name and add too list
                $name = $list[$i].toString()
                $modules += $name
            }
        }
        return $modules
    } else {
        printOut red "ERROR: Module Directory not found."
        printOut red "Please make a directory called `'Modules`' (without quotes)"
        printOut red "  in the same directory of BitcoinerBot.ps1"
        printOut red "- - - EXITING - - -"
        Exit
    }
}

#####################################################################################
# Data Filters
#####################################################################################

# Return: boolean
filter isNumeric(){
    return ($_.Trim() -match "[-]?[0-9.]+$")
}

#####################################################################################
# Menu Output Functions
#####################################################################################

# Return: void
function printMenuColumn($cSize){
    for($i = 0; $i -lt ($cSize); $i++){
        if(($i % 2) -eq 0){
            Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "-"
        } else {
             Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR " "
        }
    }
}

# Return: void
function printMenuColumnLSide($cSize){
    Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR " "
    for($i = 1; $i -lt ($cSize); $i++){
        Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR " "
    }
}

# Return: void
function printMenuColumnRSide($cSize){
    for($i = 1; $i -lt ($cSize); $i++){
        Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR " "
    }
    Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR " "
}

# Return: void
function printMenuTitle($cSize){
    if($cSize -eq 12){
        Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "BitcoinerBot"
    } elseif ($cSize -gt 12){
        $diff = $cSize - 12
        $sideCol = $diff / 2
        if($sideCol -is [int]){
            for($s = $sideCol; $s -gt 0; $s--){
                Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR " "
            }
            Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "BitcoinerBot"
            for($s = $sideCol; $s -gt 0; $s--){
                Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR " "
            }
        } else {
            for($s = [Math]::Floor($sideCol); $s -gt 0; $s--){
                Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR " "
            }
            Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "BitcoinerBot"
            for($s = [Math]::Floor($sideCol); $s -gt 0; $s--){
                Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR " "
            }
        }
    }
}

# Return: void
function printMenuAuthor($cSize){
    if($cSize -eq 14){
        Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "By: dot_Cipher"
    } elseif ($cSize -gt 14){
        $diff = $cSize - 14
        $sideCol = $diff / 2
        if($sideCol -is [int]){
            for($s = $sideCol; $s -gt 0; $s--){
                Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR " "
            }
            Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "By: dot_Cipher"
            for($s = $sideCol; $s -gt 0; $s--){
                Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR " "
            }
        } else {
            for($s = [Math]::Floor($sideCol); $s -gt 0; $s--){
                Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR " "
            }
            Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "By: dot_Cipher"
            for($s = [Math]::Floor($sideCol); $s -gt 0; $s--){
                Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR " "
            }
        }
    }
}

# Return: void
function printMenu(){
    $conWidth = (Get-Host).UI.RawUI.WindowSize.Width
    $col_1 = 0
    $col_2 = 0
    $col_3 = 0
    # Divide into three columns
    $parts = ($conWidth / 3)
    if($parts -is [int]){
        $col_1 = $col_2 = $col_3 = $parts
    } else {
        $col_1 = $col_3 = [Math]::Floor($parts)
        $col_2 = $parts + 1
    }
    if($col_2 -ge 14){
        # Write Top Line
        printMenuColumn $conWidth
        #Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "`n"
        # Write Title Line
        printMenuColumnLSide $col_1
        printMenuTitle $col_2
        printMenuColumnRSide $col_3
        Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "`n"
        # Write Author Line
        printMenuColumnLSide $col_1
        printMenuAuthor $col_2
        printMenuColumnRSide $col_3
        Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "`n"
        # Write Bottom Line
        printMenuColumn $conWidth
        Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "`n"
    } elseif($conWidth -ge 14){
        # Write Top Line
        printMenuColumn $conWidth
        Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "`n"
        # Write Title Line
        printMenuTitle $conWidth
        Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "`n"
        # Write Author Line
        printMenuAuthor $conWidth
        Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "`n"
        # Write Bottom Line
        printMenuColumn $conWidth
        Write-Host -NoNewLine -ForegroundColor $OUTPUT_COLOR "`n"
    }
}

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
function writeToLog($type, $datetime, $desc){
    # Force out spaces from $type
    $type = $type -replace ' ', '_'
    
    # Check existance of log
    if((Test-Path $LOG_FILE) -ne $true){
        New-Item -ItemType file $LOG_FILE | Out-Null
    }
    
    # Write string to log
    # [<DATE> - <TIME>] <TYPE> <DESC>
    $str = "[" + $datetime + "] " + $type + " " + $desc
    Add-Content $LOG_FILE $str
}

# Return: Credential Object
function getCredentialsFromUser(){
    # Retrieve system information
    $uname = [Environment]::UserName
    $mname = [Environment]::MachineName
    $credStr = $mname + "\" + $uname
    # Get credentials from user
    $cred = $host.ui.PromptForCredential("Enter Credentials", `
        "Please enter your user name and password.", "$credStr", "")
    #$cred = Get-Credential -Credential $credStr
    return $cred
}

# Return: boolean
function checkInternetConnection(){
    # Hardcoded GUID tag for connectivity in Windows Registry (Vista and above)
    # Note:  Does NOT count VPN tunneling/Proxies as connected
    $guid = [Guid]'{DCB00C01-570F-4A9B-8D69-199FDBA5723B}'
    $type = [Type]::GetTypeFromCLSID($guid)
    $act = [Activator]::CreateInstance($type)
    return $act.IsConnectedToInternet
}

# Return: void
function printOut($color, $type){
    if($type -eq $WADDR_INVALID_SIZE){
        Write-Host -foregroundcolor $color "Wallet address is not proper size, exiting."
    } elseif($type -eq $WADDR_INVALID_BASE58){
        Write-Host -foregroundcolor $color "Wallet Address is not in Base58, exiting."
    } elseif($type -eq $WADDR_INVALID_HASHCHK){
        Write-Host -foregroundcolor $color "Wallet Address failed hash check, exiting."
    } else {
        Write-Host -foregroundcolor $color $type
    }
}

# Return: boolean
function isWalletChecked($log_tbl, $wallet_addr){
    for($i=0; $i -lt $log_tbl.count; $i=$i+1){
        if($log_tbl[$i][2] -eq $wallet_addr){
            if($log_tbl[$i][1] -eq $WADDR_VALID){
                return $true
            } elseif($log_tbl[$i][1] -eq $WADDR_INVALID_SIZE){
                printOut yellow $WADDR_INVALID_SIZE
                Exit
            } elseif($log_tbl[$i][1] -eq $WADDR_INVALID_BASE58){
                printOut yellow $WADDR_INVALID_BASE58
                Exit
            } elseif($log_tbl[$i][1] -eq $WADDR_INVALID_HASHCHK){
                printOut yellow $WADDR_INVALID_HASHCHK
                Exit
            }
        }
    }
    return $false
}

# Return: String
function checkWalletAddress($wallet_addr){
    # Form API Query
    $nav_query = "$WALLETCHECK_API" + "$wallet_addr"
    
    # Open an instance of ie to check api
    $ie = New-Object -com "InternetExplorer.Application"
    $ie.navigate($nav_query)
    while($ie.ReadyState -ne 4){
        Start-Sleep -m 100
    }
    $rv = $ie.Document.body.innerHTML
    
    # Parse out return value
    # TODO: Fix this for matching all within any html tag
    # TODO: Refer to regex use in loadLogFile
    $rv = $rv.Substring($rv.IndexOf('>')+1)
    $rv = $rv.Substring(0,$rv.IndexOf('<'))
    
    # Close process
    Stop-Process -processname 'iexplore' -force
    
    # Do appropriate action based on return value and return
    $dt = getDateAndTimeStr
    if($rv -eq 'CK'){
        writeToLog $WADDR_INVALID_HASHCHK $dt $wallet_addr
    } elseif($rv -eq 'X5'){
        writeToLog $WADDR_INVALID_BASE58 $dt $wallet_addr
    } elseif($rv -eq 'SZ'){
        writeToLog $WADDR_INVALID_SIZE $dt $wallet_addr
    } else {
        writeToLog $WADDR_VALID $dt $wallet_addr
    }
    return $rv
}
#####################################################################################
# Scheduler Functions
#####################################################################################

# Return: String
function getCreatedStrForScheduler(){
    # Get Date Object
    $date = Get-Date
    # Form string
    $year = padDateOrTimeStr ($date.Year.toString())
    $month = padDateOrTimeStr ($date.Month.toString())
    $day = padDateOrTimeStr ($date.Day.toString())
    $hour = padDateOrTimeStr ($date.Hour.toString())
    $min = padDateOrTimeStr ($date.Minute.toString())
    $sec = padDateOrTimeStr ($date.Second.toString())
    # Return formed string
    return $year + '-' + $month + '-' + $day + 'T' + $hour + ':' + $min + ':' + $sec
}

# Return: String
function getDateForScheduler(){
    # Get Date Object
    $date = Get-Date
    # Form string
    $year = padDateOrTimeStr ($date.Year.toString())
    $month = padDateOrTimeStr ($date.Month.toString())
    $day = padDateOrTimeStr ($date.Day.toString())
    # Return formed string
    return $year + '-' + $month + '-' + $day
}

# Return: String
function padDateOrTimeStr($str){
    if($str.length -eq 1){
        $str = "0" + $str
    }
    return $str
}

# Return: String
function getTimeToExecForScheduler(){
    cls
    printMenu
    printOut $OUTPUT_COLOR "Enter time to run BitcoinerBot each day"
    printOut $OUTPUT_COLOR "Note: Your computer must be turned on during the time you specify each day"
    printOut $OUTPUT_COLOR "Format = HH:MM:SS (ex. 23:40:00, 10:15:23)`n"
    $inTime = ""
    # Start loop
    while($true){
        # Get input
        Write-Host -ForegroundColor $OUTPUT_COLOR "Enter Time > " -NoNewLine
        $inTime = Read-Host
        # Parse out
        if($inTime -ne ""){
            if($inTime.Length -eq 8){
                # Check format
                $hourStr = $inTime.Substring(0,2)
                $c1 = $inTime.Substring(2,1)
                $minStr = $inTime.Substring(3,2)
                $c2 = $inTime.Substring(5,1)
                $secStr = $inTime.Substring(6,2)
                $format = $false
                if($hourStr | isNumeric){
                    if($c1 -eq ":"){
                        if($minStr | isNumeric){
                            if($c2 -eq ":"){
                                if($secStr | isNumeric){
                                    # Succeeded format check
                                    $format = $true
                                } else {
                                    printOut red "`nError: Seconds(SS) must be numeric.`n"
                                }
                            } else {
                                printOut red "`nError: Not valid format, colon required after Minutes(MM) field.`n"
                            }
                        } else {
                            printOut red "`nError: Minutes(MM) must be numeric.`n"
                        }
                    } else {
                        printOut red "`nError: Not valid format, colon required after Hours(HH) field.`n"
                    }
                } else {
                    printOut red "`nError: Hours(HH) must be numeric.`n"
                }
                # Check for boundries of HH, MM, and SS
                if($format -eq $true){
                    if(($hourStr -le 24) -and ($hourStr -ge 0)){
                        if(($minStr -le 59) -and ($minStr -ge 0)){
                            if(($secStr -le 59) -and ($secStr -ge 0)){
                                # Succeeded bounds check
                                break
                            } else {
                                printOut red "`nError: Seconds(SS) must be between 00 and 59.`n"
                            }
                        } else {
                            printOut red "`nError: Minutes(MM) must be between 00 and 59.`n"
                        }
                    } else {
                        printOut red "`nError: Hours(HH) must be between 00 and 24.`n"
                    }
                }
            } else {
                printOut red "`nError: Input not valid length.`n"
            }
        } else {
            printOut red "`nError: Input cannot be empty.`n"
        }
    }
    return $inTime
}

function getTaskName(){
    $begin = $SCRIPT.LastIndexOf('\')+1
    $end = $SCRIPT.LastIndexOf("ps1")-1
    $dif = $end - $begin
    $name = $SCRIPT.Substring($begin,$dif)
    return $name
}

# Return: String
function createXMLTaskForScheduler($user, $ttexec){
    # 2013-04-24T13:53:00
    # Make task name
    $name = getTaskName
    # Read in template
    $xml = [xml](Get-Content $XML_TASKFORMAT_PATH)
    # Set new values
    $xml.Task.RegistrationInfo.Author = $user
    $xml.Task.RegistrationInfo.Date = (getCreatedStrForScheduler).toString()
    $xml.Task.RegistrationInfo.Description = "[BitcoinerBot Autogenerated Task] Execution at $ttexec daily"
    # Set execution time
    $execTime = (getDateForScheduler) + 'T' + $ttexec
    $xml.Task.Triggers.CalendarTrigger.StartBoundary = $execTime
    $xml.Task.Principals.Principal.UserId = $user
    # Set script command (Assuming Powershell is main issued command)
    $cmd = "-command"
    $fullPath = (Resolve-Path $SCRIPT).toString()
    $arg = $fullPath -replace ' ', '` '
    $xml.Task.Actions.Exec.Arguments = $cmd + " " `
        + $arg + " $EXECUTE_MODULES_PARAM_STR"
    
    # Write out to file
    $xmlExists = Test-Path "$SETUP_DIR\$name.xml"
    if($xmlExists -eq $true){
        Remove-Item "$SETUP_DIR\$name.xml"
        New-Item "$SETUP_DIR\$name.xml" -ItemType file | Out-Null
        Add-Content "$SETUP_DIR\$name.xml" $xml.InnerXML
    } else {
        New-Item "$SETUP_DIR\$name.xml" -ItemType file | Out-Null
        Add-Content "$SETUP_DIR\$name.xml" $xml.InnerXML
    }
    $fullXMLPath = (Resolve-Path "$SETUP_DIR\$name.xml").toString()
    return $fullXMLPath
}

# Return: Task Object List
function getTaskList(){
    $tasks = @()
    $scheduler = New-Object -ComObject "Schedule.Service"
    $scheduler.Connect() 
    # Build inventory of tasks from root of scheduler
    $scheduler.GetFolder("\").GetTasks(0) | % {
        $xml = [xml]$_.xml
        $tasks += New-Object PSObject -Property @{
            "Name" = $_.Name
            "Path" = $_.Path
            "LastRunTime" = $_.LastRunTime
            "NextRunTime" = $_.NextRunTime
            "Actions" = ($xml.Task.Actions.Exec | % { "$($_.Command) $($_.Arguments)" }) -join "`n"
        }
    }
    # Close Com Object
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($scheduler) | Out-Null
    # Output all tasks
    return $tasks
}

# Return: void
function unscheduleXMLTask($taskName, $xmlfilePath){
    $taskName = "`"$taskName`""
    $output = (Schtasks /delete /tn $taskName /f) 2>&1
    $rvStr = $output[0].toString()
    if($rvStr -eq $null){
        printOut red "`nERROR: Could not query scheduler, please restart BitcoinerBot and try agian.`n"
    } else {
        if($rvStr -eq "S"){
            Remove-Item "$xmlfilePath"
            printOut green "`nSUCCESS: BitcoinerBot task is now removed from the scheduler`n"
        } elseif($rvStr -eq "ERROR: The system cannot find the file specified."){
            printOut red "`nERROR: Cannot remove BitcoinerBot task, no task exists in the scheduler."
            printOut red "Please add a task for BitcoinerBot and try again.`n"
        } else {
            printOut red "`n$rvStr`n"
        }
    }
}

# Return: void
function scheduleXMLTask($creds, $xmlfilePath){
    # Get credentials to schedule with
    $taskName = getTaskName
    # Add quotes
    $xmlFilePath = "`"$xmlFilePath`""
    $user = $creds.UserName
    $user = "`"$user`""
    $pass = $creds.GetNetworkCredential().Password
    $pass = "`"$pass`""
    # Schedule the task
    $output = (Schtasks /create /xml $xmlfilePath `
        /tn "\$taskName" /ru $user /rp $pass) 2>&1
    $rvStr = $output[0].toString()
    if($rvStr -eq $null){
        printOut red "`nERROR: Could not query scheduler, please restart BitcoinerBot and try agian.`n"
    } else {
        if($rvStr -eq "S"){
            printOut green "`nSUCCESS: BitcoinerBot has been scheduled!`n"
        } elseif($rvStr -eq "ERROR: Cannot create a file when that file already exists."){
            printOut red "`nERROR: Cannot schedule BitcoinerBot since it has already been scheduled."
            printOut red "`tPlease remove the scheduled task for BitcoinerBot and try again.`n"
        } else {
            printOut red "`n$rvStr`n"
        }
    }
}

#####################################################################################
# Module Driver
#####################################################################################

# Return: boolean
function runModules($modules, $ini_file){
    # Is it a single modules or multiple modules?
    # Then check if Modules are proper format
    #  BB_<MODNAME>
    if($modules.getType().toString() -eq "System.String"){
        # Single 
        if($modules.StartsWith("BB_")){
            # Run each module and pass ini to the module
            $name = $modules
            Import-Module -force "$MODULES_DIR\$name" -ArgumentList $ini_file
            Invoke-Expression "& `"$MODULES_DIR\$name`""
        }
    } else {
        for($i=0; $i -lt $modules.length; $i++){
            if($modules[$i].StartsWith("BB_")){
                # Run each module and pass ini to the module
                $name = $modules[$i]
                Import-Module -force "$MODULES_DIR\$name" -ArgumentList $ini_file
                Invoke-Expression "& `"$MODULES_DIR\$name`""
            }
        }
    }
}

#####################################################################################
# Main function
#####################################################################################
# Return: void
function main(){
    # Get Date and Time String when run
    $dt = getDateAndTimeStr
    
    # Check if EXECUTE_MODULES was provided
    if(!$EXECUTE_MODULES){
        # - - - Do not execute modules - - -
        $cred = getCredentialsFromUser
        $continue = $true
        while($continue){
            cls
            printMenu
            $MENU_result = $host.ui.PromptForChoice($MENU_TITLE, $MENU_MESSAGE, $MENU_OPTS, 0) 
            switch($MENU_result){
                0 { # - Add Task -
                    if($cred -eq $null){
                        # Do nothing
                    } else {
                        $timeInput = getTimeToExecForScheduler
                        $xmlFile = createXMLTaskForScheduler $cred.UserName $timeInput
                        scheduleXMLTask $cred $xmlFile
                        printOut $OUTPUT_COLOR "`nPress any key to continue...`n"
                        $x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
                    }
                }
                1 { # - Remove Task -
                    $tName = getTaskName
                    $xmlFile = "$SETUP_DIR\$tName.xml"
                    unscheduleXMLTask $tName $xmlFile
                    printOut $OUTPUT_COLOR "`nPress any key to continue...`n"
                    $x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
                }
                2 { # - Quit -
                    Write-Host ""
                    $continue = $false
                }
            }
        }
    } else {
        # - - - Execute modules - - -
        # Note: This should be automatically called,
        #       not user called.
        # Test internet connection
        $connection = checkInternetConnection
        if($connection -eq $false){
            printOut red "Not connected to internet, please connect and run again"
            writeToLog "NO_CONNECTION" $dt "Not connected to internet, cannot execute modules."
            Exit
        }
        
        # Grab data from INI file
        $ini = loadINIFile
        $wallet_addr = $ini['Bitcoiner-Bot']['Wallet-Address']
        $wallet_addr = $wallet_addr.substring(1,$wallet_addr.length-2)
        
        # Grab data from Log file
        $log = loadLogFile
        # Clear log if larger than 100 lines
        if($log.count -ge $MAX_LOG_LINES){
            # Clear and reload log
            clearLog
            $log = loadLogFile
        }
        
        # Has Wallet been checked?
        $checked = isWalletChecked $log $wallet_addr
        
        if($checked -eq $false){
            Write-Host -nonewline "Checking Wallet Address...`t`t"
            # If it hasn't, then check Wallet Address
            $rv = checkWalletAddress $wallet_addr
            # Check BlockChain API Return Codes
            <#
            if(($rv -eq 'X5') -or ($rv -eq 'SZ') -or ($rv -eq 'CK')){
                Exit
            }
            #>
            if($rv -eq 'X5'){
                printOut red "Error"
                printOut yellow "Wallet Address is not in Base58, exiting."
                Exit
            } elseif ($rv -eq 'SZ'){
                printOut red "Error"
                printOut yellow "Wallet Address is not proper size, exiting."
                Exit
            } elseif ($rv -eq 'CK'){
                printOut red "Error"
                printOut yellow "Wallet Address failed hash check, exiting."
                Exit
            } else {
                printOut green "Success!`n"
            }
        }
        
        # Finally load all modules then run them
        $mods = loadModules
        runModules $mods $ini
    }
}

# Main function call
main
Exit
