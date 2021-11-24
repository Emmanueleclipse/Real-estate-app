# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prefix', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=64)),
                ('postfix', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=8)),
                ('city', models.CharField(max_length=64)),
                ('telephone', models.CharField(max_length=64)),
                ('fax', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=255)),
                ('web', models.URLField(max_length=255)),
                ('search', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'agencies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forename', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=64)),
                ('mobile', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=255)),
                ('photo', models.ImageField(upload_to=b'agent_photos')),
                ('search', models.CharField(max_length=255)),
                ('agency', models.ForeignKey(to='agents.Agency')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
