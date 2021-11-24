# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_auto_20150714_1334'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactemail',
            old_name='relpy_to',
            new_name='reply_to',
        ),
        migrations.RemoveField(
            model_name='contactemail',
            name='status',
        ),
        migrations.RemoveField(
            model_name='contactphone',
            name='status',
        ),
        migrations.AddField(
            model_name='contactemail',
            name='type',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactphone',
            name='type',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
    ]
