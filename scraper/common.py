import re, datetime, time
from agency.settings import SERVER_ENVIRONMENT
""" Useful constants and functions shared by master and worker threads. (c) BienFacile 2013 """

QUEUE_SUFFIX = '_'+SERVER_ENVIRONMENT.lower()

SCANQUEUE = 'toscrape'+QUEUE_SUFFIX
UPDATEDBQUEUE = 'updatedb'+QUEUE_SUFFIX
MAILERQUEUE = 'mails'+QUEUE_SUFFIX
CLASSIFIEDIMAGESQUEUE = 'classifiedimages'+QUEUE_SUFFIX
CLIENTLEADSQUEUE = 'clientleads'+QUEUE_SUFFIX

def extract_domain(uri):
	domain = re.findall('/([a-z.*]+)/', uri)
	if domain:
		uri = domain[0]
	uri = uri.replace('www.', '')
	return uri

def get_scanqueue(uri):
	domain = extract_domain(uri)
	return SCANQUEUE + '.' + domain.replace('.', '_')

def absolute_link(old,new):
	if new[:4] == 'http':
		return new
	if new[0] == '/':
		return old[0:old.index('/',7)] + new
	return old[0:old.rindex('/')+1] + new

def dict2datetime(datedict, defaultdate): # take a dict and override elements in datetime
	try:
		return datetime.datetime(	'year' in datedict and datedict['year'] or defaultdate.year,
									'month' in datedict and datedict['month'] or defaultdate.month,
									'day' in datedict and datedict['day'] or defaultdate.day,
									'hour' in datedict and datedict['hour'] or defaultdate.hour,
									'minute' in datedict and datedict['minute'] or defaultdate.minute,
									0,0,None)
	except ValueError:
		return None
