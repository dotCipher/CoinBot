#!/usr/bin/python
#####################################################################################
# File: CoinBot_Logging.py
# Purpose: A Logger module for custom logging of CoinBot
# Constraints: Must be imported into a main namespace Python file
# Usage: import CoinBot_Logging
#####################################################################################
# Imports
#####################################################################################
import os
import logging
#####################################################################################
# Logging system functions
#####################################################################################
# Initializes the logging system
# Returns: (void)
def setLoggingTo(logfilePath):
  if not os.path.exists(logfilePath):
    if not os.path.exists(os.path.dirname(os.path.realpath(logfilePath))):
      os.makedirs(os.path.dirname(os.path.realpath(logfilePath)))
  logging.basicConfig(level=logging.DEBUG, 
    filename=logfilePath, filemode='a+',
    format='[%(asctime)s_%(msecs)d]:%(levelname)s:%(message)s', 
    datefmt='%m/%d/%Y_%H:%M:%S')

# Wrapper for logging level = DEBUG
# Returns: (void)
def logDebug(msg):
  logging.debug(msg)

# Wrapper for logging level = INFO
# Returns: (void)
def logInfo(msg):
  logging.info(msg)

# Wrapper for logging level = WARNING
# Returns: (void)
def logWarning(msg):
  logging.warning(msg)

# Wrapper for logging level = ERROR
# Returns: (void)
def logError(msg):
  logging.error(msg)

# Wrapper for logging level = CRITICAL
# Returns: (void)
def logCritical(msg):
  logging.critical(msg)

# Given a logfile, clears the entire log
# Returns: True OR False (Boolean)
def clearLog(logfile):
  if not os.path.exists(logfile):
    return False
  with open(logfile, 'w'):
    pass
    return True
