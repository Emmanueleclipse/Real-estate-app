# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic import View
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Q
from agents.models import Agency,Agent, AgentSettings
from agency.utils import JsonException, pkobject, editobject, setobject
import scraper.rabbitutil as queueutil

class HomePageView(TemplateView):
    template_name = "index.html"

class AnnoncesView(TemplateView):
    template_name = "annonces.html"

class PreferencesView(TemplateView):
    template_name = "preferences.html"

class HelpView(TemplateView):
    template_name = "help.html"

class AgencesView(TemplateView):
    template_name = "agences.html"

class AgenceView(TemplateView):
    template_name = "agence.html"

class AgentsView(TemplateView):
    template_name = "agents.html"

def json_agences(request):
    agencies = Agency.objects.all().order_by('name')
    data = []
    for agency in agencies:
        data.append({ 'name': agency.agencyname, 'branch': agency.branch, 'address': agency.address, 'city': agency.city, 'postcode': agency.postcode, 'telephone': agency.telephone, 'email': agency.email, 'web': agency.web, 'search': agency.search, 'id': agency.id })
    return JsonResponse(data, safe=False)

def json_agents(request):
    if request.method == 'POST' and request.user.is_admin:
        fields = [
                    { 'name': 'forename', 'required': True }, 
                    { 'name': 'surname', 'required': True },
                    { 'name': 'role', },
                    { 'name': 'mobile', },
                    { 'name': 'public', 'type': 'boolean' }, 
                ]
        try:
            # Get if ID or create
            pk = pkobject(request.POST)
            item, created = Agent.objects.filter(pk=pk).get_or_create() if pk else (Agent(), False)
            if editobject(request.POST, item, created):
                # Extra modifications to the object here

                # Set fields and save
                if setobject(request.POST, item, fields):
                    item.save()
        except Exception as e:
            return JsonException(e)
    agents = Agent.objects.all().order_by('surname') if request.user.is_admin else Agent.objects.filter(Q(public=True)|Q(agency=request.user.agency)).order_by('surname')
    data = []
    for agent in agents:
        time_ago = timezone.now() - timedelta(days=90)
        data.append({ 'id' : agent.id, 'public' : agent.public, 'forename': agent.forename, 'surname': agent.surname, 'agency': agent.agency.agencyname, 'branch': agent.agency.branch, 'mobile': agent.mobile, 'email': agent.email, 'search': agent.search, 'agency_id': agent.agency_id, 'isonline' : False if not agent.last_login or agent.last_login < time_ago else True })
    return JsonResponse(data, safe=False)

def json_monagence(request):
    agents = Agent.objects.filter(agency=request.user.agency).order_by('surname')
    data = []
    for agent in agents:
        thumbnail = agent.thumbnail() if agent.photo else None
        data.append({ 'forename': agent.forename, 'surname': agent.surname, 'agency': agent.agency.agencyname, 'branch': agent.agency.branch, 'mobile': agent.mobile, 'email': agent.email, 'thumbnail': thumbnail, 'search': agent.search, 'agency_id': agent.agency_id, 'id' : agent.id })
    return JsonResponse(data, safe=False)

def get_usersetting(agent):
    result = {}
    settings = AgentSettings.objects.filter(agent=agent)
    for setting in settings:
        result[setting.key] = setting.value
    return result

def set_usersetting(agent,settings):
    for key, value in settings.iteritems():
        setting, created = AgentSettings.objects.get_or_create(key=key,agent=agent)
        if not value or value == '':
            setting.delete()
        else:
            setting.value = value
            setting.save()

class UpdateAgenciesView(TemplateView):
    template_name = "updateagencies.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateAgenciesView, self).get_context_data(**kwargs)
        context['usersettings'] = get_usersetting(self.request.user)
        return context

    def agentline(self, details):
        result = details.forename+' '+details.surname+', '
        result += ('numero portable '+details.mobile if details.mobile else "besoin de son numero portable")
        result += ', '+('email '+details.email if details.email else ", besoin de son adresse email")
        return result + "\n"

    def post(self, request, *args, **kwargs):
        if request.POST.get('save', None):
            result = "Saved"
        else:
            agencies = Agency.objects.all().order_by('id')
            agentslist = Agent.objects.all().order_by('agency')
            agents = {}
            emails = []
            sendlist = []
            i=0
            result = ''
            for item in agentslist:
                if item.agency_id in agents:
                    agents[item.agency_id].append(item)
                else:
                    agents[item.agency_id] = [item, ]
            queue = queueutil.ScraperQueue()
            for item in agencies:
                agency = item.name+(' ('+item.branch+')' if item.branch else '')
                agency = (item.prefix+' ' if item.prefix else '')+item.name+(' '+item.postfix if item.postfix else '')

                email = item.email
                if email not in emails:
                    numagents = len(agents[item.id]) if item.id in agents else 0
                    result += '<br/>'+str(i)+') Agency: '+agency+' has '+(str(numagents) if numagents else 'no')+' agents'
                    subject = request.POST.get('subject', 'Email pour')+' '+agency
                    body = ''
                    if numagents == 0:
                        body = request.POST.get('none', '')
                    if numagents == 1:
                        body = request.POST.get('one', '')+"\n\n"
                        body += self.agentline(agents[item.id][0])
                    if numagents > 1 or numagents == 1 and body == '':
                        body = request.POST.get('multiple', '')+"\n\n"
                        for agentdetails in agents[item.id]:
                            body += self.agentline(agentdetails)
                    if body != '':
                        body += "\n\n"+request.POST.get('signature', '')
                        envelope = { 'to' : (agency+' <'+email+'>'), 'from': 'Phillip Temple <phillip@paradiseproperties.fr>', 'body' : body, 'subject' : subject }
                        result += '<hr/><table><tr><td>To: '+envelope['to']+'</td><td>From: '+envelope['from']+'</td><td>Subject: '+envelope['subject']+'</td></tr></table><br/><pre>'+envelope['body']+'</pre><hr/>'
                        if request.POST.get('send', ''):
                            queue_name = 'mails'
                            message = json.dumps(envelope)
                            queue.ensureopen(queue_name)
                            queue.send(queue_name,message)

                    emails.append(email)

                else:
                    result += '<br/>Ignoring duplicate email '+email

                i += 1
            set_usersetting( request.user, { 'updateagencies_lastupdate' : str(datetime.now()), } )

        set_usersetting( request.user, {  'updateagencies_none' : request.POST.get('none', None),
                            'updateagencies_one' : request.POST.get('one', None),
                            'updateagencies_multiple' : request.POST.get('multiple', None), 
                            'updateagencies_subject' : request.POST.get('subject', None),
                            'updateagencies_signature' : request.POST.get('signature', None),
                        } )
        return HttpResponse(result)
