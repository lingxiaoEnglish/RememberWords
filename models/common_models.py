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
from pydantic import BaseModel

class CommonModel(BaseModel):
    createdAt: int
    updatedAt: int
    url: str
    tags: List[str] = []
    modifiedAt: int = 0
    _id: str = ""
    _objectStore: str = ""

    _user: str = ""
    type: str = ""