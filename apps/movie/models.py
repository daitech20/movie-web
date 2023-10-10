# -*- coding: utf-8 -*-
from auth_v2.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.utils.django_base_models import BaseModel

# Create your models here.


class Category(BaseModel):
    name = models.CharField(max_length=50)
    code = models.IntegerField(unique=True)

    def __str__(self) -> str:
        return self.name


class Keyword(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    point = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)],)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="keywords_category")

    def __str__(self) -> str:
        return self.name


class Comment(BaseModel):
    content = models.CharField(max_length=255)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='comments_category', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_user")

    def __str__(self) -> str:
        return self.content


class Movie(BaseModel):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True, blank=True)
    content = models.CharField(max_length=255)
    publisher = models.CharField(max_length=50)
    year_of_manufacture = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    duration = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='movies_category')
    category_train = models.ForeignKey(Category, on_delete=models.CASCADE,
                                       related_name='movies_category_train', null=True, blank=True)
    comment = models.ManyToManyField(Comment, related_name="movies_comment", blank=True)

    def __str__(self) -> str:
        return self.name
