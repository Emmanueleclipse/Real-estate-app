# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-12 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0025_auto_20180411_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientlead',
            name='source_id',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
