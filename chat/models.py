from __future__ import unicode_literals

from django.db import models
from agents.models import Agent,Agency

class Chat(models.Model):
	when = models.DateTimeField(auto_now=True)
	message = models.TextField()
	from_agent = models.ForeignKey(Agent, related_name='chat_from_agent', db_index=True)
	to_agent = models.ForeignKey(Agent, related_name='chat_to_agent', db_index=True)
	class Meta:
		ordering = ["-when"]

	def __unicode__(self):
		return self.message

class UnreadChat(models.Model):
	when = models.DateTimeField(auto_now=True)
	from_agent = models.ForeignKey(Agent, related_name='lastchat_from_agent', db_index=True)
	to_agent = models.ForeignKey(Agent, related_name='last_chat_to_agent', db_index=True)

class GroupChat(models.Model):
	when = models.DateTimeField(auto_now=True)
	message = models.TextField()
	from_agent = models.ForeignKey(Agent, related_name='groupchat_from_agent')
	agency = models.ForeignKey(Agency, related_name='groupchat_agency', db_index=True)

	class Meta:
		ordering = ["-when"]

	def __unicode__(self):
		return self.message

