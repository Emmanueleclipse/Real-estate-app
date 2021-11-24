from __future__ import unicode_literals
from django.db import models
from agents.models import Agent
from clients.models import Client
from notaires.models import Notaire

class Sale(models.Model):
	address = models.CharField(max_length=255, null=True, blank=True)
	size = models.IntegerField(null=True, blank=True)
	pieces = models.IntegerField(null=True, blank=True)
	floor = models.IntegerField(null=True, blank=True)
	sale_price = models.IntegerField(null=True, blank=True)

	buyer = models.ForeignKey(Client, null=True, blank=True, related_name='sale_buyer')
	seller = models.ForeignKey(Client, null=True, blank=True, related_name='sale_seller')

	agent_buyer = models.ForeignKey(Agent, null=True, blank=True, related_name='sale_agent_buyer')
	agent_seller = models.ForeignKey(Agent, null=True, blank=True, related_name='sale_agent_seller')

	notaire_buyer = models.ForeignKey(Notaire, null=True, blank=True, related_name='sale_notaire_buyer')
	notaire_clerk_buyer = models.ForeignKey(Notaire, null=True, blank=True, related_name='sale_clerk_buyer')
	notaire_seller = models.ForeignKey(Notaire, null=True, blank=True, related_name='sale_notaire_seller')
	notaire_clerk_seller = models.ForeignKey(Notaire, null=True, blank=True, related_name='sale_clerk_seller')

	total_commission = models.IntegerField(null=True, blank=True)
	agency_commission = models.IntegerField(null=True, blank=True)

	current_offer = models.ForeignKey('SaleOffer', null=True, blank=True, related_name='sale_current_offer')
	accepted_offer = models.ForeignKey('SaleOffer', null=True, blank=True, related_name='sale_accepted_offer')

	sale_lost = models.BooleanField(default=False)

	compromis_sent_buyer = models.DateField(null=True, blank=True)
	compromis_signed_buyer = models.DateField(null=True, blank=True)
	compromis_sent_seller = models.DateField(null=True, blank=True)
	compromis_signed_seller = models.DateField(null=True, blank=True)
	compromis_signed_received_buyer = models.DateField(null=True, blank=True)

	compromis_final_signing_date = models.DateField(null=True, blank=True)


	mortgage_required  = models.BooleanField(default=False)
	mortgage_offer_received = models.DateField(null=True, blank=True)

	signing_date = models.DateField(null=True, blank=True)
	signing_done = models.BooleanField(default=False)

	commission_received_agency = models.DateField(null=True, blank=True)
	commission_received_agent = models.DateField(null=True, blank=True)

	electricity_meter_reading = models.CharField(max_length=255, null=True, blank=True)
	electricity_meter_reading_offpeak = models.CharField(max_length=255, null=True, blank=True)
	water_meter_reading = models.CharField(max_length=255, null=True, blank=True)
	gas_meter_reading = models.CharField(max_length=255, null=True, blank=True)
	last_phone_info = models.CharField(max_length=255, null=True, blank=True)

	electicity_done  = models.BooleanField(default=False)
	gas_done  = models.BooleanField(default=False)
	water_done  = models.BooleanField(default=False)

	insurance_done  = models.BooleanField(default=False)

	notes = models.TextField(null=True, blank=True)

class SaleOffer(models.Model):
    sale = models.ForeignKey(Sale)
    offer_date = models.DateField(auto_now_add=True)
    offer_amount = models.IntegerField()
    offer_commission = models.IntegerField()
    loan_required = models.BooleanField(default=True)
    made_by_buyer = models.BooleanField(default=True)
    offer_type = models.CharField(max_length=255, null=True, blank=True)

    accepted_date = models.DateField(null=True, blank=True)
    rejected_date = models.DateField(null=True, blank=True)

class SaleCommission(models.Model):
    sale = models.ForeignKey(Sale)
    agent = models.ForeignKey(Agent, null=True, blank=True)
    amount = models.IntegerField()


