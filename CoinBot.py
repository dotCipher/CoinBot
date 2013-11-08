#!/usr/bin/python
#####################################################################################
# File: CoinBot.py
# Purpose: An 'Ub3r31337' way to automatically visit certain free e-coin sites 
#          and enter valid address information for payouts.
# Constraints: Must be run using Python
# Syntax: python ./CoinBot.py
#####################################################################################
# Imports
#####################################################################################
from optparse import OptionParser
import os
import ConfigParser
import logging
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
####################################################################################
# Command Line Params
#####################################################################################
def initCliParams():
  parser = OptionParser(usage="usage: %prog [options]",
    version="%prog 1.0")
  parser.add_option("-e", "--execute-modules",
    action="store_true", dest="execute_modules",
    default=False, help="Execute modules",)
  (options, args) = parser.parse_args()
####################################################################################
# File IO functions
#####################################################################################
# Gets config file as variable
# Returns: config OR None (Object)
def getConfig():
  if not os.path.exists(_CORE_CONFIG_FILE):
    return None
  configDictionary = {}
  config = ConfigParser.ConfigParser()
  config.read(_CORE_CONFIG_FILE)
  return config

# Given config, prints full config file to console
# Returns: (void)
def debugPrintConfig(config):
  for section in config.sections():
    print "[" + section + "]"
    for option in config.options(section):
      print option + ":"
      print config.get(section, option)
      #config.get("common", "folder").split("\n")

# Initializes the logging system
# Returns: (void)
def initLogging():
  if not os.path.exists(_CORE_LOG_FILE):
    os.makedirs(_LOGS_DIR)
  logging.basicConfig(level=logging.DEBUG, 
    filename=_CORE_LOG_FILE, filemode='a',
    format='[%(asctime)s_%(msecs)d]:%(levelname)s:%(message)s', 
    datefmt='%m/%d/%Y_%H:%M:%S')

# Given a logfile, clears the entire log
# Returns: True OR False (Boolean)
def clearLog(logfile):
  if not os.path.exists(_CORE_LOG_FILE):
    return False
  with open(logfile, 'w'):
    pass
    return True

# Gets a List of CoinBot module objects
# Returns: List<Module> OR None (Object)
def getModules():
  # TODO: Finish this method
  
#####################################################################################
# Main function
#####################################################################################
def main():
  # Setup command line params
  initCliParams()
  # Initialize Logging
  initLogging()
  # Grab configurations
  config = getConfig()


#####################################################################################
# Main function call
#####################################################################################
# Namespace check of core program
if __name__ == '__main__':
    main()

