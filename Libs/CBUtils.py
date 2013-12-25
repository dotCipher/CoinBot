#!/usr/bin/python
####################################################################################
# File: CoinBot_Utils.py
# Purpose: A module that contains general purpose functions
# Constraints: Must be imported into a main namespace Python file
# Usage: import CoinBot_Utils
####################################################################################
# Imports
####################################################################################
import os
####################################################################################
# Globals
####################################################################################
_DATETIME_FORMAT='%m/%d/%Y_%H:%M:%S'
_DATE_FORMAT='%m-%d-%Y'
_TIME_FORMAT='%H_%M_%S'
####################################################################################
# Utilities
####################################################################################
# Unicode to ASCII decoder for JSON
def decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = decode_list(item)
        elif isinstance(item, dict):
            item = decode_dict(item)
        rv.append(item)
    return rv
def decode_dict(data):
	rv = {}
	for key, value in data.iteritems():
		if isinstance(key, unicode):
			key = key.encode('utf-8')
		if isinstance(value, unicode):
			value = value.encode('utf-8')
		elif isinstance(value, list):
			value = decode_list(value)
		elif isinstance(value, dict):
			value = decode_dict(value)
		rv[key] = value
	return rv

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