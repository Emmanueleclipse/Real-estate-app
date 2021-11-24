# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CabinetNotaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=255, null=True, blank=True)),
                ('postcode', models.CharField(max_length=8, null=True, blank=True)),
                ('city', models.CharField(max_length=64, null=True, blank=True)),
                ('telephone', models.CharField(max_length=64, null=True, blank=True)),
                ('fax', models.CharField(max_length=64, null=True, blank=True)),
                ('email', models.EmailField(max_length=255)),
                ('web', models.URLField(max_length=255, null=True, blank=True)),
                ('search', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forename', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=64, null=True, blank=True)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=64, null=True, blank=True)),
                ('mobile', models.CharField(max_length=64, null=True, blank=True)),
                ('photo', models.ImageField(null=True, upload_to=b'notaire_photos', blank=True)),
                ('search', models.CharField(max_length=255, null=True, blank=True)),
                ('cabinet', models.ForeignKey(to='notaires.CabinetNotaire')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
