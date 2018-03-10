# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-09 17:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tvtrail', '0009_auto_20180302_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_episode_relation',
            name='show',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='tvtrail.tv_show'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user_episode_relation',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=2),
        ),
        migrations.AlterField(
            model_name='user_show_relation',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=None, max_digits=2),
        ),
    ]
