# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from StreamSystem.models import StreamInfo

# Register your models here.


class StreamInfoAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'stream_method', 'src_path', 'dst_path', 'create_time')


admin.site.register(StreamInfo, StreamInfoAdmin)
