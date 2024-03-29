# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-06 10:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0019_contact_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientLead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, max_length=255, null=True)),
                ('source_url', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('buying', models.TextField()),
                ('selling', models.TextField()),
                ('notes', models.TextField()),
                ('assigned_agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leadagent', to='clients.Client')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leadclient', to='clients.Client')),
            ],
        ),
    ]
