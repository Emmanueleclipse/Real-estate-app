# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-11-25 17:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnreadChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(db_index=True)),
                ('from_agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lastchat_from_agent', to=settings.AUTH_USER_MODEL)),
                ('msg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.Chat')),
                ('to_agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='last_chat_to_agent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
