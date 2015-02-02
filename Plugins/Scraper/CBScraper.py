#!/usr/bin/python
#####################################################################################
# File: CoinBot_Scraper.py
# Purpose: A Scraper plugin for fetching market data online for CoinBot
# Constraints: Must be imported into a main namespace Python file
# Usage: import CoinBot_Scraper
###############################################################################
# Import standard libraries
###############################################################################
import os, sys, inspect, signal, re
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
# Writes an API call to its correct file
def writeCallOutput(apiName, outdir, callStr, callOutput):
	# Output to filename of date in folder tree of:
	#  'data/<API_LOC>/<API_CALL>/<date>/<time>.json'
	#  ie. 'data/Vircurex/getLowestAsk/12-3-2013/4_20_PM.json'
	#  or  'data/Vircurex/getHighestBid_BTC-FTC/12-4-2013/4_20_PM.json'
	# Set logging
	cbLogging.setLoggingTo('stdout')
	# Build dir vars
	title = cbUtils.scrubFilename(callStr)
	apiDir = os.path.join(outdir, apiName)
	callDir = os.path.join(apiDir, title)
	callDateDir = os.path.join(callDir, cbUtils.getDate())
	# Check output dir
	cbUtils.ensureDirPath(callDateDir)
	# Build output file in dir
	timeFileName = cbUtils.getTime() + ".txt"
	callTimeFile = os.path.join(callDateDir, timeFileName)
	# Write out to file + log
	f = open(callTimeFile, 'w')
	f.write(callOutput)
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
# Scrapex functions
###############################################################################
scrapex = ["{BASE}", "{ALT}"]
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
###############################################################################
# API Calls
###############################################################################
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
# Processes all API Config objects given in the list
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
						callList.append(callStr)
						j += 1
			else:
				callList.append(call)
		# Execute all calls from callList
		for call in callList:
			executeAPICall(apiName, apiUrl, call, apiOutdir)
def executeAPICall(apiName, apiUrl, callStr, outdir):
	# Execute api call
	callOutput = json.dumps(
		requests.get(apiUrl + callStr).json
	)
	# Write output
	writeCallOutput(apiName, outdir, callStr, callOutput)
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