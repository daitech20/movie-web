# -*- coding: utf-8 -*-
from django.urls import include, path

app_name = 'movie'
urlpatterns = [
    path('api/v1/', include('apps.movie.api')),
]
