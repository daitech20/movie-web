# -*- coding: utf-8 -*-
import csv
from io import TextIOWrapper

from core.utils.api_resp import ErrorResponseException


def read_movie_csv(csv_file):
    try:
        csv_file.file.seek(0)
        csv_file_wrapper = TextIOWrapper(csv_file.file, encoding='utf-8')
        csv_reader = csv.reader(csv_file_wrapper)

        movies = []
        for row in csv_reader:
            movies.append({
                "code": row[0],
                "name": row[1],
                "image": row[2],
                "content": row[3],
                "publisher": row[4],
                "year_of_manufacture": row[5],
                "country": row[6],
                "duration": row[7],
                "category": row[8],
                "category_train": None
            })

    except Exception as e:
        raise ErrorResponseException(error=str(e))

    return movies


def read_category_csv(csv_file):
    try:
        csv_file.file.seek(0)
        csv_file_wrapper = TextIOWrapper(csv_file.file, encoding='utf-8')
        csv_reader = csv.reader(csv_file_wrapper)

        categories = []

        for row in csv_reader:
            categories.append({
                "code": row[0],
                "name": row[1],
            })

    except Exception as e:
        raise ErrorResponseException(error=str(e))

    return categories


def read_user_csv(csv_file):
    try:
        csv_file.file.seek(0)
        csv_file_wrapper = TextIOWrapper(csv_file.file, encoding='utf-8')
        csv_reader = csv.reader(csv_file_wrapper)

        users = []

        for row in csv_reader:
            users.append({
                "code": row[0],
                "username": row[1],
                "password": row[2],
                "first_name": row[3],
                "last_name": row[4]
            })

    except Exception as e:
        raise ErrorResponseException(error=str(e))

    return users


def read_comment_csv(csv_file):
    try:
        csv_file.file.seek(0)
        csv_file_wrapper = TextIOWrapper(csv_file.file, encoding='utf-8')
        csv_reader = csv.reader(csv_file_wrapper)

        users = []

        for row in csv_reader:
            users.append({
                "content": row[0],
                "rate": row[1],
                "category": row[2],
                "movie": row[3],
                "user": row[4]
            })

    except Exception as e:
        raise ErrorResponseException(error=str(e))

    return users


def read_keyword_csv(csv_file):
    try:
        csv_file.file.seek(0)
        csv_file_wrapper = TextIOWrapper(csv_file.file, encoding='utf-8')
        csv_reader = csv.reader(csv_file_wrapper)

        keywords = []

        for row in csv_reader:
            keywords.append({
                "code": row[0],
                "name": row[1],
                "point": row[2],
                "category": row[3]
            })

    except Exception as e:
        raise ErrorResponseException(error=str(e))

    return keywords