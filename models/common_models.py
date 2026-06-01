# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : common_models
@Author  : lingxiao
@Date    : 2026-06-01 13:53
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

# ... existing code ...
from typing import List
from pydantic import BaseModel, Field, computed_field
from datetime import datetime

class CommonModel(BaseModel):
    createdAt: int
    updatedAt: int
    url: str
    tags: List[str] = Field(default_factory=list)
    modifiedAt: int = 0
    _id: str = ""
    _objectStore: str = ""

    _user: str = ""
    type: str = ""

    @staticmethod
    def format_timestamp(ts: int) -> str:
        return datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")

    @computed_field
    @property
    def created_date(self) -> str:
        return self.format_timestamp(self.createdAt)

    @computed_field
    @property
    def updated_date(self) -> str:
        return self.format_timestamp(self.updatedAt)

    @computed_field
    @property
    def modified_date(self) -> str:
        return self.format_timestamp(self.modifiedAt)