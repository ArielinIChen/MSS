# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
from celery import task
import datetime
from StreamSystem.stream_check import stream_process_check


@task
def chk_stream_process():
    stream_process_check()

