# -*- coding: utf-8 -*-
from django.urls import path  # noqa
from movie.api import views

urlpatterns = [
    path('list-movie', views.MovieList.as_view(), name='list_movie'),
    path('get-movie/<int:code>', views.MovieDetail.as_view(), name='list_movie'),
    path('import-category-csv', views.import_category_csv, name='import_category_csv'),
    path('import-movie-csv', views.import_movie_csv, name='import_movie_csv'),
    path('import-user-csv', views.import_user_csv, name='import_user_csv'),
    path('import-comment-csv', views.import_comment_csv, name='import_comment_csv'),
    path('create-comment', views.create_comment, name='create_comment'),
    path('train-comment', views.train_comment, name='train_comment'),
    path('search-movie', views.search_movie, name='search_movie'),
    path('import-keyword-csv', views.import_keyword_csv, name='import_keyword_csv'),
]
