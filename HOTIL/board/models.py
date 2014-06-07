# -*- coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Problem(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(User, related_name='problems')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    html = models.CharField(max_length=50)
admin.site.register(Problem)

class HWPFile(models.Model):
    hwp = models.FileField(upload_to='hwp')
