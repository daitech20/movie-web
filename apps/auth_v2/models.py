# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models  # noqa


class User(AbstractUser):
    code = models.IntegerField(unique=True, default=1)
