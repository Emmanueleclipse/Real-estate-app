# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-08 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0011_auto_20160806_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientsearch',
            name='trash',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]