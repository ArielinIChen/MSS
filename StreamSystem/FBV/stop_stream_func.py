# -*- coding: utf-8 -*-
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MSS.settings")
# django.setup()
from __future__ import unicode_literals

import streamlink
import datetime
import os

from StreamSystem.models import StreamInfo


def stop_stream_process(channel_name, **kwargs):
    stream_info = StreamInfo.objects.filter(channel_name=channel_name)
    if len(stream_info) == 0:
        return {'error': 'Channel_name: %s not found !' % channel_name}
    else:
        stream_method = stream_info.values()[0]['stream_method']
        src_path = stream_info.values()[0]['src_path']
        dst_path = stream_info.values()[0]['dst_path']

        command_line = "ps -ef | grep %s | grep %s | grep -Ev 'grep' | awk '{print $2}' | xargs -n1 kill -9" \
                       % (src_path, dst_path)

        count = 0
        print command_line

        # while count < 3:
        #     result = os.system(command_line)
        #     if result == 0:
        #         stream_info.delete()
        #         break
        #     else:
        #         count += 1

        stream_info.delete()
        if count < 3:
            return {'success': 'stop stream %s done!' % channel_name}
        else:
            return {'error': 'stop stream %s failed!' % channel_name}


if __name__ == '__main__':
    stop_stream_process(channel_name='name4')
