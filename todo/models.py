# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from news.models import News
from agents.models import Agent
#from clients.models import Client
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta

class ToDo(models.Model):
	title = models.CharField(max_length=140)
	description = models.TextField(blank=True, null=True)
	tags = models.CharField(max_length=255,null=True,blank=True)
	created_date = models.DateField(auto_now=True)
	start_date = models.DateField(blank=True, null=True, )
	due_date = models.DateField(blank=True, null=True, )
	completed_date = models.DateField(blank=True, null=True)
	created_by = models.ForeignKey(Agent, related_name='todo_created_by',blank=True, null=True, db_index=True)
	assigned_to = models.ForeignKey(Agent, related_name='todo_assigned_to',blank=True, null=True, db_index=True)

	for_client = models.ForeignKey('clients.Client', related_name='todo_for_client',blank=True, null=True)
	for_agent = models.ForeignKey(Agent, related_name='todo_for_agent',blank=True, null=True)

	class Meta:
		ordering = ["due_date"]

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.assigned_to:
			self.assigned_to = self.created_by
		super(ToDo, self).save(*args, **kwargs)

@receiver(post_save, sender=ToDo)
def post_save_todo(sender, instance, created, **kwargs):
	news = News()
	news.description = instance.description
	news.url = "javascript:todo.modal('#modal', { title : 'Modifier tache', hidden: { id: "+str(instance.id)+" } });"
	title = instance.title
	if created:
		news.icon = 'lightbulb-o'
		title = 'Nouveau tache: '+title
	elif instance.completed_date:
		title = '<strike>'+ title + '</strike>'
		news.icon = 'check'
	else:
		if datetime.today().date() == instance.created_date and instance.created_by == instance.assigned_to: # don't log modifications of own tasks if task created today
			return
		title = 'Modification: '+ title
		news.icon = 'refresh'
	if instance.created_by != instance.assigned_to:
		news.agent = instance.created_by
		news.title = title + ' ('+ instance.assigned_to.get_full_name() +')'
		news.save()
		news.pk = None
		news.agent = instance.assigned_to
		news.title = title + ' ('+ instance.created_by.get_full_name() +')'
		news.save()
	else:
		news.title = title
		news.agent = instance.created_by
		news.save()
