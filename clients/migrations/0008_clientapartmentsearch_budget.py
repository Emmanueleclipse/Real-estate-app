# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_clientapartmentsearch'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientapartmentsearch',
            name='budget',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
