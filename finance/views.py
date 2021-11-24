# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv, re
from dateutil.parser import parse

from django.http import HttpResponse, JsonResponse
from django.views.generic import View,TemplateView
from agency.utils import JsonException, JsonReport, pkobject, editobject, setobject
from finance.models import Supplier, FactureSupplier, BankAccount, BankEntry, FactureNotaire, FactureAgent, FactureApporteur
from agents.models import Agent

class SuppliersView(TemplateView):
    template_name = "suppliers.html"

class SuppliersFactureView(TemplateView):
    template_name = "suppliers_facture.html"

class BankAccountView(TemplateView):
    template_name = "banks.html"

class NotairesFactureView(TemplateView):
    template_name = "notaires_facture.html"

class AgentsFactureView(TemplateView):
    template_name = "agents_facture.html"

class ApporteursFactureView(TemplateView):
    template_name = "apporteurs_facture.html"

class SommaireFinanceView(TemplateView):
    template_name = "finance_summary.html"


def json_suppliers(request):
	if request.method == 'POST':
		fields = [
					{ 'name': 'name', 'required': True }, 
					{ 'name': 'description', },
					{ 'name': 'siret', },
					{ 'name': 'vat_number', },
					{ 'name': 'category', },
					{ 'name': 'tags', },
				]
		try:
			# Get if ID or create
			pk = pkobject(request.POST)
			item, created = Supplier.objects.filter(agency = request.user.agency, pk=pk).get_or_create() if pk else (Supplier(), True)
			if editobject(request.POST, item, created):
				if created:
					item.agency = request.user.agency
				# Set fields and save
				if setobject(request.POST, item, fields):
					item.save()
		except Exception as e:
			return JsonException(e)

	results = []
	suppliers = Supplier.objects.filter(agency=request.user.agency).order_by('name')[:1000]
	for supplier in suppliers:
		results.append({ 'id': int(supplier.id), 'name' : supplier.name, 'description' : supplier.description, 'tags' : supplier.tags, 'siret' : supplier.siret, 'vat_number' : supplier.vat_number, 'category' : supplier.category })
	return JsonResponse(results, safe=False)

def json_suppliers_facture(request):
	if request.method == 'POST':
		fields = [
					{ 'name': 'supplier', 'required': True,'key' : 'supplier', 'foreignkey' : True, }, 
					{ 'name': 'invoice_number', },
					{ 'name': 'description', },
					{ 'name': 'amount', 'type' : 'decimal', },
					{ 'name': 'vat', 'type': 'boolean', },
					{ 'name': 'paid', 'type': 'boolean', },
					{ 'name': 'date', 'required': True }
				]
		try:
			# Get if ID or create
			pk = pkobject(request.POST)
			item, created = FactureSupplier.objects.filter(agency = request.user.agency, pk=pk).get_or_create() if pk else (FactureSupplier(), True)
			if editobject(request.POST, item, created):
				if created:
					item.submitted_by = request.user
					item.agency = request.user.agency
				# Set fields and save
				if setobject(request.POST, item, fields):
					item.save()

		except Exception as e:
			return JsonException(e)

	results = []
	if request.user.is_admin:
		factures = FactureSupplier.objects.filter(agency=request.user.agency).order_by('-date')[:1000]
	else:
		factures = FactureSupplier.objects.filter(submitted_by=request.user).order_by('-date')[:1000]
	for item in factures:
		results.append({ 'id': int(item.id), 'date' : item.date, 'supplier' : item.supplier.name, 'supplier_id' : item.supplier.id, 'file' : item.facture.filename if item.facture else None, 'invoice_number' : item.invoice_number, 'description' : item.description, 'amount' : item.amount, 'vat' : 'true' if item.vat else 'false', 'paid' : 'true' if item.paid else 'false' })
	return JsonResponse(results, safe=False)

