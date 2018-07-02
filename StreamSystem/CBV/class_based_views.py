# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import logging

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from StreamSystem.CBV.StreamFunc import StartStreamMixin, StopStreamMixin
from StreamSystem.models import StreamInfo

# Create your views here.

logger = logging.getLogger(__name__)


class JsonResponseMixin(object):

    @staticmethod
    def json_response(content):
        return HttpResponse(json.dumps(content))


def index(request):
    return render(request, 'index.html')


def show_stream(request):
    on_stream_list = list(StreamInfo.objects.all().values())
    if len(on_stream_list) > 0:
        time_delta = datetime.timedelta(hours=8)
        for i in range(len(on_stream_list)):
            on_stream_list[i]['create_time'] = \
                (on_stream_list[i]['create_time'] + time_delta).strftime('%Y-%m-%d_%H-%M-%S')
        on_stream_list.insert(0, 'Filled')
    else:
        on_stream_list.insert(0, 'Empty')
    return HttpResponse(json.dumps(on_stream_list))


class StartStream(JsonResponseMixin, View):

    def post(self, request):
        received_json_data = json.loads(request.body)
        channel_name = received_json_data['channel_name']
        stream_method = received_json_data['stream_method']
        src_path = received_json_data['src_path']
        dst_path = received_json_data['dst_path']

        stream_in_db = StreamInfo.objects.filter(src_path=src_path, dst_path=dst_path, stream_method=stream_method)
        channel_name_in_db = StreamInfo.objects.filter(channel_name=channel_name)
        if len(stream_in_db) > 0:
            return HttpResponse(json.dumps({'error': 'This Stream is existed !'}))
        elif len(channel_name_in_db) > 0:
            return HttpResponse(json.dumps({'error': 'Duplicate channel_name !'}))
        else:
            reply = StartStreamMixin(channel_name, stream_method, src_path, dst_path)
            if stream_method == 'streamlink':
                return self.json_response(reply.start_streamlink())
            else:
                return self.json_response(reply.start_publish_or_relay())


class StopStream(JsonResponseMixin, View):
    def post(self, request):
        received_json_data = json.loads(request.body)
        channel_name = received_json_data['channel_name']

        reply = StopStreamMixin(channel_name).stop_stream()
        return self.json_response(reply)
