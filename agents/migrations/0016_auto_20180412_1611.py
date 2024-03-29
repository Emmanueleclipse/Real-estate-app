# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-12 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0015_auto_20180406_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentmailbox',
            name='display_name',
            field=models.CharField(default='None', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agentmailbox',
            name='email',
            field=models.CharField(default='test@test.com', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agentmailbox',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mailprovider',
            name='imap_port',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mailprovider',
            name='smtp_port',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
