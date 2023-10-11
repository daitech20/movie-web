# -*- coding: utf-8 -*-
from auth_v2.models import User
from django.db import transaction as trans
from django.views.decorators.csrf import csrf_exempt
from movie.api.schemas import CommentCreateRequest, SearchMovieRequest
from movie.api.serializers import MovieListSerializer, MovieSerializer
from movie.models import Category, Comment, Keyword, Movie
from movie.services import (read_category_csv, read_comment_csv,
                            read_keyword_csv, read_movie_csv, read_user_csv,
                            recommend, train_comment_movie)
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from core.utils.api_req import parse_pydantic_obj
from core.utils.api_resp import ErrorResponseException, success_api_resp
from core.utils.services import object_to_dict


class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return success_api_resp(data=serializer.data)


class MovieDetail(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_fields = ['code']

    def retrieve(self, request, code):
        try:
            instance = Movie.objects.get(code=code)
            serializer = self.get_serializer(instance)

            return success_api_resp(data=serializer.data)
        except Exception as e:
            raise ErrorResponseException(error=str(e))


@api_view(('POST',))
@permission_classes([])
@csrf_exempt
def import_category_csv(request):
    if not request.FILES.get('csv_file'):
        raise ErrorResponseException(error="Không đọc được file")

    csv_file = request.FILES['csv_file']
    categories = read_category_csv(csv_file)

    for category in categories:
        category_code = category.get("code")
        check_category = Category.objects.filter(code=category_code).first()

        # check exist student
        if not check_category:
            new_category = Category.objects.create(
                code=category_code,
                name=category.get("name")
            )
            new_category.save()

    return success_api_resp(data=[])


@api_view(('POST',))
@permission_classes([])
@csrf_exempt
def import_movie_csv(request):
    if not request.FILES.get('csv_file'):
        raise ErrorResponseException(error="Không đọc được file")

    csv_file = request.FILES['csv_file']
    movies = read_movie_csv(csv_file)

    for movie in movies:
        movie_code = movie.get("code")
        check_movie = Movie.objects.filter(code=movie_code).first()

        # check exist student
        if not check_movie:
            new_movie = Movie.objects.create(
                code=movie_code,
                name=movie.get("name"),
                image=movie.get("image"),
                content=movie.get("content"),
                publisher=movie.get("publisher"),
                year_of_manufacture=movie.get("year_of_manufacture"),
                country=movie.get("country"),
                duration=movie.get("duration"),
                category=Category.objects.get(code=int(movie.get("category"))),
                category_train=None
            )
            new_movie.save()

    return success_api_resp(data=[])


@api_view(('POST',))
@permission_classes([])
@csrf_exempt
def import_user_csv(request):
    if not request.FILES.get('csv_file'):
        raise ErrorResponseException(error="Không đọc được file")

    csv_file = request.FILES['csv_file']
    users = read_user_csv(csv_file)

    for user in users:
        username = user.get("username")
        check_user = User.objects.filter(username=username).first()

        # check exist student
        if not check_user:
            new_user = User.objects.create(
                code=user.get("code"),
                username=username,
                first_name=user.get("first_name"),
                last_name=user.get("last_name")
            )
            new_user.set_password(user.get("password"))
            new_user.save()

    return success_api_resp(data=[])


@api_view(('POST',))
@permission_classes([IsAuthenticated])
@csrf_exempt
def create_comment(request):
    rdata = parse_pydantic_obj(CommentCreateRequest, request.data)
    try:
        if request.user.is_anonymous:
            user = None
        else:
            user = request.user
        category = Category.objects.get(code=rdata.category)
        comment = Comment.objects.create(
            content=rdata.content,
            rate=rdata.rate,
            user=user,
            category=category
        )
        movie = Movie.objects.get(code=rdata.movie)
        movie.comment.add(comment)

        data = object_to_dict(comment)
        data['category'] = object_to_dict(data['category'])
        data['user'] = comment.user.code

        return success_api_resp(data=data)

    except Exception as e:
        raise ErrorResponseException(error=str(e))


@api_view(('POST',))
@permission_classes([])
@csrf_exempt
def import_comment_csv(request):
    if not request.FILES.get('csv_file'):
        raise ErrorResponseException(error="Không đọc được file")

    csv_file = request.FILES['csv_file']
    comments = read_comment_csv(csv_file)
    with trans.atomic():
        for comment in comments:
            new_comment = Comment.objects.create(
                content=comment.get('content'),
                rate=comment.get('rate'),
                category=Category.objects.get(code=int(comment.get("category"))),
                user=User.objects.get(code=int(comment.get("user")))
            )
            new_comment.save()
            movie = Movie.objects.get(code=int(comment.get('movie')))
            movie.comment.add(new_comment)
            movie.save()

        return success_api_resp(data=[])


@api_view(('GET',))
@permission_classes([])
@csrf_exempt
def train_comment(request):
    try:
        # function train comment
        for movie in Movie.objects.filter():
            train_comment_movie(movie.id)

        return success_api_resp(data=[])
    except Exception as e:
        raise ErrorResponseException(error=str(e))


@api_view(('POST',))
@permission_classes([])
@csrf_exempt
def search_movie(request):
    rdata = parse_pydantic_obj(SearchMovieRequest, request.data)
    try:
        content = rdata.content
        movie = recommend(content)
        if movie:
            movie_data = object_to_dict(movie)
            movie_data['category'] = object_to_dict(movie_data['category'])
            movie_data['category_train'] = object_to_dict(movie_data['category_train'])
            movie_data['comment'] = []
            return success_api_resp(data=movie_data)
        else:
            return success_api_resp(data=[])
    except Exception as e:
        raise ErrorResponseException(error=str(e))


@api_view(('POST',))
@permission_classes([])
@csrf_exempt
def import_keyword_csv(request):
    if not request.FILES.get('csv_file'):
        raise ErrorResponseException(error="Không đọc được file")

    csv_file = request.FILES['csv_file']
    keywords = read_keyword_csv(csv_file)
    with trans.atomic():
        for code, keyword in enumerate(keywords):
            keyword_name = keyword.get("name")
            check_keyword = Keyword.objects.filter(name=keyword_name).first()

            # check exist keyword
            if not check_keyword:
                new_keyword = Keyword.objects.create(
                    code=code+1,
                    name=keyword_name,
                    point=keyword.get('point'),
                    category=Category.objects.get(code=int(keyword.get("category")))
                )
                new_keyword.save()

        return success_api_resp(data=[])
