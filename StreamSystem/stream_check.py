# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time

from StreamSystem.FBV.relay_and_publish_func import start_relay_or_publish
from StreamSystem.FBV.streamlink_func import start_streamlink

from StreamSystem.FBV.stop_stream_func import stop_stream_process
from StreamSystem.models import StreamInfo


def stream_process_check():
    streams = StreamInfo.objects.all()
    if len(streams) == 0:
        return 'No stream in process'
    else:
        check_command = 'ps -ef | grep "%s" | grep "%s" | grep -Ev "grep" | wc -l'
        streams_info = streams.values()
        for stream in streams_info:
            channel_name = stream['channel_name']
            stream_method = stream['stream_method']
            src_path = stream['src_path']
            dst_path = stream['dst_path']
            print check_command % (src_path, dst_path)
            # ps_count = int(os.popen(check_command % (src_path, dst_path)).read())
            # if ps_count == 0:
            #     if stream_method == 'streamlink':
            #         start_streamlink(src_path, dst_path, channel_name)
            #     else:
            #         start_relay_or_publish(src_path, dst_path, stream_method, channel_name)
            # elif ps_count == 1:
            #     pass
            # else:
            #     stop_stream_process(channel_name)
            #     time.sleep(10)
            #     if stream_method == 'streamlink':
            #         start_streamlink(src_path, dst_path, channel_name)
            #     else:
            #         start_relay_or_publish(src_path, dst_path, stream_method, channel_name)
