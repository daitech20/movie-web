# -*- coding: utf-8 -*-
from django.urls import include, path

app_name = 'auth_v2'
urlpatterns = [
    path('api/v1/', include('apps.auth_v2.api')),
]
