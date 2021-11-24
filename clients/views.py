# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView
from django.db.models import Q
from django.utils.http import urlencode
from urllib import quote_plus
from agency.utils import JsonException, pkobject, editobject, setobject, atleast
from clients.models import Client,Contact,ContactPhone,ContactEmail,ClientSearch,ClientSale,ClientActivity,ClientLead
from agents.models import Agent

def urlmsg(text):
    text = text.encode("utf-8")
    return quote_plus(text)

class ClientsView(TemplateView):
    template_name = "clients.html"

class ClientView(TemplateView):
    template_name = 'client.html'

class BuyersView(TemplateView):
    template_name = "buyers.html"

class SellersView(TemplateView):
    template_name = "sellers.html"

class ClientLeadsView(TemplateView):
    template_name = 'clientleads.html'


def json_buyers(request):
    if request.method == 'POST':
        fields = [
                    { 'name': 'client_id', 'required': True }, 
                    { 'name': 'description', },
                    { 'name': 'budget', },
                    { 'name': 'tags', },
                    { 'name': 'what', 'default': 'appartement' }, 
                ]

        try:
            if request.POST.get('togglelock'):
                item = Client.objects.get(pk=request.POST.get('togglelock'))
                item.hot = not item.hot
                item.save()
            else:
                # Get if ID or create
                pk = pkobject(request.POST)
                item, created = ClientSearch.objects.filter(Q(client__agent=request.user),Q(pk=pk)).get_or_create() if pk else (ClientSearch(), False)
                if editobject(request.POST, item, created):
                    # Extra modifications to the object here
                    # Set fields and save
                    if setobject(request.POST, item, fields):
                        item.save()
        except Exception as e:
            return JsonException(e)

    searches = ClientSearch.objects.filter(client__agent=request.user).exclude(trash__isnull=False).exclude(client__trash__isnull=False).order_by('-client__hot','-client__last_contact')
    array_searches = []
    for item in searches:
        search = item.client.search+','+item.tags if item.tags else item.client.search
        array_searches.append({'id': item.id, 'search': search, 'description': item.description, 'hot' : item.client.hot, 'what' : item.what, 'budget': item.budget, 'tags': item.tags, 'client_id' : item.client_id, 'who' : item.client.name, 'date_created' : item.date_created, 'last_contact' : item.client.last_contact })
    return JsonResponse(array_searches, safe=False)

def json_sellers(request):
    if request.method == 'POST':
        fields = [
                    { 'name': 'client_id', 'required': True }, 
                    { 'name': 'description', },
                    { 'name': 'address', },
                    { 'name': 'price', },
                    { 'name': 'tags', },
                    { 'name': 'what', 'default': 'appartement' }, 
                ]
        try:
            if request.POST.get('togglelock'):
                item = Client.objects.get(pk=request.POST.get('togglelock'))
                item.hot = not item.hot
                item.save()
            else:
                # Get if ID or create
                pk = pkobject(request.POST)
                item, created = ClientSale.objects.filter(Q(client__agent=request.user),Q(pk=pk)).get_or_create() if pk else (ClientSale(), False)
                if editobject(request.POST, item, created):
                    # Extra modifications to the object here

                    # Set fields and save
                    if setobject(request.POST, item, fields):
                        item.save()
        except Exception as e:
            return JsonException(e)
    sales = ClientSale.objects.filter(client__agent=request.user).exclude(trash__isnull=False).order_by('-client__hot','client__last_contact')
    array_sales = []
    for item in sales:
        search = item.client.search+','+item.tags if item.tags else item.client.search
        array_sales.append({'id': item.id, 'search': search, 'description': item.description, 'hot' : item.client.hot, 'what' : item.what, 'address': item.address, 'price': item.price, 'tags': item.tags, 'client_id' : item.client_id, 'who' : item.client.name, 'lastcontact' : item.client.last_contact })
    return JsonResponse(array_sales, safe=False)

def json_clients(request):
    if request.method == 'POST':
        fields = [
                    { 'name': 'agent_id', 'required': True }, 
                    { 'name': 'last_contact', },
                    { 'name': 'next_contact', },
                ]
        try:
            # Get if ID or create
            pk = pkobject(request.POST)
            item, created = Client.objects.filter(Q(agent=request.user),Q(pk=pk)).get_or_create() if pk else (Client(), False)
            if editobject(request.POST, item, created):
                # Extra modifications to the object here

                # Set fields and save
                if setobject(request.POST, item, fields):
                    item.save()
        except Exception as e:
            return JsonException(e)
    clients = Client.objects.filter(agent=request.user)
    array_clients = []
    for item in clients:
