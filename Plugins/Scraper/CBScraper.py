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
import simplejson as json
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
_CONFIG_FILE=os.path.join(_SCRIPT_DIR, _CONFIG_NAME)
# Apis
_APIS_NAME = "Apis"
_APIS_DIR = os.path.join(_SCRIPT_DIR, _APIS_NAME)
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
# Writes an API call to its correct file
def writeCallOutput(api, title, output):
	# Output to filename of date in folder tree of:
	#  'data/<API_LOC>/<API_CALL>/<date>/<time>.json'
	#  ie. 'data/Vircurex/getLowestAsk/12-3-2013/4_20_PM.json'
	#  or  'data/Vircurex/getHighestBid_BTC-FTC/12-4-2013/4_20_PM.json'
	# Set logging
	cbLogging.setLoggingTo('stdout')
	# Build dir vars
	baseDir = getOutputDirectory()
	apiDir = os.path.join(baseDir, api)
	callDir = os.path.join(apiDir, title)
	callDateDir = os.path.join(callDir, cbUtils.getDate())
	# Check output dir
	cbUtils.ensureDirPath(callDateDir)
	# Build output file in dir
	timeFileName = cbUtils.getTime() + ".txt"
	callTimeFile = os.path.join(callDateDir, timeFileName)
	# Write out to file + log
	f = open(callTimeFile, 'w')
	f.write(output)
	f.close()
	cbLogging.logInfo(title + " written in " + callTimeFile)
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
	return json.dumps(requests.get(apiCall).json)

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
	API_NAME = "Vircurex"
	# Execute get of summary and write out
	writeCallOutput(
		API_NAME,
		"getInfoForCurrency",
		getInfoForCurrency()
	)
	# Outline currencies
	currencies = ['BTC', 'FTC', 'LTC', 'USD']
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
			# getLowestAsk
			writeCallOutput(
				API_NAME,
				"getLowestAsk_" + base + "-" + alt,
				getLowestAsk(base, alt)
			)
			# getHighestBid
			writeCallOutput(
				API_NAME,
				"getHighestBid_" + base + "-" + alt,
				getHighestBid(base, alt)
			)
			# getLastTrade
			writeCallOutput(
				API_NAME,
				"getLastTrade_" + base + "-" + alt,
				getLastTrade(base, alt)
			)
			# getVolume
			writeCallOutput(
				API_NAME,
				"getVolume_" + base + "-" + alt,
				getVolume(base, alt)
			)
			j += 1
#############################################
# NOTE: These methods are still in development
# Read all API config files
def readApiConfigs():
	hasPath = cbUtils.ensureDirPath(_APIS_DIR)
	if not hasPath:
		return None
	else:
		fileList = []
		apiConfigs = []
		os.chdir(_APIS_DIR)
		# Get all API configs
		for f in os.listdir("."):
			if (f.endswith(".ini")) and (not(f == "Template.ini")):
				fileList.append(f)
		# Parse all API configs
		for f in fileList:
			config = cbConfig.getConfig(f)
			apiConfigs.append(config)
		return apiConfigs
# # Processes all API Config objects given in the list
def processAPIConfigs(apiConfigList):
	for apiConfig in apiConfigList:
		# CORE values
		apiName = apiConfig.get("CORE", "name")
		apiUrl = apiConfig.get("CORE", "url")
		apiOutdir = apiConfig.get("CORE", "outdir")
		apiCurrs = apiConfig.get("CORE", "currs").split('\n')
		# API values
		apiCalls = apiConfig.get("API", "calls").split('\n')
		callList = []
		# Build call list
		for call in apiCalls:
			if hasScrapex(call):
				# Build call string by replacing with Scrapex
				i = 0
				while i < len(apiCurrs):
					base = apiCurrs[i]
					j = 0
					alt_list = []
					while j < len(apiCurrs):
						if not apiCurrs[i] == apiCurrs[j]:
							alt_list.append(apiCurrs[j])
						j += 1
					i += 1
					# Iterate through alt list with bases
					j = 0
					while j < len(alt_list):
						alt = alt_list[j]
						callStr = replaceScrapex(call, base, alt)
						callList.append(apiUrl + callStr)
						j += 1
			else:
				callList.append(apiUrl + call)
		print callList
def replaceScrapex(string, base, alt):
	baseRepl = string.replace("{BASE}", base)
	altRepl = baseRepl.replace("{ALT}", alt)
	return altRepl
def hasScrapex(string):
	scrapex = ["{BASE}", "{ALT}"]
	for exp in scrapex:
		if exp in string:
			return True
	return False
#def executeAPICall(apiName, callStr, outdir):
#############################################
###############################################################################
# Main Calls
###############################################################################
# All executions will be registered in this loop
def scraperLoop():
	#execVircurex()
	apiConfigs = readApiConfigs()
	processAPIConfigs(apiConfigs)
# Main plugin call
def start_scraper():
	# Run all registered scrapers
	cbLogging.setLoggingTo('stdout')
	cbLogging.logInfo("Scraper starting, press Ctrl+C to stop...")
	# Run each function every minute
	runFunction(60, -1, scraperLoop)