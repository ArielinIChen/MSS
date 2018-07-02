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
Streamlink Example:
platform_live: Streamlink_C4_7e4341a07ed059bcda17e0937a0fe445
main_url: rtmp://127.0.0.1/match/segment_pubg
sub_url: https://www.panda.tv/imbachiji
publish_url: rtmp://127.0.0.1/relay/streamlink
platform: Streamlink_4_7e4341a07ed059bcda17e0937a0fe445
host: tv.imbatv.cn
bitrate: 3000K
logfile: /main_disk/logs/cmd_switch_rtmp_Streamlink_4_2018-06-25-10-59-00.txt

***** start channel: Streamlink_4 on 06-25-10:59:00 *****
cmd: /usr/local/bin/streamlink --http-cookie cid=8991c91135bd5ad6fd8a9f988ae0b897_Streamlink_4_7e4341a07ed059bcda17e0937a0fe445 --rtmpdump /usr/local/bin/rtmpdump "https://www.panda.tv/imbachiji" best -O |  /usr/local/bin/av_publish -xerror -re -y -loglevel info -i - -threads 2 -flags +global_header -c:a libfdk_aac -b:a 96K -ac 2 -ar 44100 -c:v copy -metadata title='switch_Streamlink_4_7e4341a07ed059bcda17e0937a0fe445' -f flv 'rtmp://127.0.0.1/match/segment_pubg' &> '/main_disk/logs/switch_rtmp/switch_rtmp-06-25-10-59-00-698867512-Streamlink_4.txt'

[cli][info] Found matching plugin pandatv for URL https://www.panda.tv/imbachiji
[plugin.pandatv][info] Stream currently unavailable.
error: No playable streams found on this URL: https://www.panda.tv/imbachiji
'''

streamlink_cmd = '/usr/local/bin/streamlink'
rtmpdump_cmd = '/usr/local/bin/rtmpdump'
ffmpeg_cmd = '/usr/local/bin/ffmpeg'
streamlink_log_path = '/var/log/streamlink_log/'


def start_streamlink(src_path, dst_path, channel_name, **kwargs):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    title = '_'.join(['Streamlink', channel_name, now_time])
    log_file = ''.join([streamlink_log_path, 'Streamlink_', now_time, '.txt'])
    ffmpeg_opts = ' -xerror -re -y -loglevel info -i - -threads 2 -flags +global_header ' \
                  '-c:a libfdk_aac -b:a 96K -ac 2 -ar 44100 -c:v copy -metadata title="%s" -f flv' % title

    command_line = '%s -rtmpdump %s "%s" best -O | %s %s "%s" &> "%s"' \
                   % (streamlink_cmd, rtmpdump_cmd, src_path, ffmpeg_cmd, ffmpeg_opts, dst_path, log_file)

    print command_line
    # result = os.system(command_line)
    # if result == 0:
    #     StreamInfo.objects.create(src_path=src_path,
    #                               dst_path=dst_path,
    #                               stream_method='streamlink',
    #                               channel_name=channel_name)
    #     return 'success'
    # else:
    #     return 'failed'
    StreamInfo.objects.create(src_path=src_path,
                              dst_path=dst_path,
                              stream_method='streamlink',
                              channel_name=channel_name)
    return 'success'


if __name__ == '__main__':
    start_streamlink('https://www.panda.tv/imbachiji', 'twitch.tv/chichichi', 'streamlink_test_from_pycharm')
