# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0006_auto_20150317_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'agency_logos', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agent',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'agent_images', blank=True),
            preserve_default=True,
        ),
    ]
