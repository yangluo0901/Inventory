# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-29 11:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_reg', '0018_auto_20180328_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='document',
            field=models.ImageField(default=None, upload_to='documents/%Y/%m/%d'),
        ),
    ]