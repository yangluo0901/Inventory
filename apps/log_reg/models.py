# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="userprofile")
    birthdate = models.DateField(max_length =20, null=True)
    level =  models.IntegerField(default = 1);# 2 IS MANAGEMENT LEVEL
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()



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
