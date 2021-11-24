# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0007_auto_20150318_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='web_listing',
            field=models.URLField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
