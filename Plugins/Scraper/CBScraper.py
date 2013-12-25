#!/usr/bin/python
#####################################################################################
# File: CoinBot_Scraper.py
# Purpose: A Scraper plugin for fetching market data online for CoinBot
# Constraints: Must be imported into a main namespace Python file
# Usage: import CoinBot_Scraper
###############################################################################
# Import standard libraries
###############################################################################
import os, sys, inspect, signal
import requests, threading, time
###############################################################################
# Project imports
###############################################################################
import Libs.CBConfig as cbConfig
import Libs.CBUtils as cbUtils
import Libs.CBLogging as cbLogging
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
# Configs
_CONFIG_NAME="CBScraperConfig.ini"
_CONFIG_FILE=os.path.join(_SCRIPT_DIR,_CONFIG_NAME)
###############################################################################
# Core functions
###############################################################################
# Get output locations
def getOutputDirectory():
	config = cbConfig.getConfig(_CONFIG_FILE)
	for section in config.sections():
		for option in config.options(section):
			if option == "output-directory":
				return config.get(section, option)
###############################################################################
# Thread scheduling functions
###############################################################################
# FunctionThread schedule wrapper
# iters = -1 (run infinitely)
def runFunction(interval, iters, worker_func):
	if iters == -1:
		while True:
			worker_func()
			time.sleep(interval)
	elif iters >= 1:
		while iters > 0:
			worker_func()
			iters -= 1
			if iters != 0:
				time.sleep(interval)
			else:
				break
###############################################################################
# API Calls: Vircurex
###############################################################################
# API Call Wrapper: Vircurex
def callVircurex(callstr):
	url = "https://vircurex.com/api/"
	apiCall = url + callstr
	return str(requests.get(apiCall).json)

# API Call: Vircurex - get_info_for_currency
def getInfoForCurrency():
	call = "get_info_for_currency.json"
	return callVircurex(call)
# API Call: Vircurex - get_lowest_ask
def getLowestAsk(base, alt):
	call = "get_lowest_ask.json?base=" + base + "&alt=" + alt
	return callVircurex(call)
# API Call: Vircurex - get_highest_bid
def getHighestBid(base, alt):
	call = "get_highest_bid.json?base=" + base + "&alt=" + alt
	return callVircurex(call)
# API Call: Vircurex - get_last_trade
def getLastTrade(base, alt):
	call = "get_last_trade.json?base=" + base + "&alt=" + alt
	return callVircurex(call)
# API Call: Vircurex - get_volume
def getVolume(base, alt):
	call = "get_volume.json?base=" + base + "&alt=" + alt
	return callVircurex(call)

# API Caller for: Vircurex
def execVircurex():
	folderName = "Vircurex"
	# Check base output directory
	baseDir = getOutputDirectory()
	apiDir = os.path.join(baseDir, folderName)
	# Set logging
	cbLogging.setLoggingTo('stdout')
	cbLogging.logInfo("API Directory at: " + apiDir)
	
	# Execute get of summary and write out
	summary = getInfoForCurrency()
	sDir = os.path.join(apiDir, "getInfoForCurrency")
	sDateDir = os.path.join(sDir, getDate())
	cbUtils.ensureDirPath(sDateDir)
	timeFileName = getTime() + ".txt"
	sTimeFile = os.path.join(sDateDir, timeFileName)
	f = open(sTimeFile, 'w')
	f.write(summary)
	f.close()

	# Write output for getInfoForCurrency
	cbLogging.logInfo("")

	# # Outline currencies
	# currencies = ['BTC', 'FTC', 'LTC', 'USD']
	# # Execute all api calls with all pairs
	# i = 0
	# while i < len(currencies):
	# 	base = currencies[i]
	# 	# Build alt list
	# 	j = 0
	# 	alt_list = []
	# 	while j < len(currencies):
	# 		if not currencies[i] == currencies[j]:
	# 			alt_list.append(currencies[j])
	# 		j += 1
	# 	i += 1
	# 	# Iterate through alt list with bases
	# 	j = 0
	# 	while j < len(alt_list):
	# 		alt = alt_list[j]
	# 		low = getLowestAsk(base, alt[j])
	# 		high = getHighestBid(base, alt[j])
	# 		trade = getLastTrade(base, alt[j])
	# 		volumne = getVolume(base, alt[j])
	# 		# TODO: Do stuff with each
	# 		j += 1
###############################################################################
# Main Call
###############################################################################
def test():
	d = getOutputDirectory()
	base = os.path.join(d, "Test")
	t = getTime() + ".txt"
	tFile = os.path.join(base, t)
	print tFile
# Main plugin call
def start_scraper():
	# First check if '<DIR>' output directory exists
	# Create directory if it doesnt exist
	#ensureDirPath(getOutputDirectory())
	# Second check if '<DIR>/<API> directory exists
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
	runFunction(30, 2, execVircurex)