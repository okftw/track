# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class NutritionInfo(models.Model):
    name = models.CharField(max_length=500,null=True, blank=True)
    info = models.CharField(max_length=500,null=True, blank=True)
    glycemicindex = models.IntegerField(null=True, blank=True)
    glycemicload = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.name

# Create your models here.
class Entries(models.Model):
    Date                   = models.DateField(auto_now_add=True)
    DateTime               = models.DateTimeField(auto_now_add=True)
    Username               = models.CharField(max_length=200,null=True, blank=True)
    Tracking               = models.CharField(max_length=200,null=True, blank=True)
    String_Value           = models.CharField(max_length=200,null=True, blank=True)
    Numerical_Value        = models.CharField(max_length=200,null=True, blank=True)
    Additional_Information = models.CharField(max_length=200,null=True, blank=True)
    Nurtrition_Info        = models.ForeignKey(NutritionInfo, on_delete=models.CASCADE,null=True, blank=True)

    #author = models.ForeignKey(User, default=None, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
            return self.String_Value

class Exercise(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user  = models.OneToOneField(
                User,
                on_delete=models.CASCADE,
                blank=True,
                null=True,
                unique=True,
                related_name='userprofile'
            )
    age    = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=200,null=True, blank=True)
    weight_tracker = models.BooleanField(default=True)
    bm_tracker = models.BooleanField(default=False)
    countdown_number = models.IntegerField(null=True, blank=True, default=60)

    def __str__(self):
            return self.user.username
