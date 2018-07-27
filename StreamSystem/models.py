# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class StreamInfo(models.Model):
    channel_name = models.CharField(max_length=50, blank=True, default=None)
    stream_method = models.CharField(max_length=50, blank=True, default=None)
    src_path = models.CharField(max_length=200, blank=True, default=None)
    dst_path = models.CharField(max_length=200, blank=True, default=None)
    create_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.channel_name


class User(models.Model):
    username = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=50, blank=False)
    # email = models.EmailField(blank=True, default=None)
    create_time = models.DateTimeField(auto_now=True)
    last_login_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.username
