# -*- coding: utf-8 -*-
from django.contrib import admin
from movie.models import Category, Comment, Keyword, Movie

# Register your models here.


admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Keyword)
