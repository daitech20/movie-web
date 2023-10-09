# -*- coding: utf-8 -*-
from typing import Any

from rest_framework.exceptions import APIException
from rest_framework.response import Response


def make_api_response(
    success: int = 1,
    data: Any = None,
    http_status: int = 200,
    **kwargs
):
    payloads = {
        'success': 1,
        'data': data
    }
    return Response(status=http_status, data=payloads)


def success_api_resp(
    data: Any,
    success: int = 1,
    **kwargs
):

    return make_api_response(success, data, **kwargs)


class ErrorResponseException(APIException):
    status_code = 200

    def __init__(self, success: int = 0, error: Any = "error"):
        self.detail = error
        self.success = success
        super().__init__(error, self.status_code)


def custom_exception_handler(exc, context):
    response_data = {
        "success": 0,
        "error": exc.detail
    }
    response = Response(response_data, status=exc.status_code)

    return response
