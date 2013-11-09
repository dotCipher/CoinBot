#!/usr/bin/python
#####################################################################################
# File: CB_ModuleTemplate.py
# Purpose: This module is only meant as a template to other modules
#####################################################################################
# Imports
#####################################################################################
import os
import random
import time
# Project libraries
import Libs.CoinBot_Config as cbConfig
import Libs.CoinBot_Logging as cbLogger
#####################################################################################
# Global variables
#####################################################################################
_SITE_URL="http://www.google.com/"
_MOD_NAME=os.path.split(inspect.getfile( inspect.currentframe() ))[0]
#####################################################################################
# Module helpers
#####################################################################################
# Given a nMin and nMax, havee program wait random time between interval
# Returns: (void)
def randomWait(nMin, nMax):
	if(nMin >= nMax):
		waitTime = random.uniform(nMin, nMin+1)
	else:
		waitTime = random.uniform(nMin,nMax)
	print "Waiting for: " + waitTime
	time.sleep(waitTime)
	print "BAM!"
#####################################################################################
# Module Function
#####################################################################################
# Given a configFilePath, and logDirPath, execute module logic
# Returns: True OR False (Boolean)
def executeModule(configFilePath, logDirPath):
	print "STARTING"
	# Set logger
	logFile = os.path.join(logDir, _MOD_NAME)
	cbLogger.setLoggingTo(logFile)
	# Pull data from config file
	config = cbConfig.getConfig(configFile)
	#config.get("Bitcoin", "Wallet-Addresses").split("\n")
	randomWait(1, 10)
	randomWait(2, 4)
	randomWait(7, 12)
	randomWait(100, 200)
	print "HEY!"