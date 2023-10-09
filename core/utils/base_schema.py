# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel


class CustomBaseModel(BaseModel):

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
        json_decoders = {
            datetime: lambda v: datetime.fromisoformat(v),
        }
