# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-24 17:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0014_auto_20170224_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientsale',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
