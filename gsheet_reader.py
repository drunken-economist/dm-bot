import codecs
import configparser
import csv
import requests
from contextlib import closing
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

config = configparser.ConfigParser()
config.read('config.ini')

def read_tldr(session_date=None):
	print('looking for tldr with session_date of ' + session_date)
	url = config['CSV']['tldr_csv']
	with closing(requests.get(url, stream=True)) as r:
		reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter = ',', quotechar='"')
		for row in reader:
			if session_date == row[0]:
				return row
		row[1] = row[1] + ' \n[date `{}` not found, using latest session]'.format(session_date)
		return row

def current_xp():
	url = config['CSV']['log_csv']
	with closing(requests.get(url, stream=True)) as r:
		reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter = ',', quotechar='"')
		for row in reader:
			xp = row[10]
			level = row[11]
		return [xp, level]

def whois(npc_name='list'):
	npcs = {}
	url = config['CSV']['whois_csv']
	with closing(requests.get(url, stream=True)) as r:
		reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter = ',', quotechar='"')
		for row in reader:
			name = row[0]
			description = row[1]
			npcs[name] = description
		if npc_name.lower() == 'list':
			response = 'You can ask about the following NPCs:'
			for npc_name in list(npcs.keys()):
				response = response + '\n' + npc_name
			return response
		search_match = process.extractOne(npc_name, list(npcs.keys()))
		response = '*{}*\n_(match score: {})_\n{}'.format(search_match[0], search_match[1], npcs[search_match[0]])
		return response