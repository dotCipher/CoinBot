#!/usr/bin/python
#####################################################################################
# File: CoinBot_Scraper.py
# Purpose: A Scraper module for fetching market data online for CoinBot
# Constraints: Must be imported into a main namespace Python file
# Usage: import CoinBot_Scraper
###############################################################################
# Import standard libraries
###############################################################################
import os, sys, inspect
import requests, threading
###############################################################################
# Project imports
###############################################################################
import Libs.CoinBot_Config as cbConfig
import Libs.CoinBot_Logging as cbLogger
import Libs.CoinBot_Utils as cbUtils
###############################################################################
# Global variables
###############################################################################
########### Static Location variables ###########
_FILE_FRAME=os.path.split(inspect.getfile( inspect.currentframe() ))
for element in _FILE_FRAME:
  if ".py" not in element:
    _SCRIPT_DIR = element
  if ".py" in element:
  	_SCRIPT_FILE = element
_SCRIPT_PATH=os.path.join(_SCRIPT_DIR, _SCRIPT_FILE)
# Folder Location variables
_DATA_FOLDER_NAME = "Data"
_DATA_DIR = os.path.join(_SCRIPT_DIR,_DATA_FOLDER_NAME)
# API Specific directory locations
_VIRCUREX_FOLDER_NAME = "Vircurex"
_VIRCUREX_DIR = os.path.join(_DATA_DIR, _VIRCUREX_FOLDER_NAME)
###############################################################################
# Core Functions
###############################################################################
# JSON Data wrapper
def getJSONData(url):
	r = requests.get(url)
	return r.json()
# Function timing scheduler
def scheduleFunction(interval, worker_func, iterations = 0):
	if(iterations > 1):
		threading.Timer(
			interval, 
			scheduleFunction, 
			[interval, worker_func, 0 if iterations == 0 else iterations-1]
		).start()
	elif(iterations == 1):
		worker_func()
###############################################################################
# API Calls: Vircurex
###############################################################################
# API Call Wrapper: Vircurex
def apiCall_Vircurex(callstr):
	url = "https://vircurex.com/api/"
	apiCall = url + callstr
	return getJSONData(apiCall)

# API Call: Vircurex - get_info_for_currency
def getInfoForCurrency():
	call = "get_info_for_currency.json"
	return apiCall_Vircurex(call)
# API Call: Vircurex - get_lowest_ask
def getLowestAsk(base, alt):
	call = "get_lowest_ask.json?base=" + base + "&alt=" + alt
	return apiCall_Vircurex(call)
# API Call: Vircurex - get_highest_bid
def getHighestBid(base, alt):
	call = "get_highest_bid.json?base=" + base + "&alt=" + alt
	return apiCall_Vircurex(call)
# API Call: Vircurex - get_last_trade
def getLastTrade(base, alt):
	call = "get_last_trade.json?base=" + base + "&alt=" + alt
	return apiCall_Vircurex(call)
# API Call: Vircurex - get_volume
def getVolume(base, alt):
	call = "get_volume.json?base=" + base + "&alt=" + alt
	return apiCall_Vircurex(call)

# API Caller for: Vircurex
def execCalls_Vircurex():
	currencies = ['BTC', 'FTC', 'LTC', 'USD']
	# Execute get of summary
	summary = getInfoForCurrency()
	# Execute all api calls with all pairs
	i = 0
	while i < len(currencies):
		base = currencies[i]
		# Build alt list
		j = 0
		alt_list = []
		while j < len(currencies):
			if not currencies[i] == currencies[j]:
				alt_list.append(currencies[j])
			j += 1
		i += 1
		# Iterate through alt list with bases
		j = 0
		while j < len(alt_list):
			alt = alt_list[j]
			low = getLowestAsk(base, alt[j])
			high = getHighestBid(base, alt[j])
			trade = getLastTrade(base, alt[j])
			volumne = getVolume(base, alt[j])
			j += 1
###############################################################################
# Main Call
###############################################################################
# Main plugin call
def start_scraper():
	# First check if 'data' directory exists
	# Create directory if it doesnt exist
	#ensureDirPath(_DATA_DIR)
	# Second check if 'data/<API> directory exists
	# Create directory if it doesnt exist
	#ensureDirPath(_VIRCUREX_DIR)
	# Get current time and date
	# TODO
	# Output to filename of date in folder tree of:
	#  'data/<API_LOC>/<API_CALL>/<date>/<time>.json'
	#  ie. 'data/Vircurex/getLowestAsk/12-3-2013/4_20_PM.json'
	#  or  'data/Vircurex/getHighestBid_BTC-FTC/12-4-2013/4_20_PM.json'
	# from running:
	#  scheduleFunction(60, execCalls_Vircurex)
	print "In Scraper:"

#f = open('myfile','w')
#f.write('hi there\n')
# python will convert \n to os.linesep
#f.close()
# you can omit in most cases as the destructor will call if

#import requests
#r = requests.get('someurl')
#print r.json()