def json_banks(request):
	if request.method == 'POST':
		data = request.POST.copy().dict()
		fields = [
					{ 'name': 'agent', 'key' : 'agent_id', 'foreignkey': True, 'default': request.user.id },
					{ 'name': 'bank_name', 'required': True }, 
					{ 'name': 'bank_address', 'required': True }, 
					{ 'name': 'account_name', 'required': True }, 
					{ 'name': 'iban', 'required': True }, 
					{ 'name': 'bic', }, 
					{ 'name': 'opened_date', },
					{ 'name': 'closed_date', },
					{ 'name': 'balance', 'type' : 'decimal',},
				]
		pk = pkobject(request.POST)
		try:
			if 'agent_id' in request.POST:
				user = Agent.objects.get(pk=request.POST.get('agent_id'))
			else:
				user = request.user
		except Exception as e:
			return JsonReport(e, "Unable to get Agent")
		try:
			# Get if ID or create
			item, created = BankAccount.objects.filter(agent = user, pk=pk).get_or_create() if pk else (BankAccount(), True)
		except Exception as e:
			return JsonReport(e, "Unable to get/create BankAccount")
		if editobject(data, item, created):
			if data['for'] != 'agent':
				item.agency = user.agency
			else:
				item.agency = None
			# Set fields and save
			if setobject(data, item, fields):
				try:
					if data['for'] != 'agent':
						BankAccount.objects.filter(agent=user, agency=user.agency).update(current=False)
					else:
						BankAccount.objects.filter(agent=user, agency=None).update(current=False)
				except Exception as e:
					return JsonReport(e, "Unable to update BankAccount.current to False")
				item.current = True
				try:
					item.save()
				except Exception as e:
					return JsonReport(e, "Unable to save BankAccount")

	results = []
	if request.user.is_admin:
		banks = BankAccount.objects.filter(agent__agency=request.user.agency).order_by('opened_date')[:1000]
	else:
		banks = BankAccount.objects.filter(agent=request.user).order_by('opened_date')[:1000]
	for bank in banks:
		results.append({ 'id': int(bank.id), 'agent_id' : bank.agent_id,'bank_name' : bank.bank_name, 'bank_address' : bank.bank_address, 'account_name' : bank.account_name, 'iban' : bank.iban, 'bic' : bank.bic, 'opened_date' : bank.opened_date, 'close_date' : bank.closed_date, 'balance' : bank.balance, 'current' : bank.current, 'for' : 'agence' if bank.agency else 'agent' })
	return JsonResponse(results, safe=False)

def json_bankentries(request):
	if request.method == 'POST':
		data = request.POST.copy().dict()
		fields = [
					{ 'name': 'bank_account', 'key' : 'bank_account_id', 'foreignkey' : True, 'required' : True }, 
					{ 'name': 'date', 'required': True }, 
					{ 'name': 'amount', 'type' : 'decimal', 'required': True }, 
					{ 'name': 'reference', }, 
					{ 'name': 'comment', }, 
				]
		# Get if ID or create
		pk = pkobject(request.POST)
		try:
			item, created = BankEntry.objects.filter(pk=pk).get_or_create() if pk else (BankEntry(), True)
		except Exception as e:
			return JsonReport(e, 'Unable to get/create BankEntry')
		if editobject(data, item, created):
			# Set fields and save
			if setobject(data, item, fields):
				try:
					item.save()
				except Exception as e:
					return JsonReport(e, 'Unable to save BankEntry')
			else:
				return JsonResponse({ 'name' : "Remplir tout les champs s'il vous plait", 'failed' : True })

	results = []
	entries = BankEntry.objects.filter(bank_account__agent=request.user).order_by('-date')[:5000]
	for entry in entries:
		results.append({ 'id': int(entry.id), 'bank_account' :str(entry.bank_account), 'bank_account_id' : entry.bank_account.id, 'date' : entry.date, 'amount' : entry.amount, 'reference' : entry.reference, 'comment' : entry.comment,  })
	return JsonResponse(results, safe=False)

def get_csv_index(row):
	search = { 'date de comptabilisation' : 'date', 'libellé' : 'comment', 'référence' : 'reference', 'montant' : 'amount' }
	result = {}
	index = 0
	for field in row:
		field = field.decode('utf-8')
		#field = field.decode('iso8859-1')
		if field.lower() in search.keys():
			result[search[field.lower()]] = index
		index = index + 1
	return result

def json_bankupload(request):
	if request.method == 'POST':
		success = []
		failure = []
		results = {}
		for filename,uploadedfile in request.FILES.items():
			try:
				bank = BankAccount.objects.get(pk=request.POST.get('bank_account_id'))
			except Exception as e:
				failure.append("Unable to identify which bank account")
				break
			if bank.agency != request.user.agency:
				failure.append("Sorry but you cannot access this bank account")
				break

			if uploadedfile.content_type != 'text/plain' and uploadedfile.content_type != 'text/csv':
				failure.append('Wrong filetype for file: '+uploadedfile.name)
			else:
				data = csv.reader(uploadedfile, delimiter=str(u';').encode('iso8859-1'))
				lines = 0
				added = 0
				duplicate = 0
				fields = {}
				for row in data:
					if lines == 0:
						index = get_csv_index(row)
						if len(index) != 4:
							failure.append('Wrong file format for file: '+uploadedfile.name)
							break
						# check header
					else:
						if BankEntry.objects.filter(reference = row[index['reference']], amount = row[index['amount']]).exists():
							duplicate = duplicate + 1
						else:
							try:
								newentry = BankEntry( bank_account = bank, amount = row[index['amount']], date = parse(row[index['date']]), reference = row[index['reference']], comment = row[index['comment']])
								newentry.save()
								added = added + 1
							except Exception as e:
								failure.append('Unable to add line '+str(lines)+' - '+str(e.message)+' ('+str(type(e))+'): '+str(row))

					lines = lines + 1
				success.append("File '"+uploadedfile.name+"' processed: "+str(added)+" new entries, ignored "+str(duplicate)+" existing")
		if len(success) > 0:
			results['success'] = "<br/>\n".join(success)
		if len(failure) > 0:
			results['error'] = "<br/>\n".join(failure)
	return JsonResponse(results, safe=False)

