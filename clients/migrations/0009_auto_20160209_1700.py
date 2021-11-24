# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_clientapartmentsearch_budget'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('client', models.ForeignKey(to='clients.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClientSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('what', models.CharField(default=b'apartment', max_length=255, choices=[(b'appartement', b'Appartement'), (b'villa', b'Villa'), (b'commerce', b'Commerce'), (b'terrain', b'Terrain'), (b'garage', b'Garage')])),
                ('description', models.TextField()),
                ('budget', models.IntegerField(null=True, blank=True)),
                ('tags', models.CharField(max_length=255, null=True, blank=True)),
                ('client', models.ForeignKey(to='clients.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='clientapartmentsearch',
            name='client',
        ),
        migrations.DeleteModel(
            name='ClientApartmentSearch',
        ),
        migrations.AddField(
            model_name='client',
            name='last_contact',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='next_contact',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='client',
            name='trash',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
