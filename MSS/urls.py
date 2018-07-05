"""MSS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from StreamSystem.FBV import views as ss_fbv
from StreamSystem.CBV import class_based_views as ss_cbv

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^$', ss_fbv.index),
    # url(r'^index/$', ss_fbv.index),
    # url(r'^show_stream/$', ss_fbv.show_stream),
    # url(r'^stream/add/$', ss_fbv.add_stream),
    # url(r'^stream/del/$', ss_fbv.stop_stream),
    url(r'^$', ss_cbv.index),
    url(r'^index/$', ss_cbv.index),
    url(r'^show_stream/$', ss_cbv.show_stream),
    url(r'^stream/add/$', ss_cbv.StartStream.as_view()),
    url(r'^stream/del/$', ss_cbv.StopStream.as_view()),
    url(r'^page2/$', ss_fbv.page2),
    url(r'^get_log/', ss_fbv.show_log_file),
]