def json_notaire_factures(request):
	if request.method == 'POST':
		data = request.POST.copy().dict()
		fields = [
					{ 'name': 'date', 'required': True }, 
					{ 'name': 'invoice_number' }, 
					{ 'name': 'client_name', 'required': True }, 
					{ 'name': 'client_address' }, 
					{ 'name': 'other_agency' }, 
					{ 'name': 'property_address', },
					{ 'name': 'commission', 'required': True },
					{ 'name': 'paid', 'type' : 'boolean', 'default' : False },
					{ 'name': 'agent', 'key' : 'agent_id', 'foreignkey': True, 'default': request.user.id },
					{ 'name': 'updatebank', 'type' : 'boolean', 'default' : False },
					{ 'name': 'notaire' }, 
				]
		# Get if ID or create
		pk = pkobject(request.POST)
		try:
			if 'agent_id' in request.POST:
				agent = Agent.objects.get(pk=request.POST.get('agent_id'))
			else:
				agent = request.user
		except Exception as e:
			return JsonReport(e, "Unable to get Agent")

		try:
			item, created = FactureNotaire.objects.filter(agent__agency = request.user.agency, pk=pk).get_or_create() if pk else (FactureNotaire(), True)
		except Exception as e:
			return JsonReport(e, 'Unable to get/create FactureNotaire')

		if editobject(data, item, created):
			# Set fields and save
			if item.bank_account_id == None or 'updatebank' in data:
				try:
					item.bank_account = BankAccount.objects.get(agency=request.user.agency, current=True)
				except Exception as e:
					return JsonReport(e, 'Unable to get current agency bank account')
			if setobject(data, item, fields):
				try:
					if not item.invoice_number:
						item.invoice_number = get_next_invoice_number(FactureNotaire.objects.filter(agent__agency = agent.agency).latest('invoice_number').invoice_number)
				except Exception as e:
					return JsonReport(e, "Trying to get next invoice number")
				try:
					item.save()
				except Exception as e:
					return JsonReport(e, 'Unable to save FactureNotaire')
			else:
				return JsonResponse({ 'name' : "Failed to setobject as missing fields", 'failed' : True })

	results = []
	if request.user.is_admin:
		facturenotaires = FactureNotaire.objects.filter(agent__agency=request.user.agency).order_by('-date')[:1000]
	else:
		facturenotaires = FactureNotaire.objects.filter(agent=request.user).order_by('-date')[:1000]
	for facture in facturenotaires:
		results.append({ 'id': int(facture.id), 'date' : facture.date, 'agent_id' : facture.agent_id, 'agent' : str(facture.agent), 'description': facture.description(), 'bank_account_id' : facture.bank_account_id, 'invoice_number' : facture.invoice_number, 'client_name' : facture.client_name, 'client_address' : facture.client_address, 'other_agency' : facture.other_agency, 'property_address' : facture.property_address, 'commission' : facture.commission, 'notaire' : facture.notaire, 'paid' : 'true' if facture.paid else 'false' })
	return JsonResponse(results, safe=False)

def get_next_invoice_number(current):
	if not current or current == '':
		return "1"
	current = str(current)
	pattern = re.compile(r'\d+')
	number = pattern.findall(str(current))[-1]
	newnum = current.replace(number,str(int(number)+1))
	return newnum

