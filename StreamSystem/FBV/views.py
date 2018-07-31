# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from StreamSystem.FBV.relay_and_publish_func import start_relay_or_publish
from StreamSystem.FBV.stop_stream_func import stop_stream_process
from StreamSystem.FBV.streamlink_func import start_streamlink
from StreamSystem.models import StreamInfo, User

# Create your views here.

logger = logging.getLogger(__name__)


class JsonResponseMixin(object):

    @staticmethod
    def json_response(content):
        return HttpResponse(json.dumps(content))


def encode_pw(ori_pw):
    # tmp_pw = make_password(ori_pw, '123456').split('$')[3]
    tmp_pw_plus_salt = str(ori_pw) + 'what1the@fuck3is$that5'
    return make_password(tmp_pw_plus_salt)


def index(request):
    return render(request, 'index.html')


def check_log(request):
    return render(request, 'check_log.html')


def login_page(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print username, password
        if username == '' or username is None or password == '' or password is None:
            return HttpResponse('username or password cannot be None')
        try:
            user = User.objects.get(username=username)
        except Exception:
            return HttpResponse('username: %s not found' % username)
        else:
            pw_input = encode_pw(ori_pw=password)
            pw_in_db = user.password
            if not check_password(pw_input, pw_in_db):
                return HttpResponse('username and password not match')
            else:
                request.session['is_login'] = True
                request.session['username'] = username
                resp = redirect('/index/')
                resp.set_cookie('username', username, 60*60*7)
                return resp
    else:
        return render(request, 'login_page.html')


def register_page(request):
    return render(request, 'register_page.html')


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


def add_stream(request):
    if request.method == 'POST':
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
            if stream_method == 'streamlink':
                reply = start_streamlink(src_path, dst_path, channel_name)
            else:
                reply = start_relay_or_publish(src_path, dst_path, stream_method, channel_name)

        if reply == 'success':
            return HttpResponse(json.dumps({'success': 'Create Done!'}))
        else:
            return HttpResponse(json.dumps({'error': 'Create Failed!'}))


def stop_stream(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        channel_name = received_json_data['channel_name']

        reply = stop_stream_process(channel_name)
        return HttpResponse(json.dumps(reply))


def show_log_file(request):
    if request.method == 'GET':
        return HttpResponse('the return string for test 1111 yahaha~\n' * 20)
        # channel_name = request.GET.get('channel_name')
        # if channel_name == '' or channel_name is None:
        #     return HttpResponse('channel_name is null, please check')
        # else:
        #     reply = read_file(channel_name)
        #     return HttpResponse(json.dumps(reply))
