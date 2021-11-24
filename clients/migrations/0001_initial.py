# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0003_auto_20150218_1110'),
        ('notaires', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateField()),
                ('date_updated', models.DateField()),
                ('agent', models.ForeignKey(to='agents.Agent')),
                ('preferred_notaire', models.ForeignKey(blank=True, to='notaires.Notaire', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(0, b'(Principal)'), (10, b'Partner'), (20, b'Assistant'), (30, b'Sibling')])),
                ('forename', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=64, null=True, blank=True)),
                ('mobile', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone_home', models.CharField(max_length=64)),
                ('phone_office', models.CharField(max_length=64)),
                ('search', models.CharField(max_length=255, null=True, blank=True)),
                ('client', models.ForeignKey(to='clients.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
