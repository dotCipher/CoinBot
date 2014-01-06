# __CoinBot__

## Description

CoinBot is a multi-function tool that can do many things related to all digital currencies, like scraping the web for data e-currency data and storing it locally, and even go to coin faucets for instant payouts.

CoinBot's primary purpose is to hit different e-currency faucets that are represented with a single python module per faucet.

It is organized the following way:

- Libs
	- Contains shared code between all modules/plugins.
- Plugins
	- Contains extra features that can be controlled by CoinBot.
- Modules
	- Contains all the python modules that each represent a different e-currency faucet.
- Setup
	- Contains all configuration options for customizing what CoinBot does.
- Coinbot.py
	- The main controller script that executes all of its child features.

## Features / Usage

### 1) Primary

The main function of CoinBot can be used to schedule the execution of individual modules for execution based on the system it's on.

To go to the main menu of CoinBot, execute the following:

	./CoinBot.py

#### Module Execution

If you wish to manually execute an individual module __(not recommended)__ then execute the following:

	./CoinBot.py -e <Module>
	
__OR__

	./CoinBot.py --execute-module <Module>

### 2) Plugin: Scraper

CoinBot also supports the dynamic use of web scraping a multitude of sites that present live data on all e-currencies.

__Before you execute the Scraper__ make sure you verify all of the API configs within the _Scraper/Apis_ directory.  

#### Plugin Execution

To start the scraper run the following:

	./CoinBot.py -s

#### API Configuration

The scraper is fitted with a way to dynamically parse the API config files for easy addition/modification/removal of any given API call.

The formatting used in the config files is outlined in the _Scraper/Apis/Template.ini_ file.  All APIs that are outlined in _Scraper/Apis_ (except Template.ini) are executed based on their contents.

For further information please refer to the _Scraper/Apis/Template.ini_ file.

## TODO

- Implement main menu for CoinBot
- Compile a list of viable faucets for use
- (See issue list for more)

## Author

dot_Cipher:
<a href="http://www.null-sec.net">Site</a>