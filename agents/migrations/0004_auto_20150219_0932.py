# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0003_auto_20150218_1110'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutsideAgent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forename', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=64, null=True, blank=True)),
                ('mobile', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('photo', models.ImageField(null=True, upload_to=b'agent_photos', blank=True)),
                ('search', models.CharField(max_length=255, null=True, blank=True)),
                ('agency', models.ForeignKey(to='agents.Agency')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='agent',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='is_admin',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agent',
            name='password',
            field=models.CharField(default='test', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agent',
            name='agency',
            field=models.ForeignKey(blank=True, to='agents.Agency', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agent',
            name='email',
            field=models.EmailField(default='info@bienfacile.com', unique=True, max_length=255, verbose_name=b'email address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agent',
            name='forename',
            field=models.CharField(max_length=254),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agent',
            name='mobile',
            field=models.CharField(max_length=254, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agent',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'developer_images', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agent',
            name='surname',
            field=models.CharField(default='TEST', max_length=254),
            preserve_default=False,
        ),
    ]
