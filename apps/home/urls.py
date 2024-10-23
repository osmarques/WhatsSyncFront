# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    path('chat.html', views.chat, name='chat'),
    path('/webhook', views.webhook_receiver, name='webhook_receiver'),
    path('mensagens', views.mensagens, name='mensagens'),
]
