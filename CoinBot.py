#!/usr/bin/python
#####################################################################################
# File: CoinBot.py
# Purpose: An 'Ub3r31337' way to auto manage digital currencies
# Constraints: Must be run using Python
# Syntax: ./CoinBot.py
###############################################################################
# Import standard libraries
###############################################################################
from optparse import OptionParser
import os, sys, inspect, signal
###############################################################################
# Global variables
###############################################################################
########### Static Location variables ###########
_FILE_FRAME=os.path.split(inspect.getfile( inspect.currentframe() ))
for element in _FILE_FRAME:
  if ".py" in element:
    _SCRIPT_FILE=element
_MAIN_DIR=os.path.dirname(os.path.realpath(_SCRIPT_FILE))
_SCRIPT_NAME=os.path.basename(_SCRIPT_FILE)
_SCRIPT=os.path.realpath(_SCRIPT_FILE)
# Folder Location variables
_MODULES_FOLDER_NAME="Modules"
_MODULES_DIR=os.path.join(_MAIN_DIR,_MODULES_FOLDER_NAME)
_SETUP_FOLDER_NAME="Setup"
_SETUP_DIR=os.path.join(_MAIN_DIR,_SETUP_FOLDER_NAME)
_PLUGINS_FOLDER_NAME="Plugins"
_PLUGINS_DIR=os.path.join(_MAIN_DIR, _PLUGINS_FOLDER_NAME)
_LIB_FOLDER_NAME="Libs"
_LIB_DIR=os.path.join(_MAIN_DIR,_LIB_FOLDER_NAME)
_LOGS_FOLDER_NAME="Logs"
_LOGS_DIR=os.path.join(_MAIN_DIR,_LOGS_FOLDER_NAME)
# Register Plugins here
_SCRAPER_FOLDER_NAME="Scraper"
_SCRAPER_DIR=os.path.join(_PLUGINS_DIR, _SCRAPER_FOLDER_NAME)
# File Location variables
_CORE_LOG_NAME="CBCore.log"
_CORE_LOG_FILE=os.path.join(_LOGS_DIR,_CORE_LOG_NAME)
_CORE_CONFIG_NAME="CBConfig.ini"
_CORE_CONFIG_FILE=os.path.join(_SETUP_DIR,_CORE_CONFIG_NAME)
###############################################################################
# Dynamically build project path into the system
###############################################################################
def addToPath(fileOrDir):
  toAdd = os.path.realpath(os.path.abspath(fileOrDir))
  if toAdd not in sys.path:
    sys.path.insert(0, toAdd)
# Append main folder
addToPath(_MAIN_DIR)
# Append sub-folders
addToPath(os.path.join(_MAIN_DIR,_MODULES_FOLDER_NAME))
addToPath(os.path.join(_MAIN_DIR,_LIB_FOLDER_NAME))
addToPath(os.path.join(_MAIN_DIR,_PLUGINS_FOLDER_NAME))
###############################################################################
# Signal Handler
###############################################################################
def signal_handler(signal, frame):
    print '\nCtrl+C detected, exiting...'
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
###############################################################################
# Usage sub-function
###############################################################################
def invalidUsage():
    print "Invalid usage, must provide at least one flag"
    print "(Run with -h for more info)"
###############################################################################
# Project imports
###############################################################################
import Libs.CBConfig as cbConfig
import Libs.CBLogging as cbLogger
import Libs.CBUtils as cbUtils
import Plugins.Scraper.CBScraper as cbScraper
###############################################################################
# Core functions
###############################################################################
# Gets a List of CoinBot Modules
# Returns: List<Module> OR None (Object)
# TODO: Move logic to new function for getting list
def execute_modules():
  hasPath = cbUtils.ensureDirPath(_MODULES_DIR)
  if not hasPath:
    return None
  else:
    os.chdir(_MODULES_DIR)
    for files in os.listdir("."):
      if (files.endswith(".py")) and (not(files == "__init__.py")):
        print files
        print "iteration"
        # TODO: Figure out syntax for executing strings as files in python
        #eval(files)
###############################################################################
# Main function
###############################################################################
def main():
  # Parse CLI
  parser = OptionParser(usage="Usage: %prog [options]",
    version="%prog 0.5")
  parser.add_option("-e", "--exec-modules",
    action="store_true", dest="exec_modules",
    default=False, help="Execute modules")
  parser.add_option("-s", "--start-scraper",
    action="store_true", dest="start_scraper",
    default=False, help="Starts the scraper")
  (options, args) = parser.parse_args()
  # Initialize proper use bool
  isValid = False

  # Run all modules
  if(options.exec_modules is True):
    print "NOTE: Feature not fully implemented yet."
    execute_modules()
    isValid = True

  # Initialize Logging
  # TODO: Migrate to module specific call
  #cbLogger.setLoggingTo(_CORE_LOG_FILE)

  # Grab configurations
  # TODO: Migrate to module specific call
  #config = cbConfig.getConfig(_CORE_CONFIG_FILE)

  if(options.start_scraper is True):
    cbScraper.start_scraper()
    isValid = True

  if((options.exec_modules is False)
    and (options.start_scraper is False)):
    invalidUsage()

###############################################################################
# Main function call
###############################################################################
# Namespace check of core program
if __name__ == '__main__':
  main()

