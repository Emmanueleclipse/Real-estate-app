# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-18 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0015_clientsale_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='relationship',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
