# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-24 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0017_auto_20170320_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
