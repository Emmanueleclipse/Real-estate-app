# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-23 16:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0027_clientlead_what'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientlead',
            name='language',
            field=models.CharField(blank=True, choices=[(b'fr', b'Francais'), (b'en', b'Anglais'), (b'it', b'Italien'), (b'ru', b'Russe')], max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='clientsale',
            name='date_created',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='clientsearch',
            name='date_created',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='contact',
            name='language',
            field=models.CharField(blank=True, choices=[(b'en', b'Anglais'), (b'fr', b'Francais'), (b'it', b'Italien'), (b'ru', b'Russe')], max_length=8, null=True),
        ),
    ]
