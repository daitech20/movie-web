# -*- coding: utf-8 -*-
from .api_resp import ErrorResponseException


def parse_pydantic_obj(parser, data):
    try:
        return parser.parse_obj(data)
    except Exception as e:
        raise ErrorResponseException(error=e.errors())
