# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CabinetNotaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=255, null=True, blank=True)),
                ('postcode', models.CharField(max_length=8, null=True, blank=True)),
                ('city', models.CharField(max_length=64, null=True, blank=True)),
                ('telephone', models.CharField(max_length=64, null=True, blank=True)),
                ('fax', models.CharField(max_length=64, null=True, blank=True)),
                ('email', models.EmailField(max_length=255)),
                ('web', models.URLField(max_length=255, null=True, blank=True)),
                ('search', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateField()),
                ('date_updated', models.DateField()),
                ('agent', models.ForeignKey(to='agents.Agent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(0, b'(Principal)'), (10, b'Partner'), (20, b'Assistant'), (30, b'Sibling')])),
                ('forename', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=64, null=True, blank=True)),
                ('mobile', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone_home', models.CharField(max_length=64)),
                ('phone_office', models.CharField(max_length=64)),
                ('search', models.CharField(max_length=255, null=True, blank=True)),
                ('client', models.ForeignKey(to='agents.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notaire',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('forename', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=64, null=True, blank=True)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=64, null=True, blank=True)),
                ('mobile', models.CharField(max_length=64, null=True, blank=True)),
                ('photo', models.ImageField(null=True, upload_to=b'notaire_photos', blank=True)),
                ('search', models.CharField(max_length=255, null=True, blank=True)),
                ('cabinet', models.ForeignKey(to='agents.CabinetNotaire')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PreviousAgency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agency', models.ForeignKey(to='agents.Agency')),
                ('agent', models.ForeignKey(to='agents.Agent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='client',
            name='preferred_notaire',
            field=models.ForeignKey(blank=True, to='agents.Notaire', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='address',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='city',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='fax',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='postcode',
            field=models.CharField(max_length=8, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='postfix',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='prefix',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='search',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='telephone',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agency',
            name='web',
            field=models.URLField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agent',
            name='email',
            field=models.EmailField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agent',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'agent_photos', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agent',
            name='search',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agent',
            name='surname',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
    ]
