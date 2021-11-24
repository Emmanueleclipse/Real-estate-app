# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0002_auto_20150218_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='agent',
        ),
        migrations.RemoveField(
            model_name='client',
            name='preferred_notaire',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='client',
        ),
        migrations.DeleteModel(
            name='Client',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.RemoveField(
            model_name='notaire',
            name='cabinet',
        ),
        migrations.DeleteModel(
            name='CabinetNotaire',
        ),
        migrations.DeleteModel(
            name='Notaire',
        ),
    ]
