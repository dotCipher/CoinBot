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

# Boilerplate
def fetch_json_data(url):
	r = requests.get(url)
	return r.json()

def fetch_data():


#f = open('myfile','w')
#f.write('hi there\n')
# python will convert \n to os.linesep
#f.close()
# you can omit in most cases as the destructor will call if

#import requests
#r = requests.get('someurl')
#print r.json()