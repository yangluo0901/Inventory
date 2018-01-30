# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthdate = models.DateField(max_length =20, null=True)
    level =  models.IntegerField(default = 1);# 2 IS MANAGEMENT LEVEL
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
class Inventory(models.Model):
    name = models.CharField( max_length = 255)
    lot_num = models.CharField(max_length = 15)
    location = models.CharField(max_length = 50)
    container = models.CharField(max_length = 100)
    net_quantity = models.IntegerField()
    pnet_quantity = models.IntegerField()
    tquantity = models.FloatField(default = None)
    mfg_date = models.DateTimeField()
    action = models.TextField()
