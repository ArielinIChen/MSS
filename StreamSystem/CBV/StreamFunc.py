# -*- coding: utf-8 -*-
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
relay_log_path = '/var/log/relay_log/'
publish_log_path = '/var/log/publish_log/'


class StartStreamMixin(object):

    def __init__(self, channel_name, stream_method, src_path, dst_path):
        self.channel_name = channel_name
        self.stream_method = stream_method
        self.src_path = src_path
        self.dst_path = dst_path
        self.now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        if self.stream_method == 'streamlink':
            self.title = '_'.join(['Streamlink', self.channel_name, self.now_time])
            self.log_file = ''.join([streamlink_log_path, 'Streamlink_', self.channel_name, '_', self.now_time, '.txt'])

        elif self.stream_method == 'relay':
            self.title = '_'.join(['Relay', self.channel_name, self.now_time])
            self.log_file = ''.join([relay_log_path, 'Relay_', self.channel_name, '_', self.now_time, '.txt'])

        else:   # self.stream_method == 'publish'
            self.title = '_'.join(['Publish', self.channel_name, self.now_time])
            self.log_file = ''.join([publish_log_path, 'Publish_', self.channel_name, '_', self.now_time, '.txt'])

    def start_streamlink(self, **kwargs):
        if self.channel_name == '' or self.channel_name is None:
            return {'error': 'channel_name cannot be None!'}
        elif self.src_path == '' or self.src_path is None:
            return {'error': 'src_path cannot be None!'}
        elif self.dst_path == '' or self.dst_path is None:
            return {'error': 'dst_path cannot be None!'}

        ffmpeg_opts = '%s -xerror -re -y -loglevel info -i - -threads 2 -flags +global_header ' \
                      '-c:a libfdk_aac -b:a 96K -ac 2 -ar 44100 -c:v copy -metadata title="%s" -f flv "%s"' \
                      % (ffmpeg_cmd, self.title, self.dst_path)
        command_line = 'nohup %s --rtmpdump %s "%s" worst -O | %s |& stdbuf -oL tr "\\r" "\\n" 1> "%s" 2>&1 &' \
                       % (streamlink_cmd, rtmpdump_cmd, self.src_path, ffmpeg_opts, self.log_file)
        print command_line
        os.system(command_line)
        check_ps_cmd_1 = 'ps -ef | grep "streamlink" | grep %s | grep -Ev "grep" | wc -l' % self.src_path
        check_ps_cmd_2 = 'ps -ef | grep "ffmpeg" | grep %s | grep -Ev "grep" | wc -l' % self.title
        result_1 = os.popen(check_ps_cmd_1).read()
        result_2 = os.popen(check_ps_cmd_2).read()
        if int(result_1) != 0 and int(result_2) != 0:
            StreamInfo.objects.create(src_path=self.src_path,
                                      dst_path=self.dst_path,
                                      stream_method=self.stream_method,
                                      channel_name=self.channel_name)
            return {'success': 'Create [%s] method stream: [%s] Done!' % (self.stream_method, self.channel_name)}
        else:
            return {'error': 'Create [%s] method stream: [%s] Failed!' % (self.stream_method, self.channel_name)}
        # StreamInfo.objects.create(src_path=self.src_path,
        #                           dst_path=self.dst_path,
        #                           stream_method=self.stream_method,
        #                           channel_name=self.channel_name)
        # return {'success': 'Create [%s] method stream: [%s] Done!' % (self.stream_method, self.channel_name)}
        # return {'error': 'Create [%s] method stream: [%s] Failed!' % (self.stream_method, self.channel_name)}

    def start_publish_or_relay(self, **kwargs):

        command_line = '%s -xerror -y -i "%s" -c:v copy -c:a copy -metadata title="%s" -f flv "%s" &> "%s" &' \
                       % (ffmpeg_cmd, self.src_path, self.title, self.dst_path, self.log_file)
        check_ps_cmd = 'ps -ef | grep "streamlink" | grep %s | grep %s | grep -Ev "grep" | wc -l' % (self.src_path, self.dst_path)

        print command_line
        print check_ps_cmd
        # result = os.system(command_line)
        # result = os.popen(check_ps_cmd)
        # if result != 0:
        # if result == 0:
        #     StreamInfo.objects.create(src_path=self.src_path,
        #                               dst_path=self.dst_path,
        #                               stream_method=self.stream_method,
        #                               channel_name=self.channel_name)
        #     return {'success': 'Create [%s] method stream: [%s] Done!' % (self.stream_method, self.channel_name)}
        # else:
        #     return {'error': 'Create [%s] method stream: [%s] Failed!' % (self.stream_method, self.channel_name)}
        StreamInfo.objects.create(src_path=self.src_path,
                                  dst_path=self.dst_path,
                                  stream_method=self.stream_method,
                                  channel_name=self.channel_name)
        return {'success': 'Create [%s] method stream: [%s] Done!' % (self.stream_method, self.channel_name)}
        # return {'error': 'Create [%s] method stream: [%s] Failed!' % (self.stream_method, self.channel_name)}


class StopStreamMixin(object):

    def __init__(self, channel_name):
        self.channel_name = channel_name

    def stop_stream(self, **kwargs):
        stream_info = StreamInfo.objects.filter(channel_name=self.channel_name)
        if len(stream_info) == 0:
            return {'error': 'Channel_name: %s not found !' % self.channel_name}
        else:
            src_path = stream_info.values()[0]['src_path']
            dst_path = stream_info.values()[0]['dst_path']
            stream_method = stream_info.values()[0]['stream_method']

            if stream_method == 'streamlink':
                command_line = "ps -ef | grep streamlink | grep %s | grep -Ev 'grep' | awk '{print $2}' | xargs -n1 kill -9" % src_path
            else:
                command_line = "ps -ef | grep ffmpeg | grep %s | grep %s | grep -Ev 'grep' | awk '{print $2}' | xargs -n1 kill -9" \
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
                return {'success': 'Stop [%s] method stream: [%s] done!' % (stream_method, self.channel_name)}
            else:
                return {'error': 'Stop [%s] method stream: [%s] failed!' % (stream_method, self.channel_name)}
