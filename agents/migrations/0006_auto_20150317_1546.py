# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0005_auto_20150312_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='apimo_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='emulis_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='fnaim_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='orpi_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agency',
            name='seloger_id',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
