# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback_manager', '0002_auto_20170517_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergrademap',
            name='grade',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], default='A', max_length=1),
        ),
    ]
