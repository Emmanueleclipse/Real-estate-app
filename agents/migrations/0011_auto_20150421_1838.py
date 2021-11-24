# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import agents.models


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0010_auto_20150416_0810'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='owner',
            field=models.ForeignKey(related_name='agencyowner', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='branch',
            field=agents.models.CharNullField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='fax',
            field=agents.models.CharNullField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='postfix',
            field=agents.models.CharNullField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='prefix',
            field=agents.models.CharNullField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='telephone',
            field=agents.models.CharNullField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
    ]
