# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0008_agency_web_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outsideagent',
            name='agency',
        ),
        migrations.DeleteModel(
            name='OutsideAgent',
        ),
        migrations.AddField(
            model_name='agent',
            name='role',
            field=models.CharField(max_length=254, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agent',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
