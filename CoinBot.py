#!/usr/bin/python
#####################################################################################
# File: CoinBot.py
# Purpose: An 'Ub3r31337' way to automatically visit certain free e-coin sites 
#          and enter valid address information for payouts.
# Constraints: Must be run using Python
# Syntax: python ./BitcoinerBot.py
#####################################################################################
# Imports
#####################################################################################
from optparse import OptionParser
import os
#####################################################################################
# Script localization function
#####################################################################################
def getMainDirectory():
	return os.path.dirname(os.path.realpath(__file__))
def getScriptName():
	return os.path.basename(__file__)
def getFullScriptPath():
	return os.path.realpath(__file__)
####################################################################################
# Global variables
#####################################################################################
########### Static Location variables ###########
_MAIN_DIR=getMainDirectory()
_SCRIPT_NAME=getScriptName()
_SCRIPT=getFullScriptPath()
# Folder Location variables
_MODULES_DIR=os.path.join(_MAIN_DIR,"Modules")
_SETUP_DIR=os.path.join(_MAIN_DIR,"Setup")
_LIB_DIR=os.path.join(_MAIN_DIR,"Libs")
_LOGS_DIR=os.path.join(_MAIN_DIR,"Logs")
# File Location variables
_CORE_LOG_FILE=os.path.join(_LOGS_DIR,"CB_Core.log")
_CORE_CONFIG_FILE=os.path.join(_SETUP_DIR,"CB_Config.ini")

#####################################################################################
# Main function
#####################################################################################
def main():
	# Setup command line params
    parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 1.0")
    parser.add_option("-e", "--execute-modules",
                      action="store_true",
                      dest="execute_modules",
                      default=False,
                      help="Execute modules",)
    (options, args) = parser.parse_args()
    print _MODULES_DIR
    print _SETUP_DIR
    print _LIB_DIR
    print _LOGS_DIR
    print _CORE_LOG_FILE
    print _CORE_CONFIG_FILE


#####################################################################################
# Main function call
#####################################################################################
if __name__ == '__main__':
    main()