def json_agent_factures(request):
	if request.method == 'POST':
		fields = [
					{ 'name': 'agent', 'key' : 'agent_id', 'foreignkey': True, 'default': request.user.id },
					{ 'name': 'sale', 'required': True, 'key' : 'sale_id', 'foreignkey' : True, }, 
					{ 'name': 'invoice_number' },
					{ 'name': 'commission', 'type' : 'number', },
					{ 'name': 'commission_percent', 'type' : 'number', },
					{ 'name': 'vat', 'type': 'boolean', },
					{ 'name': 'paid', 'type': 'boolean', },
					{ 'name': 'date', 'required': True }
				]
			# Get if ID or create
		pk = pkobject(request.POST)
		try:
			if 'agent_id' in request.POST:
				agent = Agent.objects.get(pk=request.POST.get('agent_id'))
			else:
				agent = request.user
		except Exception as e:
			return JsonReport(e, "Unable to get Agent")

		try:
			item, created = FactureAgent.objects.filter(agent__agency = request.user.agency, pk=pk).get_or_create() if pk else (FactureAgent(), True)
		except Exception as e:
			return JsonReport(e, "Trying to get or create FactureAgent")
		if editobject(request.POST, item, created):
			# Set fields and save
			try:
				item.bank_account = BankAccount.objects.get(agent=agent, agency=None, current=True)
			except Exception as e:
				return JsonResponse({ 'name' : "Need to set primary bank account for "+str(agent), 'failed' : True })
			if setobject(request.POST, item, fields):
				try:
					if not item.invoice_number:
						item.invoice_number = get_next_invoice_number(FactureAgent.objects.filter(agent = agent).latest('invoice_number').invoice_number)
				except Exception as e:
					return JsonReport(e, "Trying to get next invoice number")
				try:
					item.save()
				except Exception as e:
					return JsonReport(e, "Trying to save FactureAgent")

			else:
				return JsonResponse({ 'name' : "Unable to save, something missing", 'failed' : True })

	results = []
	if request.user.is_admin:
		factures = FactureAgent.objects.filter(agent__agency=request.user.agency).order_by('-date')[:1000]
	else:
		factures = FactureAgent.objects.filter(agent=request.user).order_by('-date')[:1000]
	for item in factures:
		results.append({ 'id': int(item.id), 'date' : item.date, 'sale' : str(item.sale), 'sale_id' : item.sale.id, 'file' : item.facture.filename if item.facture else None, 'invoice_number' : item.invoice_number, 'commission' : item.commission, 'commission_percent' : item.commission_percent, 'agent' : str(item.agent), 'agent_id' : item.agent_id, 'vat' : 'true' if item.vat else 'false', 'paid' : 'true' if item.paid else 'false' })
	return JsonResponse(results, safe=False)

def json_apporteur_factures(request):
	if request.method == 'POST':
		fields = [
					{ 'name': 'agent', 'key' : 'agent_id', 'foreignkey': True, 'default': request.user.id },
					{ 'name': 'sale', 'required': True, 'key' : 'sale_id', 'foreignkey' : True, }, 
					{ 'name': 'invoice_number' },
					{ 'name': 'commission', 'type' : 'number', },
					{ 'name': 'vat', 'type': 'boolean', },
					{ 'name': 'paid', 'type': 'boolean', },
					{ 'name': 'date', 'required': True },
					{ 'name': 'name', 'required': True },
					{ 'name': 'address', 'required': True },
					{ 'name': 'iban', 'required': True },
					{ 'name': 'bic' },
					{ 'name': 'siret' }
				]
			# Get if ID or create
		pk = pkobject(request.POST)
		try:
			if 'agent_id' in request.POST:
				agent = Agent.objects.get(pk=request.POST.get('agent_id'))
			else:
				agent = request.user
		except Exception as e:
			return JsonReport(e, "Unable to get Agent")

		try:
			item, created = FactureApporteur.objects.filter(agent__agency = request.user.agency, pk=pk).get_or_create() if pk else (FactureApporteur(), True)
		except Exception as e:
			return JsonReport(e,"Trying to get or create FactureAgent")
		if editobject(request.POST, item, created):
			# Set fields and save
			item.agent = agent
			if setobject(request.POST, item, fields):
				try:
					if not item.invoice_number:
						item.invoice_number = get_next_invoice_number(FactureApporteur.objects.filter(agent = agent).latest('invoice_number').invoice_number)
				except Exception as e:
					return JsonReport(e, "Trying to get next invoice number")
				try:
					item.save()
				except Exception as e:
					return JsonReport(e,"Trying to get or create FactureApporteur")

			else:
				return JsonResponse({ 'name' : "Unable to save, something missing", 'failed' : True })

	results = []
	if request.user.is_admin:
		factures = FactureApporteur.objects.filter(agent__agency=request.user.agency).order_by('-date')[:1000]
	else:
		factures = FactureApporteur.objects.filter(agent=request.user).order_by('-date')[:1000]
	for item in factures:
		results.append({ 'id': int(item.id), 'date' : item.date, 'sale' : str(item.sale), 'sale_id' : item.sale.id, 'file' : item.facture.filename if item.facture else None, 'invoice_number' : item.invoice_number, 'commission' : item.commission, 'name' : item.name, 'address' : item.address, 'iban' : item.iban, 'bic' : item.bic, 'siret' : item.siret, 'agent' : str(item.agent), 'agent_id' : item.agent_id, 'vat' : 'true' if item.vat else 'false', 'paid' : 'true' if item.paid else 'false' })
	return JsonResponse(results, safe=False)

