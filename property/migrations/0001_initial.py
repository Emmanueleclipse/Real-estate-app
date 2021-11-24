# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-12-28 18:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mandat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('contract', models.CharField(blank=True, choices=[('simple', 'Simple'), ('exclusive', 'Exclusif'), ('coexclusive', 'Co-exclusif'), ('delegation', 'D\xe9l\xe9gation')], max_length=255, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('what', models.CharField(blank=True, choices=[('apartment', 'Appartement'), ('villa', 'Villa'), ('parking', 'Parking')], max_length=255, null=True)),
                ('size', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('owner', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
                ('telephone', models.CharField(blank=True, max_length=255, null=True)),
                ('sale_price', models.IntegerField()),
                ('commission', models.IntegerField(blank=True, null=True)),
                ('commission_percent', models.IntegerField(blank=True, null=True)),
                ('sold', models.CharField(blank=True, choices=[('sold', 'Vendu'), ('ours', 'Vendu par nous'), ('others', 'Vendu par autre agence'), ('owner', 'Vendu par propri\xe9taire'), ('cancelled', 'Retir\xe9 par propri\xe9taire'), ('withdrawn', 'Retir\xe9 par agence')], max_length=255, null=True)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mandat_agent', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
    ]
