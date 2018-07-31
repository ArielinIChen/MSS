# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, response
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from StreamSystem.models import User

import datetime


def encode_pw(ori_pw):
    # tmp_pw = make_password(ori_pw, '123456').split('$')[3]
    tmp_pw_plus_salt = str(ori_pw) + 'what1the@fuck3is$that5'
    return make_password(tmp_pw_plus_salt)


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    else:
        username = request.session['username']
        resp = HttpResponse('%s Sign Out!' % username)
        resp.delete_cookie('username')
        request.session.flush()
        return resp


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' or username is None or password == '' or password is None:
            return HttpResponse('username or password cannot be None')
        elif len(User.objects.filter(username=username)) != 0:
            return HttpResponse('username: %s is been used' % username)
        else:
            User.objects.create(username=username, password=password)
            resp = redirect('/index/')
            resp.set_cookie('username', username, 60*60*7)
            return resp


