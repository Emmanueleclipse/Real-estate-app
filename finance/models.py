# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from agents.models import Agency,Agent
from files.models import Upload

class Supplier(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	siret = models.CharField(max_length=255,null=True,blank=True)
	vat_number = models.CharField(max_length=255,null=True,blank=True)
	category = models.CharField(max_length=255,null=True,blank=True)
	tags = models.CharField(max_length=255,null=True,blank=True)
	agency = models.ForeignKey(Agency, related_name='supplier_agency', db_index=True)
	created_by = models.ForeignKey(Agent, related_name='supplier_agent',blank=True, null=True)

	class Meta:
		ordering = ["name"]

	def __unicode__(self):
		return self.name

class FactureSupplier(models.Model):
	date = models.DateField()
	supplier = models.ForeignKey(Supplier, related_name='facture_supplier',blank=True, null=True)
	invoice_number = models.CharField(max_length=255,blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	amount = models.DecimalField(max_digits=6, decimal_places=2)
	vat = models.BooleanField(default=True)
	facture = models.ForeignKey(Upload, related_name='facturesupplier_upload',blank=True, null=True)
	agency = models.ForeignKey(Agency, related_name='facturesupplier_agency', db_index=True)
	submitted_by = models.ForeignKey(Agent, related_name='facturesupplier_agent',blank=True, null=True)
	paid = models.BooleanField(default=False)

	class Meta:
		ordering = ["-date"]

	def __unicode__(self):
		return self.supplier+' €'+self.amount


class BankAccount(models.Model):
	bank_name = models.CharField(max_length=255)
	bank_address = models.CharField(max_length=255)
	account_name = models.CharField(max_length=255)
	iban = models.CharField(max_length=255)
	bic = models.CharField(max_length=255,null=True,blank=True)
	opened_date = models.DateField(null=True,blank=True)
	closed_date = models.DateField(null=True,blank=True)
	agent = models.ForeignKey(Agent, related_name='bankaccount_agent',blank=True, null=True, db_index=True)
	agency = models.ForeignKey(Agency, related_name='bankaccount_agency',blank=True, null=True, db_index=True)
	current = models.BooleanField(default=True)
	balance = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

	class Meta:
		ordering = ["-opened_date"]

	def __unicode__(self):
		return self.account_name+' ('+self.bank_name+')'

class BankEntry(models.Model):
	bank_account = models.ForeignKey(BankAccount, related_name='bankentry_account', db_index=True)
	date = models.DateField()
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	reference = models.CharField(max_length=255)
	comment = models.CharField(max_length=255)

	class Meta:
		ordering = ["-date"]

	def __unicode__(self):
		return '€'+self.amount

class FactureNotaire(models.Model):
	date = models.DateField()
	invoice_number = models.CharField(max_length=255)
	agent = models.ForeignKey(Agent, related_name='facturenotaire_agent', db_index=True)
	client_name = models.CharField(max_length=255)
	client_address = models.CharField(max_length=255, null=True, blank=True)
	other_agency = models.CharField(max_length=255, null=True, blank=True)
	property_address = models.CharField(max_length=255)
	commission = models.IntegerField()
	bank_account = models.ForeignKey(BankAccount, related_name='facturenotaire_bankaccount')
	paid = models.BooleanField(default=False)
	facture = models.ForeignKey(Upload, related_name='facturenotaire_upload',blank=True, null=True)
	notaire = models.CharField(max_length=255, null=True, blank=True)

	class Meta:
		ordering = ["-date"]

	def description(self):
		return self.client_name+' ('+self.property_address+')'

	def __unicode__(self):
		return self.description()

class FactureAgent(models.Model):
	date = models.DateField()
	invoice_number = models.CharField(max_length=255)
	agent = models.ForeignKey(Agent, related_name='factureagent_agent', db_index=True)
	sale = models.ForeignKey(FactureNotaire, related_name='factureagent_sale', db_index=True)
	commission = models.IntegerField(blank=True, null=True)
	commission_percent = models.IntegerField(blank=True, null=True)
	vat = models.BooleanField(default=False)
	bank_account = models.ForeignKey(BankAccount, related_name='factureagent_bankaccount')
	paid = models.BooleanField(default=False)
	facture = models.ForeignKey(Upload, related_name='factureagent_upload',blank=True, null=True)

	class Meta:
		ordering = ["-date"]

	def __unicode__(self):
		return self.sale

class FactureApporteur(models.Model):
	date = models.DateField()
	invoice_number = models.CharField(max_length=255)
	siret = models.CharField(max_length=255,null=True,blank=True)
	name = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	iban = models.CharField(max_length=255)
	bic = models.CharField(max_length=255,null=True,blank=True)
	agent = models.ForeignKey(Agent, related_name='factureapporteur_agent', db_index=True)
	sale = models.ForeignKey(FactureNotaire, related_name='factureapporteur_sale', db_index=True)
	commission = models.IntegerField()
	vat = models.BooleanField(default=False)
	paid = models.BooleanField(default=False)
	facture = models.ForeignKey(Upload, related_name='factureapporteur_upload',blank=True, null=True)

	class Meta:
		ordering = ["-date"]

	def __unicode__(self):
		return self.name+' - '+self.sale
