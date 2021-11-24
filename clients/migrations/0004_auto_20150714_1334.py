# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20150218_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=64)),
                ('status', models.IntegerField(blank=True, null=True, choices=[(210, b'Home'), (220, b'Work'), (230, b'List')])),
                ('relpy_to', models.BooleanField(default=False)),
                ('contact', models.ForeignKey(to='clients.Contact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactPhone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=64)),
                ('status', models.IntegerField(blank=True, null=True, choices=[(110, b'Mobile'), (120, b'Home'), (130, b'Office')])),
                ('contact', models.ForeignKey(to='clients.Contact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='contact',
            name='email',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='phone_home',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='phone_office',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='type',
        ),
        migrations.AddField(
            model_name='contact',
            name='relationship',
            field=models.IntegerField(blank=True, null=True, choices=[(10, b'Partner'), (20, b'Husband'), (30, b'Wife'), (40, b'Brother'), (50, b'Sister'), (60, b'Mother'), (70, b'Father'), (80, b'Cousin'), (100, b'Assistant'), (110, b'Personal Assistant'), (120, b'Property Manager'), (130, b'Cleaner')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='status',
            field=models.IntegerField(blank=True, null=True, choices=[(10, b'M'), (20, b'Mme'), (30, b'Mlle'), (40, b'Dr'), (50, b'Prof')]),
            preserve_default=True,
        ),
    ]
