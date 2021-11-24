# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0009_auto_20150416_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
