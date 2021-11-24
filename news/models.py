# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from agents.models import Agent

class News(models.Model):
	title = models.CharField(max_length=140)
	description = models.TextField(blank=True, null=True)
	created_date = models.DateTimeField(default=timezone.now)
	agent = models.ForeignKey(Agent, related_name='news_for_agent')
	icon = models.CharField(max_length=64, null=True, blank=True)
	photo = models.CharField(max_length=255, null=True, blank=True)
	url = models.CharField(max_length=255)

	class Meta:
		ordering = ["-created_date"]

	def __unicode__(self):
		return self.title