#        search = item.client.search+','+item.tags if item.tags else item.client.search
        array_clients.append({'id': item.id, 'name' : item.name, 'last_contact': item.last_contact, 'next_contact': item.next_contact, 'agent_id' : item.agent_id, 'search' : item.search, 'trash' : item.trash })
    return JsonResponse(array_clients, safe=False)

def json_contacts_client(request):

    if request.method == 'POST':
        submission = request.POST.dict()
        pk = submission['contact_id'] if 'contact_id' in submission else pkobject(submission)

        fields = [
                   { 'name': 'client_id', 'required': True, }, 
                   { 'name': 'forename', }, { 'name': 'surname', }, { 'name': 'status', 'type': 'integer' }, { 'name': 'language', }, { 'name': 'relationship', 'type': 'integer' }, { 'name': 'notes', },
                ]
        fields_telephone = [ { 'name': 'contact_id', 'required': True }, { 'name': 'id', 'key' : 'telephone__id' }, { 'name': 'number', 'key' : 'telephone__number', 'required' : True }, { 'name': 'type', 'key': 'telephone__type'}, ]
        fields_email = [ { 'name': 'contact_id', 'required': True }, { 'name': 'id', 'key' : 'email__id' }, { 'name' : 'email', 'key': 'email__email', 'required' : True }, { 'name': 'type', 'key': 'email__type' }, { 'name': 'email__reply_to', 'type': 'boolean'} ]


        try:
            if 'subobject' in submission:
                if submission['subobject'] == 'telephone' and 'telephone__id' in submission:
                    editobject(submission, ContactPhone.objects.get(pk=submission['telephone__id'],contact_id=pk),False)
            else:
                contact, created = Contact.objects.filter(Q(client__agent=request.user),Q(pk=pk)).get_or_create() if pk else (Contact(), True)
                submission['contact_id'] = contact.id
                if editobject(submission, contact, created):
                    if contact.client_id is None:
                        if 'client_id' in submission:
                            client = Client.objects.get(pk=int(submission['client_id']),agent=request.user)
                        else:
                            client = Client()
                            client.agent = request.user
                            client.save()
                        contact.client = client
                        submission['client_id'] = client.id
                    if 'forename' in submission or 'surname' in submission:
                        if setobject(submission, contact, fields):
                            contact.save()
                            submission['contact_id'] = contact.id

                    if 'telephone__number' in submission:
                        if 'telephone__id' in submission:
                            number= ContactPhone.objects.get(pk=int(submission['telephone__id']),contact_id=submission['contact_id'])
                        else:
                            number = ContactPhone(contact_id=submission['contact_id'])
                        if setobject(submission, number, fields_telephone):
                            number.save()
                    if 'email__email' in submission:
                        if 'email__id' in submission:
                            email = ContactEmail.objects.get(pk=int(submission['email__id']),contact_id=submission['contact_id'])
                        else:
                            email = ContactEmail(contact_id=submission['contact_id'])
                        if setobject(submission, email, fields_email):
                            email.save()

        except Exception as e:
            return JsonException(e)

    clients = Client.objects.filter(agent=request.user)
    array_clients = []
    for client in clients:
        array_clients.append(int(client.id))
    contacts = Contact.objects.filter(client__in=array_clients).order_by('surname')
    i = 0
    array_contacts = []
    array_contact_ids = {}
    for contact in contacts:
        array_contacts.append( { 'id': contact.id, 'title' : contact.get_status_display(), 'forename' : contact.forename, 'surname' : contact.surname, 'relation' : contact.get_relationship_display(), 'status' : contact.status, 'language' : contact.language, 'relationship' : contact.relationship, 'notes' : contact.notes, 'search': contact.search, 'client_id' : int(contact.client_id),'trash' : contact.client.trash, 'telephone' : [], 'email' : [] } )
        array_contact_ids[int(contact.id)] = i
        i = i+ 1
    numbers = ContactPhone.objects.filter(contact__in=array_contact_ids.keys())
    for number in numbers:
        array_contacts[array_contact_ids[number.contact_id]]['telephone'].append({ 'number' : number.number, 'type' : number.type, 'id' : number.id })
    emails = ContactEmail.objects.filter(contact__in=array_contact_ids.keys())
    for email in emails:
        array_contacts[array_contact_ids[email.contact_id]]['email'].append({ 'email' : email.email, 'type' : email.type, 'id': email.id })
    return JsonResponse(array_contacts, safe=False)

def json_recent_activities(request):
    if request.method == 'POST':
        fields = [
                    { 'name': 'client_id', 'required': True }, 
                    { 'name': 'description', 'required': True }, 
                    { 'name': 'type', 'default': 'note' }, 
                ]
        try:
            activity = ClientActivity()
            if setobject(request.POST, activity, fields):
                activity.save()
        except Exception as e:
            return JsonException(e)
    results = []
    activities = ClientActivity.objects.filter(client__agent=request.user).filter(date_created__gte=datetime.now()-timedelta(days=30)).order_by('-date_created')
    for activity in activities:
        results.append({ 'client' : str(activity.client), 'client_id' : str(activity.client_id), 'datecreated' : activity.date_created, 'type' : activity.type, 'description' : activity.description })
    return JsonResponse(results, safe=False)

