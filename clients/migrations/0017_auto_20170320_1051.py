# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-20 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0016_auto_20170318_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='relationship',
            field=models.IntegerField(blank=True, choices=[(10, b'Partner'), (20, b'Husband'), (30, b'Wife'), (40, b'Brother'), (50, b'Sister'), (60, b'Mother'), (70, b'Father'), (80, b'Cousin'), (90, b'Friend'), (100, b'Assistant'), (110, b'Personal Assistant'), (120, b'Property Manager'), (130, b'Cleaner'), (999, b'Other')], null=True),
        ),
    ]
