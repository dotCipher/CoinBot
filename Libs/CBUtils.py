#!/usr/bin/python
####################################################################################
# File: CoinBot_Utils.py
# Purpose: A module that contains general purpose functions
# Constraints: Must be imported into a main namespace Python file
# Usage: import CoinBot_Utils
####################################################################################
# Imports
####################################################################################
import os, time
####################################################################################
# Globals
####################################################################################
_DATETIME_FORMAT='%m/%d/%Y_%H:%M:%S'
_DATE_FORMAT='%m-%d-%Y'
_TIME_FORMAT='%H_%M_%S'
####################################################################################
# Utilities
####################################################################################
# Time and date
def getTime():
	return time.strftime(_TIME_FORMAT)
def getDate():
	return time.strftime(_DATE_FORMAT)
def getDateTime():
	return time.strftime(_DATETIME_FORMAT)

# Create directory if none exist
def ensureDirPath(path):
	if not os.path.exists(path):
		os.makedirs(path)
		return False
	else:
		return True