# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from agents.models import Agent

class Mandat(models.Model):

	CONTRACTCHOICES = ( ('simple', 		'Simple'),
						('exclusive', 	'Exclusif'),
						('coexclusive', 'Co-exclusif'),
						('delegation', 	'Délégation'),
					)

	WHATCHOICES = ( 	('apartment', 	'Appartement'),
						('villa',	 	'Villa'),
						('parking', 	'Parking'),
					)


	SOLDCHOICES = ( 	('sold', 		'Vendu'),
						('ours', 		'Vendu par nous'),
						('others', 		'Vendu par autre agence'),
						('owner', 		'Vendu par propriétaire'),
						('cancelled', 	'Retiré par propriétaire'),
						('withdrawn', 	'Retiré par agence'),
					)

	agent = models.ForeignKey(Agent, related_name='mandat_agent', db_index=True, blank=True, null=True)
	number = models.IntegerField()
	contract = models.CharField(choices = CONTRACTCHOICES, max_length=255, blank=True, null=True)
	start_date = models.DateField()
	end_date = models.DateField()
	what = models.CharField(choices = WHATCHOICES, max_length=255, blank=True, null=True)
	size = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	owner = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	email = models.CharField(max_length=255, blank=True, null=True)
	telephone = models.CharField(max_length=255, blank=True, null=True)
	sale_price = models.IntegerField()
	commission = models.IntegerField(blank=True, null=True)
	commission_percent = models.IntegerField(blank=True, null=True)
	sold = models.CharField(choices = SOLDCHOICES, max_length=255, blank=True, null=True)

	class Meta:
		ordering = ["-start_date"]

	def __unicode__(self):
		return self.owner+' ('+self.address+')'

