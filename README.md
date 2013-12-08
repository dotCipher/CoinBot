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

### 2) Scraper

CoinBot also supports the dynamic use of web scraping a multitude of sites that present live data on all e-currencies.

## TODO

- Update Logger to be more verbose for all types of logging
- Finish implementation of Scraper
- Implement main menu for CoinBot
- Compile a list of viable faucets for use

## Author

* User : @dot_Cipher