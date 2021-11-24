# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-03 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_auto_20160209_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientactivity',
            name='type',
            field=models.CharField(choices=[(b'note', b'Note'), (b'email', b'Email'), (b'telephone', b'Telephone'), (b'rendezvous', b'Rendez-vous'), (b'passage', b'Passage')], default=b'note', max_length=255),
        ),
        migrations.AlterField(
            model_name='contact',
            name='search',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]