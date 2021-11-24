#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime,json,sys,os
import django
from django.conf import settings
sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agency.settings")
django.setup()


from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned 
import common,rabbitutil as queueutil
from dateutil.parser import parse as parsedate
from django.db import close_old_connections

from clients.models import ClientLead,ClientActivity,ClientSearch
from agents.models import Agent,AgentMailbox
from news.models import News

close_old_connections()


""" Insert leads thread. (c) BienFacile 2018 """

agent_lookup = { }
reset = False

if reset:
	toremove = ['RightMove',]
	try:
		for source in toremove:
			# remove activities
			activities = ClientActivity.objects.filter(description__contains=source+' - ')
			for activity in activities:
				activity.delete()
			# remove news
			news = News.objects.filter(description__contains=source+' - ')
			for item in news:
				item.delete()
			# remove from search descriptions
			key = 'Added from '
			searches = ClientSearch.objects.filter(description__contains=key)
			for search in searches:
				olddescription = search.description.split("\n")
				newdescription = []
				for line in olddescription:
					if key not in line:
						newdescription.append(line)
				search.description = "\n".join(newdescription)
				### TEMP to remove duplicate phrases
				startswith = search.description[:20]
				indexpos = search.description.find(startswith, 10)
				if indexpos > 0:
					search.description = search.description[:indexpos]
				search.save()
	except Exception as e: print(e)

def add_lead(ch, method, properties, body):
	src = json.loads(body)
	print src

	# If reset = true, delete so we can re-insert
	try:
		lead = ClientLead.objects.get(source_id=src['source_id'])
		found = True
	except ObjectDoesNotExist,MultipleObjectsReturned:
		found = False

	if found and reset:
			lead.delete()
			found = False

	if not found:
		try:
			lead = ClientLead()
			src['date_created'] = parsedate(src['date_created']) if 'date_created' in src else None
			for key in ['source', 'source_url', 'source_id', 'name', 'phone', 'email', 'price', 'buying', 'selling', 'notes', 'date_created', 'language']:
				setattr(lead, key, src[key]) if key in src and src[key] != '' else None
			agent_id = None
			if src['to'] in agent_lookup:
				agent_id = agent_lookup[src['to']]
			else:
				try:
					mailbox = AgentMailbox.objects.get(email=src['to'])
					agent_id = mailbox.agent.id
					agent_lookup[src['to']] = agent_id
				except:
					print "Unable to find agent mailbox with address: "+src['to']
			if agent_id:
				setattr(lead, 'assigned_agent_id', agent_id)
				lead.save()
				ch.basic_ack(delivery_tag = method.delivery_tag)
		except Exception as e: print(e)
	else:
		ch.basic_ack(delivery_tag = method.delivery_tag)

try:
	queue = queueutil.ScraperQueue()
	queue.worker(common.CLIENTLEADSQUEUE, add_lead)
except KeyboardInterrupt:
	queue.close()