def save_clientlead(request):
    fields = [
                    { 'name': 'name', 'required' : True },
                    { 'name': 'phone',},
                    { 'name': 'email',},
                    { 'name': 'buying',},
                    { 'name': 'selling',},
                    { 'name': 'what',},
                    { 'name': 'agent',},
                    { 'name': 'price', 'type' : 'number',},
                    { 'name': 'notes',},
                    { 'name': 'language', 'default' : 'fr', }, 
                    { 'name': 'source', 'default' : 'BienFacile'}, 
                    { 'name': 'source_url', }, 
                    { 'name': 'what', 'default': 'appartement' }, 
            ]
    try:
        if request.method == 'POST':
            submission = request.POST.copy().dict()
        else:
            submission = request.GET.copy().dict()
        if not atleast(submission, ['email', 'phone']):
            return { 'name' : "Merci de remplir un email ou numero telephone", 'trans' : 'missingemailphone', 'failed' : True }
        if 'buysell' in submission:
            if 'notes' not in submission or submission['notes'] == '':
                submission['notes'] = 'Pas de message'
            if submission['buysell'] == 'sell':
                submission['selling'] = submission['notes']
            else:
                submission['buying'] = submission['notes']
            del submission['buysell']
            del submission['notes']
        if 'agent' in submission:
            try:
                assigned_agent = Agent.objects.get(email=submission['agent'])
                lead = ClientLead(assigned_agent=assigned_agent)
            except:
                return { 'name' : "Agent inconno pour email "+submission['agent'], 'trans' : 'unknownagent', 'failed' : True }
        elif hasattr(request, 'user'):
            lead = ClientLead(assigned_agent=request.user)
        else:
            return { 'name' : "Envoyer a qui?", 'trans' : 'missingagent', 'failed' : True }
        if setobject(submission, lead, fields):
            lead.save()
            return { 'name' : lead.name, 'client_id' : lead.client_id, 'failed' : False }
        else:
            return { 'name' : "Pas reussi, pas assez d'info", 'trans' : 'missing', 'failed' : True }
    except Exception as e:
        return {'name' : str(JsonException(e)), 'failed' : True }
    return False

def json_addclientlead(request):
    results = []
    if request.method == 'POST':
        results.append(save_clientlead(request))
    return JsonResponse(results, safe=False)

def json_clientleads(request):
    if request.method == 'POST':
        save_clientlead(request)
    results = []
    leads = ClientLead.objects.filter(assigned_agent__agency=request.user.agency).order_by('-date_created')
    for lead in leads:
        results.append({ 'name' : lead.name if lead.name else lead.email, 'phone' : lead.phone, 'email' : lead.email, 'buying' : lead.buying, 'selling' : lead.selling, 'what' : lead.what, 'price' : str(lead.price), 'notes' : lead.notes, 'agent' : lead.assigned_agent.get_full_name(), 'language' : lead.language, 'date_created' : lead.date_created, 'source' : lead.source, 'source_url' : lead.source_url, 'client_id' : lead.client_id })
    return JsonResponse(results, safe=False)

def csv_clientleads(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bienfacile_contacts.csv"'

    results = ['EMAIL;LASTNAME;FIRSTNAME;SMS']
    leads = ClientLead.objects.filter(assigned_agent=request.user, language='en')
    for lead in leads:
        if lead.name:
            forename = surname = ''
            elements = lead.name.strip('. ').split()
            if len(elements) > 0:
                forename = elements.pop(0)
                if forename.lower() in ['mr', 'mr.', 'm', 'm.', 'mrs', 'miss', 'dr.', 'ms', 'dr', 'nr', 'monsieur', 'madame']:
                    forename = elements.pop(0)
            if len(elements) > 0:
                surname = ' '.join(elements)
        phone = lead.phone if lead.phone else ''
        if lead.email:
            results.append(lead.email+';'+surname+';'+forename+';'+phone)
    response.write("\n".join(results))
    return response

def contactform(request):
    if request.method == 'GET':
        if 'source' in request.GET:
            results = save_clientlead(request)
            return JsonResponse(results, safe=False)
    elif request.method == 'POST':
        return HttpResponse("POST method not supported")
    context = {}
    response = render(request, 'contactform.js', context)
    response['Content-Type'] = 'application/javascript; charset=utf-8'
    response['Cache-Control'] = 'no-cache'
    return response
