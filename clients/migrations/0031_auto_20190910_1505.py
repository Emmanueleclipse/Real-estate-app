# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-09-10 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0030_client_hot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientactivity',
            name='date_created',
            field=models.DateTimeField(),
        ),
    ]
