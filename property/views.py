# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from django.views.generic import View,TemplateView
from agency.utils import JsonException, JsonReport, pkobject, editobject, setobject
from agents.models import Agent

class MandatsView(TemplateView):
    template_name = "mandats.html"

def json_mandats(request):
	if request.method == 'POST':
		fields = [
					{ 'name': 'agent', 'key' : 'agent_id', 'foreignkey': True, 'default': request.user.id },
					{ 'name': 'agency', 'key' : 'agency_id', 'foreignkey': True },
					{ 'name': 'name', 'required': True }, 
					{ 'name': 'description', },
					{ 'name': 'siret', },
					{ 'name': 'vat_number', },
					{ 'name': 'category', },
					{ 'name': 'tags', },
				]
		# Get if ID or create
		pk = pkobject(request.POST)
		try:
			item, created = Mandat.objects.filter(agency = request.user.agency, pk=pk).get_or_create() if pk else (Mandat(), True)
		except Exception as e:
			return JsonReport(e, "Unable to get/create Mandat")
		if editobject(request.POST, item, created):
			if agent:
				item.agent = request.user
			# Set fields and save
			if setobject(request.POST, item, fields):
				try:
					item.save()
				except Exception as e:
					return JsonReport(e, "Unable to save Mandat")
			else:
				return JsonResponse({ 'name' : "Remplir tout les champs s'il vous plait", 'failed' : True })


	results = []
	mandats = Mandat.objects.filter(agency=request.user.agency).order_by('name')[:1000]
	for item in mandats:
		results.append({ 'id': int(item.id), 'name' : supplier.name, 'description' : supplier.description, 'tags' : supplier.tags, 'siret' : supplier.siret, 'vat_number' : supplier.vat_number, 'category' : supplier.category })
	return JsonResponse(results, safe=False)

