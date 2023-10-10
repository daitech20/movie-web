# -*- coding: utf-8 -*-
from django.urls import path

from .views import (CustomTokenRefreshView, MyTokenObtainPairView,
                    RegisterView, UserDetail, UserList)

urlpatterns = [
    path('login', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='register'),
    path('list-user', UserList.as_view(), name="list_user"),
    path('get-user/<int:id>', UserDetail.as_view(), name='get_user'),
]
