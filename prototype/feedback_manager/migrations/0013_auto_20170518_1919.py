# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 13:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback_manager', '0012_timeslot_time_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='Time_table',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='feedback_manager.TimeTable'),
            preserve_default=False,
        ),
    ]
