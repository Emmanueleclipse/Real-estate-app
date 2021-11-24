# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render
from django.db.models import Q,Count
from django.http import HttpResponse, JsonResponse
from django.views.generic import View,TemplateView
from agency.utils import JsonException, JsonError, setobject
from chat.models import UnreadChat,Chat,GroupChat
from agents.models import Agent
from news.models import News

class ChatView(TemplateView):
    template_name = "chat.html"

class GroupChatView(TemplateView):
    template_name = "groupchat.html"

#def json_lastchat(request):
#	results_last = LastChat.objects.filter(to_agent=request.user).order_by('-when')
#	last = {}
#	for result in results_last:
#		last[result.from_agent] = { 'last' : result.when, 'agent_id' : result.from_agent, 'agent' : result.from_agent.name, 'thumbnail' : result.from_agent.thumbnail }

#	return JsonResponse(last, safe=False)

#	SELECT COUNT(*) as numnew, chat.from_agent FROM chat LEFT JOIN lastchat ON lastchat.from_agent = chat.from_agent WHERE chat.when > lastchat.when GROUP BY from_agent
#	results_messages = Chat.objects.filter(to_agent=request.user).filter()

def json_unreadchat(request):
	if request.method == 'POST':
		agent = request.POST.get('agent_id', None)
		if agent.isnumeric():
			UnreadChat.objects.filter(from_agent=agent).delete()
	messages = UnreadChat.objects.filter(to_agent=request.user).order_by('-when')
	unread = {}
	total = 0
	last = None
	for message in messages:
		if message.from_agent_id in unread:
			unread[message.from_agent.id]['total']=unread[message.from_agent.id]['total']+1
		else:
			unread[message.from_agent.id] = { 'total' : 1, 'last' : message.when, 'agent' : message.from_agent.get_full_name(), 'agent_id' : message.from_agent.id, 'thumbnail' : message.from_agent.thumbnail() }
			last = message.when if not last else last
		total=total+1
	results = unread.values()
	results.insert(0,{ 'total': total, 'agent': "Total", 'last': last, 'agent_id' : None })
	return JsonResponse(results, safe=False)

def json_listchat(request):
	users = {}
	# get list of users in chat messages, ordered by latest chat
	chats = Chat.objects.all().filter(Q(from_agent=request.user) | Q(to_agent=request.user)).order_by('when')
	for chat in chats:
		displayuser = chat.to_agent if chat.from_agent==request.user else chat.from_agent
		users[displayuser.id] = { 'agent_id' : displayuser.id, 'agent' : displayuser.get_full_name(), 'thumbnail' : unicode(displayuser.thumbnail()), 'when' : chat.when, 'unread' : None, 'extract' : chat.message[:90] }
	# get unread message totals and add them
	totals = UnreadChat.objects.values('from_agent').filter(to_agent=request.user).annotate(number=Count('to_agent'))
	for total in totals:
		users[total['from_agent']]['unread'] = total['number']
	return JsonResponse(users.values(), safe=False)


def json_chat(request):
	if request.method == 'POST':
		fields = [
			{ 'name': 'to_agent_id', 'required': True }, 
			{ 'name': 'message', 'required': True },
		]
		unreadfields = [
			{ 'name': 'to_agent_id', 'required': True }, 
		]
		newsfields = [
			{ 'name': 'description', 'required': True, 'key' : 'message' },
			{ 'name': 'agent_id', 'required': True, 'key' : 'to_agent_id' }, 
		]
		try:
			chat = Chat()
			chat.from_agent = request.user
			if setobject(request.POST, chat, fields):
				chat.save()
			else:
				return JsonError('Unable to extract parameters')
			unreadchat = UnreadChat()
			unreadchat.from_agent = request.user
			if setobject(request.POST, unreadchat, unreadfields):
				unreadchat.save()
			news = News()
			if setobject(request.POST, news, newsfields):
				news.title = u'Message privé reçu de '+ request.user.get_full_name()
				news.photo = request.user.thumbnail()
				news.icon = 'chat'
				news.url = '/chat?agent='+str(request.user.id)
				news.save()
		except Exception as e:
			return JsonException(e)

	results = []
	messages = Chat.objects.filter(Q(from_agent=request.user) | Q(to_agent=request.user)).order_by('-when')
	for message in messages:
		thread = message.to_agent.id if message.from_agent==request.user else message.from_agent.id
		results.append({ 'id': int(message.id), 'mine': bool(message.from_agent==request.user), 'message' : message.message, 'when' : message.when, 'thread' : thread, 'agent' : message.from_agent.get_full_name(), 'recipient' : message.to_agent.get_full_name(), 'thumbnail' : message.from_agent.thumbnail(), })
	return JsonResponse(results, safe=False)

def json_groupchat(request):
	if request.method == 'POST':
		fields = [
					{ 'name': 'message', 'required': True },
				]
		newsfields = [
					{ 'name': 'description', 'required': True, 'key' : 'message' },
				]
		try:
			chat = GroupChat()
			chat.from_agent = request.user
			chat.agency = request.user.agency
			if setobject(request.POST, chat, fields):
				chat.save()
			news = News()
			if setobject(request.POST, news, newsfields):
				news.title = u'Message groupé reçu de '+ request.user.get_full_name()
				news.photo = request.user.thumbnail()
				news.icon = 'chat'
				news.url = '/groupchat/'
				agents = Agent.objects.filter(agency=request.user.agency)
				for agent in agents:
					news.pk = None
					news.agent = agent
					news.save()
		except Exception as e:
			return JsonException(e)

	results = []
	messages = GroupChat.objects.filter(agency=request.user.agency).order_by('-when')
	for message in messages:
		results.append({ 'id': int(message.id), 'mine': bool(message.from_agent==request.user), 'message' : message.message, 'when' : message.when, 'agent' : message.from_agent.get_full_name(), 'thumbnail' : message.from_agent.thumbnail(), })
	return JsonResponse(results, safe=False)
