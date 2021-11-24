# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_auto_20151207_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientApartmentSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('tags', models.CharField(max_length=255, null=True, blank=True)),
                ('client', models.ForeignKey(to='clients.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
