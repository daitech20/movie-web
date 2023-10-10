# -*- coding: utf-8 -*-
from core.utils.base_schema import CustomBaseModel


class CommentCreateRequest(CustomBaseModel):
    content: str
    rate: int
    movie: int


class SearchMovieRequest(CustomBaseModel):
    content: str
