# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-11-27 13:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20171127_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unreadchat',
            name='message',
        ),
        migrations.AlterField(
            model_name='unreadchat',
            name='when',
            field=models.DateTimeField(auto_now=True),
        ),
    ]