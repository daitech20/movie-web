# -*- coding: utf-8 -*-
from datetime import date, datetime

from django.db.models.fields.files import ImageFieldFile


def object_to_dict(obj):
    if not obj:
        return None

    object_dict = {}
    for field in obj._meta.fields:
        field_name = field.name
        field_value = getattr(obj, field_name)

        if isinstance(field_value, datetime):
            field_value = field_value.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(field_value, date):
            field_value = field_value.strftime('%Y-%m-%d')
        if isinstance(field_value, ImageFieldFile):
            field_value = field_value.url

        if not field_name.startswith('_'):
            object_dict[field_name] = field_value

    return object_dict
