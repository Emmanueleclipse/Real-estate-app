# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Upload(models.Model):
	filename = models.CharField(max_length=254)
	mimetype = models.CharField(max_length=254)
	size = models.IntegerField()
	date = models.DateTimeField()
	compressed = models.BooleanField(default=False)
	thumb = models.BooleanField(default=False)
