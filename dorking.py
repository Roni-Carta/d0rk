"""d0rk.

Usage:
	dorking.py dork <query> [--pages=K]
	dorking.py dork engine <engine> <query> [--pages=K]

Options:
  -h --help     Show this screen.
  --version 	Show version.

"""

import re
import os
import sys
import json
import time
import signal
import requests

import gspread
import urllib.parse

from pprint import pprint
from docopt import docopt
from bs4 import BeautifulSoup
from requests.utils import requote_uri
from oauth2client.service_account import ServiceAccountCredentials

if (sys.version_info>=(3, 0, 0,)):
	from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
else:
	from urlparse import urlparse, parse_qs, urlunparse
	from urllib import urlencode

spreadsheet = "Dorking"

DIR = os.path.dirname(os.path.realpath(__file__))
CREDS = DIR + "/creds.json"
CONFIG = DIR + "/config/engines.json"
# Setup the sheet to work with
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS, scope) # JSON credentials file provided by google
client = gspread.authorize(creds)
idi = client.create(spreadsheet) 
sheet = client.open(spreadsheet).sheet1

def signal_handler(sig, frame):
	print("\rExiting so soon ? Hope to see you back =D")
	client.del_spreadsheet(idi.id)
	sys.exit(0)


def yahoo_redirect(url):
	if "search.yahoo.com" in url:
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'html.parser')
		meta_tag = soup.find(attrs={"http-equiv": "refresh"})
		if meta_tag:
			redirect = re.findall(r'(https?://\S+)', meta_tag["content"])[0]
			yahoo_redirect(redirect)
	else:
		if "yahoo" not in url:
			if "'" == url[-1]:
				url = url[:-1]
			print(url)

def google_filter(url):
	i = 4
	uu = list(urlparse(url))
	for idx, param in enumerate(uu): 
		if "ved" in param:
			i = idx
	qs = parse_qs(uu[i], keep_blank_values=True)
	if qs['sa']:
		del(qs['sa'])
	if qs['ved']:
		del(qs['ved'])
	if qs['usg']:
		del(qs['usg'])
	uu[i] = urlencode(qs, doseq=True)
	new_url = urlunparse(uu)
	print(new_url)

class Engine:
	""" Search Engine : Will query and scrap the results from a reasearch """
	def __init__(self, search, pages, engine="duckduckgo"):
		self.config(engine)
		self.engine = engine
		self.pages = pages
		self.search = search
		self.query = self.config[engine]["query"]
		self.param = self.config[engine]["param"]
		self.increment = self.config[engine]["k"]
		self.filters = self.config[engine]["filters"]

	def config(self, engine):
		# Loads the JSON file
		with open(CONFIG) as json_file:
			self.config =  json.load(json_file)

	def dork(self): 
		# Query spreadsheet
		if not self.pages:
			self.pages = "1"

		for i in range(int(self.pages)):
			# Increment the page parameter
			j = self.increment * i
			url = self.query + self.search + self.param + str(j)
		
			# Google Spreadsheet trick
			search = requote_uri(url)

			sheet.update_cell(1,1, search)
			sheet.update_cell(2,1, '=IMPORTXML(A1; "//a/@href")')

			self.results()
			time.sleep(5)

	def results(self):
		# Read the Results from spreadsheet
		urls = []
		results = sheet.col_values(1)
		for url in results:
			url = urllib.parse.unquote(url)
			if self.engine == "youtube":
				urls.extend(re.findall(r'/watch\?v=.*', url))
			else:
				urls.extend(re.findall(r'(https?://\S+)', url))

		
		self.filter(urls)
		
	
	def filter(self, results):
		# Filter unwanted stuff
		results = [string for string in results if string != ""]
		results = list(set(results))
		for url in results:
			if any(f in url for f in self.filters.values()):
				continue
			# Yahoo doesn't show the url but a proxy
			# We need to follow redirect in order to get results
			if self.engine == "yahoo":
				yahoo_redirect(url)
			# Google add multiple useless parameters to the results
			elif self.engine == "google":
				google_filter(url)
			elif self.engine == "youtube":
				print("https://www.youtube.com" + url)
			else:
				print(url)

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	args = docopt(__doc__, version='d0rk PoC BETA')
	if args['dork']:
		if args['engine']:
			engine = Engine(args['<query>'], args['--pages'], args['<engine>'])
			engine.dork()
		else:
			engine = Engine(args['<query>'], args['--pages'])
			engine.dork()
			
	client.del_spreadsheet(idi.id)

