#!/usr/bin/python
#####################################################################################
# File: CoinBot.py
# Purpose: An 'Ub3r31337' way to auto manage digital currencies
# Constraints: Must be run using Python
# Syntax: ./CoinBot.py
####################################################################################
# Import standard libraries
#####################################################################################
from optparse import OptionParser
import os, sys, inspect
####################################################################################
# Global variables
#####################################################################################
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
_CORE_LOG_NAME="CB_Core.log"
_CORE_LOG_FILE=os.path.join(_LOGS_DIR,_CORE_LOG_NAME)
_CORE_CONFIG_NAME="CB_Core.log"
_CORE_CONFIG_FILE=os.path.join(_SETUP_DIR,_CORE_CONFIG_NAME)
#####################################################################################
# Dynamically build project path into the system
#####################################################################################
# Append main folder
cmd_folder = os.path.realpath(os.path.abspath(_SCRIPT_FILE))
if cmd_folder not in sys.path:
   sys.path.insert(0, cmd_folder)
# Append sub-folders
modules_subfolder = os.path.realpath(os.path.abspath(os.path.join(_SCRIPT_FILE,_MODULES_FOLDER_NAME)))
if modules_subfolder not in sys.path:
  sys.path.insert(0, modules_subfolder)
libs_subfolder = os.path.realpath(os.path.abspath(os.path.join(_SCRIPT_FILE,_LIB_FOLDER_NAME)))
if libs_subfolder not in sys.path:
  sys.path.insert(0, libs_subfolder)
plugins_subfolder = os.path.realpath(os.path.abspath(os.path.join(_SCRIPT_FILE,_PLUGINS_FOLDER_NAME)))
if plugins_subfolder not in sys.path:
  sys.path.insert(0, plugins_subfolder)
#####################################################################################
# Import all project Libraries/Modules/Plugins
#####################################################################################
import Libs.CoinBot_Config as cbConfig
import Libs.CoinBot_Logging as cbLogger
import Plugins.Scraper.CoinBot_Scraper as cbScraper
####################################################################################
# Core Module functions
#####################################################################################
# Gets a List of CoinBot Modules
# Returns: List<Module> OR None (Object)
# TODO: Move logic to new function for getting list
def execute_modules():
  if not os.path.exists(_MODULES_DIR):
    os.makedirs(os.path.dirname(os.path.realpath(_MODULES_DIR)))
    return None
  os.chdir(_MODULES_DIR)
  for files in os.listdir("."):
    if (files.endswith(".py")) and (not(files == "__init__.py")):
      print files
      print "iteration"
      # TODO: Figure out syntax for executing strings as files in python
      #eval(files)

#####################################################################################
# Main function
#####################################################################################
def main():
  # Parse CLI
  parser = OptionParser(usage="usage: %prog [options]",
    version="%prog 1.0")
  parser.add_option("-e", "--execute-modules",
    action="store_true", dest="execute_modules",
    default=False, help="Execute modules")
  parser.add_option("-f", "--fetch-data",
    action="store_true", dest="fetch_data",
    default=False, help="Fetch market data")
  (options, args) = parser.parse_args()

  # Run all modules
  if(options.execute_modules is True):
    execute_modules()

  # Fetch all market data
  if(options.fetch_data is True):
    cbScraper.fetch_data()

  # Initialize Logging
  # TODO: Migrate to module specific call
  #cbLogger.setLoggingTo(_CORE_LOG_FILE)

  # Grab configurations
  # TODO: Migrate to module specific call
  #config = cbConfig.getConfig(_CORE_CONFIG_FILE)

#####################################################################################
# Main function call
#####################################################################################
# Namespace check of core program
if __name__ == '__main__':
    main()
