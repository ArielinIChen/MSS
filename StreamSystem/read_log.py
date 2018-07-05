# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from StreamSystem.models import StreamInfo

import os

streamlink_log_path = '/var/log/streamlink_log/'
relay_log_path = '/var/log/relay_log/'
publish_log_path = '/var/log/publish_log/'


def read_file(channel_name):
    stream_info = StreamInfo.objects.filter(channel_name=channel_name)
    if len(stream_info) == 0:
        return 'Error: %s not found in db' % channel_name
    elif len(stream_info) > 1:
        return 'Error: duplicate %s found in db' % channel_name
    else:
        stream_method = stream_info.values()[0]['stream_method']
        if stream_method == 'streamlink':
            log_path = streamlink_log_path
        elif stream_method == 'relay':
            log_path = relay_log_path
        else:
            log_path = publish_log_path
        file_name = str(os.popen('ls %s | grep %s' % (log_path, channel_name)).read())
        file_path = ''.join([log_path, file_name])
        file_read = os.popen('tail -100 %s' % file_path).read()
        return file_read
