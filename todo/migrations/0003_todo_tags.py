# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-07 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20170307_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='tags',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
