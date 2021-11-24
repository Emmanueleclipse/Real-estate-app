# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_auto_20150912_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='status',
            field=models.IntegerField(blank=True, null=True, choices=[(10, b'M'), (10, b'Mr'), (20, b'Mme'), (20, b'Mrs'), (30, b'Mlle'), (40, b'Dr'), (50, b'Prof')]),
            preserve_default=True,
        ),
    ]
