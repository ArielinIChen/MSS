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

'''
Relay Example:
platform_live: AnyCast_C2_7e4341a07ed059bcda17e0937a0fe445
main_url: rtmp://douyu.com/helloworld_test
sub_url: rtmp://127.0.0.1/match/MatchStream_c2
publish_url: rtmp://127.0.0.1/relay/anycast
platform: AnyCast_2_7e4341a07ed059bcda17e0937a0fe445
host: tv.imbatv.cn
bitrate: 3000K
logfile: /main_disk/logs/cmd_switch_rtmp_AnyCast_2_2018-06-25-14-38-38.txt

***** start channel: AnyCast_2 on 06-25-14:38:38 *****
cmd: /usr/local/bin/av_publish -xerror -y -i "rtmp://127.0.0.1/match/MatchStream_c2" -c:v copy -c:a copy  -metadata title='anycast_AnyCast_2_7e4341a07ed059bcda17e0937a0fe445' -f flv 'rtmp://douyu.com/helloworld_test' &> '/main_disk/logs/switch_rtmp/switch_rtmp-06-25-14-38-38-1183606628-AnyCast_2.txt'
'''

ffmpeg_cmd = '/usr/local/bin/ffmpeg'
relay_log_path = '/var/log/relay_log/'
publish_log_path = '/var/log/publish_log/'


def start_relay_or_publish(src_path, dst_path, stream_method, channel_name, **kwargs):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    if stream_method == 'relay':
        title = '_'.join(['Relay', channel_name, now_time])
        log_file = ''.join([relay_log_path, 'Relay_', now_time, '.txt'])
    else:
        title = '_'.join(['Publish', channel_name, now_time])
        log_file = ''.join([publish_log_path, 'Relay_', now_time, '.txt'])

    command_line = '%s -xerror -y -i "%s" -c:v copy -c:a copy -metadata title="%s" -f flv "%s" &> "%s"' \
                   % (ffmpeg_cmd, src_path, title, dst_path, log_file)

    print command_line
    # result = os.system(command_line)
    # if result == 0:
    #     StreamInfo.objects.create(src_path=src_path,
    #                               dst_path=dst_path,
    #                               stream_method=stream_method,
    #                               channel_name=channel_name)
    #     return 'success'
    # else:
    #     return 'failed'
    StreamInfo.objects.create(src_path=src_path,
                              dst_path=dst_path,
                              stream_method=stream_method,
                              channel_name=channel_name)
    return 'success'


if __name__ == '__main__':
    start_relay_or_publish('rtmp://127.0.0.1/match/MatchStream_c2',
                           'rtmp://douyu.com/helloworld_test',
                           'publish',
                           'publish_test_from_pycharm')

    start_relay_or_publish('rtmp://send.imbatv.cn/match/MatchStream_c2&abc=123&def=%n%b%cadfqer',
                           'rtmp://douyu.com/helloworld_test234&kkkyyqq=bazcxv123',
                           'relay',
                           'relay_test_from_pycharm')
