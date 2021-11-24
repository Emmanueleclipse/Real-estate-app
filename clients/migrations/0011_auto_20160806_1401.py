# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-06 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0010_auto_20160803_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientactivity',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='clientactivity',
            name='type',
            field=models.CharField(choices=[(b'note', b'Note'), (b'email', b'Email'), (b'telephone', b'Telephone'), (b'rendezvous', b'Rendez-vous'), (b'passage', b'Passage'), (b'web', b'Web site')], default=b'note', max_length=255),
        ),
    ]