# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from StreamSystem.models import StreamInfo, User

# Register your models here.


class StreamInfoAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'stream_method', 'src_path', 'dst_path', 'create_time')


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')


admin.site.register(StreamInfo, StreamInfoAdmin)
admin.site.register(User, UserAdmin)
