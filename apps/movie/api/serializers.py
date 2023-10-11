# -*- coding: utf-8 -*-
from auth_v2.models import User
from movie.models import Category, Comment, Movie
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "code", "username", "first_name", "last_name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    comment = CommentSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'code', 'name', 'image', 'category', 'comment']


class MovieSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True)
    category = CategorySerializer()
    category_train = CategorySerializer()

    class Meta:
        model = Movie
        fields = '__all__'
