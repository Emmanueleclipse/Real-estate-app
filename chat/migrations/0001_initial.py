# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-29 14:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agents', '0013_agency_lat_long'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now=True)),
                ('message', models.TextField()),
                ('from_agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_from_agent', to=settings.AUTH_USER_MODEL)),
                ('to_agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_to_agent', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-when'],
            },
        ),
        migrations.CreateModel(
            name='GroupChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now=True)),
                ('message', models.TextField()),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupchat_agency', to='agents.Agency')),
                ('from_agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupchat_from_agent', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-when'],
            },
        ),
    ]