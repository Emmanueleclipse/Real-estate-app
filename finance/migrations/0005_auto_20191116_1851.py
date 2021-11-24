# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-11-16 17:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0017_agentsettings'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0001_initial'),
        ('finance', '0004_supplier_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=255)),
                ('bank_address', models.CharField(max_length=255)),
                ('account_name', models.CharField(max_length=255)),
                ('iban', models.CharField(max_length=255)),
                ('bic', models.CharField(blank=True, max_length=255, null=True)),
                ('opened_date', models.DateField(blank=True, null=True)),
                ('closed_date', models.DateField(blank=True, null=True)),
                ('current', models.BooleanField(default=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('agency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bankaccount_agency', to='agents.Agency')),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bankaccount_agent', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-opened_date'],
            },
        ),
        migrations.CreateModel(
            name='BankEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.IntegerField()),
                ('reference', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=255)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bankentry_account', to='finance.BankAccount')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='FactureAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('invoice_number', models.CharField(max_length=255)),
                ('commission', models.IntegerField(blank=True, null=True)),
                ('commission_percent', models.IntegerField(blank=True, null=True)),
                ('vat', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factureagent_agent', to=settings.AUTH_USER_MODEL)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factureagent_bankaccount', to='finance.BankAccount')),
                ('facture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='factureagent_upload', to='files.Upload')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='FactureApporteur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('invoice_number', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('iban', models.CharField(max_length=255)),
                ('bic', models.CharField(blank=True, max_length=255, null=True)),
                ('commission', models.IntegerField()),
                ('vat', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factureapporteur_agent', to=settings.AUTH_USER_MODEL)),
                ('facture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='factureapporteur_upload', to='files.Upload')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='FactureNotaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('invoice_number', models.CharField(max_length=255)),
                ('client_name', models.CharField(max_length=255)),
                ('client_address', models.CharField(max_length=255)),
                ('other_agency', models.CharField(blank=True, max_length=255, null=True)),
                ('property_address', models.CharField(max_length=255)),
                ('commission', models.IntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facturenotaire_agent', to=settings.AUTH_USER_MODEL)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facturenotaire_bankaccount', to='finance.BankAccount')),
                ('facture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facturenotaire_upload', to='files.Upload')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='FactureSeasonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('invoice_number', models.CharField(max_length=255)),
                ('commission', models.IntegerField()),
                ('vat', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factureseasonal_agent', to=settings.AUTH_USER_MODEL)),
                ('facture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='factureseasonal_upload', to='files.Upload')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factureseasonal_sale', to='finance.FactureNotaire')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddField(
            model_name='facturesupplier',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='factureapporteur',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factureapporteur_sale', to='finance.FactureNotaire'),
        ),
        migrations.AddField(
            model_name='factureagent',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factureagent_sale', to='finance.FactureNotaire'),
        ),
    ]
