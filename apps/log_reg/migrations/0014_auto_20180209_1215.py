# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-09 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_reg', '0013_auto_20180209_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='mfg_date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='pnet_quantity',
            field=models.FloatField(default=0),
        ),
    ]
