# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : page_models
@Author  : lingxiao
@Date    : 2026-06-01 13:50
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
from typing import List, Optional
from pydantic import BaseModel
from .common_models import CommonModel
from .marks_model_deprecated import Marks

class PageMetaImg(BaseModel):
    url: str = ""
    width: Optional[int] = 0
    height: Optional[int] = 0

class PageMeta(BaseModel):
    title: str = ""
    description: str = ""
    image: PageMetaImg = None
    url: str = ""
    type: str = ""
    authorUrl: str = ""
    publishedTime: str = ""

class Page(CommonModel):
    title: str = ""
    origin: str = ""
    language: str = ""
    permission: str = ""
    isStarred: bool = False
    meta: Optional[PageMeta] = None
    marks: Optional[List[Marks]] = None

