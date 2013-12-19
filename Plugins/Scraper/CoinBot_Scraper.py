#!/usr/bin/python
#####################################################################################
# File: CoinBot_Scraper.py
# Purpose: A Scraper module for fetching market data online for CoinBot
# Constraints: Must be imported into a main namespace Python file
# Usage: import CoinBot_Scraper
#####################################################################################
# Imports
#####################################################################################
import os
import logging
import requests
import threading
from sets import Set

#####################################################################################
# Core Utilities
#####################################################################################
# JSON Data wrapper
def getJSONData(url):
	r = requests.get(url)
	return r.json()
# Function timing scheduler
def scheduleFunction(interval, worker_func, iterations = 0):
	if(iterations != 1):
		threading.Timer(
			interval, 
			scheduleFunction, 
			[interval, worker_func, 0 if iterations == 0 else iterations-1]
		).start()
	else:
		worker_func()

#####################################################################################
# API Calls: Vircurex
#####################################################################################
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
	currencies = Set(["BTC", "FTC", "LTC", "USD"])
	# Execute get of summary
	summary = getInfoForCurrency()
	# Execute all api calls with all pairs
	for i in currencies:
		base = currencies[i]
		alt_list = currencies - base
		for j in alt_list:
			low = getLowestAsk(base, alt[j])
			high = getHighestBid(base, alt[j])
			trade = getLastTrade(base, alt[j])
			volumne = getVolume(base, alt[j])


#####################################################################################
# Main Call
#####################################################################################
# Main plugin call
def start_scraper():
	# First check if 'data' directory exists
	# Create directory if it doesnt exist
	# Second check if 'data/<API> directory exists
	# Create directory if it doesnt exist
	# Get current time and date
	# Output to filename of date in folder tree of:
	#  'data/<API_LOC>/<API_CALL>/<date>/<time>.json'
	#  ie. 'data/Vircurex/getLowestAsk/12-3-2013/4_20_PM.json'
	#  or  'data/Vircurex/getHighestBid_BTC-FTC/12-4-2013/4_20_PM.json'
	# from running:
	#  scheduleFunction(60, execCalls_Vircurex)
	print "In Scraper"

#f = open('myfile','w')
#f.write('hi there\n')
# python will convert \n to os.linesep
#f.close()
# you can omit in most cases as the destructor will call if

#import requests
#r = requests.get('someurl')
#print r.json()