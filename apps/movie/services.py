# -*- coding: utf-8 -*-
import csv
import math
from io import TextIOWrapper

import numpy as np
from django.db.models import Count
from movie.models import Category, Keyword, Movie
from numpy.linalg import norm

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


def get_cmt_film():  # lấy cmt theo phim
    result = []
    movie = Movie.objects.all()
    for item in movie:
        # print(item.code)
        result.append(([item.code,list(item.comment.all())])) # noqa
    return result


def getvecto():  # khởi tạo vector đặc trưng theo thể loại cho phim
    category = Category.objects.all()
    parent_vec = {}
    for item in category:
        keyword = Keyword.objects.filter(category=item)
        char = [x.name for x in keyword]
        char = sorted(char, reverse=True , key=len)
        vec = [dict(zip([ch],[0])) for ch in char] # noqa
        parent_vec[item.name] = vec
    return parent_vec


def cacula_vec(name_movie, film_vec):
    movieTarget = Movie.objects.get(name=name_movie)
    commentSet = list(_ for _ in movieTarget.comment.all())
    # print(commentSet)
    for value_vec in film_vec[name_movie].values():
        for comment in commentSet:
            tmpComment = str(comment)
            for valueItem in value_vec:
                key, value = list(valueItem.items())[0]
                # print(tmpComment, "  ", key, "   ", tmpComment.find(key))
                if tmpComment.find(key) != -1:
                    straight = Keyword.objects.get(name=key)
                    valueItem[key] = straight.point
                    tmpComment = tmpComment.replace(key,"") # noqa
                    # print(tmpComment)
        # print(value_vec)


def dis_cosin(vec_a, vec_b):  # tính độ tương đồng cosin dựa trên vector
    # define two lists or array
    # compute cosine similarity
    A = [list(val.values()) for val in vec_a]
    a = []
    for sub in A:
        a.extend(sub)
    b = []
    B = [list(val.values()) for val in vec_b]
    for sub in B:
        b.extend(sub)
    #
    # print("a", a)
    # print("b", b)
    cosine = np.dot(a, b) / (norm(a) * norm(b))
    return cosine


def caculator_dis(movie_name, film_vec):  # tính độ tương đồng cosin của các phim theo thể loại phim
    result = {}
    for key, val in film_vec[movie_name].items():
        # print("key", key)
        # print("val", val)
        # print("+++++++++++++++++++++++++++++++++++++")
        term = '' # noqa
        value = 0.0
        sublist = []
        for key2, val2 in film_vec.items():
            # print("key2", key2)
            # print("val2", val2)

            for key3, val3 in val2.items():
                if key == key3:
                    item={}
                    # print("key", key)
                    # print("val3", val3)
                    # print("key3", key3)
                    value = dis_cosin(val, val3)
                    # print(value);
                    if not math.isnan(value):
                        item['name']=key2
                        item['value']=value
                        sublist.append(item)
            # sorted(sublist, key=value)# lamf sao ddeer  thêm phần tử item (dict) vào mảng sublist (list)
        result[key]=sublist
    return result



def recommend(film_name):
    # print(getvecto())
    film_vec = {}
    list_name_film = Movie.objects.all()
    for item in list_name_film:
        film_vec[item.name] = getvecto()
    # print(film_vec);
    #     print(film_vec.keys())
        cacula_vec(item.name, film_vec)
    movietmp=Movie.objects.get(name=film_name)
    print(movietmp.category.name)
    predict = caculator_dis(film_name,film_vec)
    tmpList = []
    for key, val in predict.items():
        if key==movietmp.category.name:
            tmpList = val
    resultlist = sorted(tmpList, key=lambda d: d['value'], reverse=True)

    if len(resultlist) > 0:
        movie = Movie.objects.get(name=resultlist[0]['name'])
        return movie
    else:
        return None
    # print(film_vec)


def train_comment_movie(movie_id):
    movie = Movie.objects.get(id=movie_id)
    comments = movie.comment.all()
    category_counts = comments.values('category').annotate(count=Count('category')).order_by('-count')
    most_common_category = category_counts.first()
    movie.category_train = Category.objects.get(id=most_common_category['category'])
    movie.save()

    try:
        second_common_category = category_counts[1]
        if most_common_category['count'] == second_common_category['count']:
            if most_common_category['category'] == movie.category.name:
                movie.category_train = Category.objects.get(id=most_common_category['category'])
            else:
                movie.category_train = Category.objects.get(id=second_common_category['category'])

        movie.save()
    except:
        pass


