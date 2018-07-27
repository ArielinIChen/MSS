# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render, redirect

from StreamSystem.models import User

import datetime


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' or username is None or password == '' or password is None:
            return HttpResponse('username or password cannot be None')
        elif len(User.objects.filter(username=username)) == 0:
            return HttpResponse('username: %s not found' % username)
        elif len(User.objects.filter(username=username, password=password)) == 0:
            return HttpResponse('username and password not match')
        else:
            request.session['username'] = username
            resp = redirect('/index/')
            resp.set_cookie('username', username, 60*60*7)
            return resp


def logout(request):
    pass


def register(request):
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
