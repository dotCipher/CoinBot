#!/usr/bin/python
#####################################################################################
# File: CoinBot_Config.py
# Purpose: A Configuration module for configuration of CoinBot
# Constraints: Must be imported into a main namespace Python file
# Usage: import CoinBot_Config
#####################################################################################
# Imports
#####################################################################################
import os
import ConfigParser
####################################################################################
# Configuration functions
#####################################################################################
# Gets config file as variable
# Returns: config OR None (Object)
def getConfig(configfile):
  if not os.path.exists(configfile):
    return None
  configDictionary = {}
  config = ConfigParser.ConfigParser()
  config.read(configfile)
  return config

# Given config, prints full config file to console
# Returns: (void)
def printConfig(config):
  for section in config.sections():
    print "[" + section + "]"
    for option in config.options(section):
      print option + ":"
      print config.get(section, option)