def search_category(input):
    tmp = getvecto()

    listtmp = []
    for key, val in tmp.items():
        for item in val:
            listtmp.extend(item.keys())
    sorted(listtmp, key=len)
    # print(listtmp)

    for item in listtmp:
        # print("*");
        # print(type(input))
        if input.find(item) != -1:
            ob = Keyword.objects.get(name=item)
            return ob.category.id

#
# def search(input):
#     try:
#         tmp = getvecto()
#         listtmp = []
#         for key, val in tmp.items():
#             for item in val:
#                 listtmp.extend(item.keys())
#         listtmp = sorted(listtmp, key=len, reverse=True)
#
#         value = [0 for i in listtmp]
#         for item in listtmp:
#             if input.find(item) != -1:
#                 ob = Keyword.objects.get(name=item)
#                 value[listtmp.index(item)] = ob.point
#
#         film_vec = {}
#         list_name_film = Movie.objects.all()
#         for item in list_name_film:
#             film_vec[item.name] = getvecto()
#             cacula_vec(item.name, film_vec)
#
#         new_vec = {}
#         for key, val in film_vec.items():
#             lstvalue =[]
#             for key2, val2 in val.items():
#                 lstvalue.extend(val2)
#             lst = sorted(lstvalue, key=lambda x: len(str(x.keys())), reverse=True)
#             new_vec[key] = lst
#         vector_film = {}
#
#         for key, val in new_vec.items():
#             subvec = []
#             for i in val:
#                 subvec.extend(list(i.values()))
#             vector_film[key] = subvec
#         result = {}
#         for key, val in vector_film.items():
#             cosine = np.dot(val, value) / (norm(val) * norm(value))
#             if not math.isnan(cosine):
#                 result[key] = cosine
#
#         final = {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}
#         result = {k: v for k, v in final.items() if v > 0}
#
#         film_name = list(result.keys())
#         return film_name
#     except:
#         return None


def sort_result(list):
    tmp = []
    print("new list")
    for key, val in list.items():
        ob = Movie.objects.get(name=key)
        # print(ob.rate());
        list[key] = ob.rate()
    list = {k: v for k, v in sorted(list.items(), key=lambda item: item[1], reverse=True)}
    result = [k for k, v in list.items()]
    print(list)
    return result



def search(input):
    tmp = getvecto()
    listtmp = []
    for key, val in tmp.items():
        for item in val:
            listtmp.extend(item.keys())
    listtmp = sorted(listtmp, key=len, reverse=True)

    value = [0 for i in listtmp]
    for item in listtmp:
        if input.find(item) != -1:
            ob = Keyword.objects.get(name=item)
            value[listtmp.index(item)] = ob.point

    film_vec = {}
    list_name_film = Movie.objects.all()
    for item in list_name_film:
        film_vec[item.name] = getvecto()
        cacula_vec(item.name, film_vec)

    new_vec = {}
    for key, val in film_vec.items():
        lstvalue =[]
        for key2, val2 in val.items():
            lstvalue.extend(val2)
        lst = sorted(lstvalue, key=lambda x: len(str(x.keys())), reverse=True)
        new_vec[key] = lst
    vector_film = {}

    for key, val in new_vec.items():
        subvec = []
        for i in val:
            subvec.extend(list(i.values()))
        vector_film[key] = subvec
    result = {}
    for key, val in vector_film.items():
        cosine = np.dot(val, value) / (norm(val) * norm(value))
        if (not math.isnan(cosine)) and (cosine > 0):
            result[key] = cosine

    final = {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}
    keyval = {}
    for ob in Category.objects.all():
        keyval[ob.name] = 0
    for k,v in final.items():
        ob = Movie.objects.get(name=k)
        val = keyval[ob.category_train.name]
        val +=1
        keyval[ob.category_train.name] = val

    return_result = []
    keyval = {k: v for k, v in sorted(keyval.items(), key=lambda item: item[1], reverse=True)}
    for key, val in keyval.items():
            filter = {}
            for key2, val2 in final.items():
                ob = Movie.objects.get(name=key2)
                if ob.category_train.name == key:
                    filter.update({key2: val2})
            return_result.extend(sort_result(filter))

    return return_result
    # final result, tìm kiếm phim trả về theo ưu tiên số sao đánh giá của các
    # phim có nhãn xuất hiện nhiều lần dựa theo từ khóa nhập vào. nhãn dựa theo là nhãn được người dùng đánh giá tạo nên
