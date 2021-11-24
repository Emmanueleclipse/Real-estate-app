# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-05 12:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0019_contact_language'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notaires', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('size', models.IntegerField(blank=True, null=True)),
                ('pieces', models.IntegerField(blank=True, null=True)),
                ('floor', models.IntegerField(blank=True, null=True)),
                ('sale_price', models.IntegerField(blank=True, null=True)),
                ('total_commission', models.IntegerField(blank=True, null=True)),
                ('agency_commission', models.IntegerField(blank=True, null=True)),
                ('sale_lost', models.CharField(blank=True, max_length=255, null=True)),
                ('compromis_sent_buyer', models.DateField(blank=True, null=True)),
                ('compromis_signed_buyer', models.DateField(blank=True, null=True)),
                ('compromis_seller_buyer', models.DateField(blank=True, null=True)),
                ('compromis_signed_sent_buyer', models.DateField(blank=True, null=True)),
                ('compromis_signed_received_buyer', models.DateField(blank=True, null=True)),
                ('compromis_final_signing_date', models.DateField(blank=True, null=True)),
                ('mortgage_offer_received', models.DateField(blank=True, null=True)),
                ('signing_date', models.DateField(blank=True, null=True)),
                ('commission_received_agency', models.DateField(blank=True, null=True)),
                ('commission_received_agent', models.DateField(blank=True, null=True)),
                ('electricity_meter_reading', models.CharField(blank=True, max_length=255, null=True)),
                ('electricity_meter_reading_offpeak', models.CharField(blank=True, max_length=255, null=True)),
                ('water_meter_reading', models.CharField(blank=True, max_length=255, null=True)),
                ('gas_meter_reading', models.CharField(blank=True, max_length=255, null=True)),
                ('last_phone_info', models.CharField(blank=True, max_length=255, null=True)),
                ('electicity_done', models.BooleanField(default=False)),
                ('gas_done', models.BooleanField(default=False)),
                ('water_done', models.BooleanField(default=False)),
                ('insurance_done', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SaleCommission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale')),
            ],
        ),
        migrations.CreateModel(
            name='SaleOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_date', models.DateField(auto_now_add=True)),
                ('offer_amount', models.IntegerField()),
                ('offer_commission', models.IntegerField()),
                ('loan_required', models.BooleanField(default=True)),
                ('made_by_buyer', models.BooleanField(default=True)),
                ('offer_type', models.CharField(blank=True, max_length=255, null=True)),
                ('accepted_date', models.DateField(blank=True, null=True)),
                ('rejected_date', models.DateField(blank=True, null=True)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale')),
            ],
        ),
        migrations.AddField(
            model_name='sale',
            name='accepted_offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_accepted_offer', to='sales.SaleOffer'),
        ),
        migrations.AddField(
            model_name='sale',
            name='agent_buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_agent_buyer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sale',
            name='agent_seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_agent_seller', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sale',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_buyer', to='clients.Client'),
        ),
        migrations.AddField(
            model_name='sale',
            name='current_offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_current_offer', to='sales.SaleOffer'),
        ),
        migrations.AddField(
            model_name='sale',
            name='notaire_buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_notaire_buyer', to='notaires.Notaire'),
        ),
        migrations.AddField(
            model_name='sale',
            name='notaire_clerk_buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_clerk_buyer', to='notaires.Notaire'),
        ),
        migrations.AddField(
            model_name='sale',
            name='notaire_clerk_seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_clerk_seller', to='notaires.Notaire'),
        ),
        migrations.AddField(
            model_name='sale',
            name='notaire_seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_notaire_seller', to='notaires.Notaire'),
        ),
        migrations.AddField(
            model_name='sale',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sale_seller', to='clients.Client'),
        ),
    ]