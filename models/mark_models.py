# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : mark_models
@Author  : lingxiao
@Date    : 2026-06-01 13:32
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

# ... existing code ...
from typing import List
from pydantic import BaseModel
from .common_models import CommonModel

class Meta(BaseModel):
    parentTagName: str
    parentIndex: int
    textOffset: int

class HighlightSource(BaseModel):
    startMeta: Meta
    endMeta: Meta
    text: str
    id: str

class Mark(CommonModel):


    text: str = ""

    mediaType: str = ""
    color: str = ""

    highlightSource: HighlightSource = None
    domElementOffsetTop: int = 0
    domElementOffsetLeft: int = 0
    _bookmark: str = ""

    notes: str = ""

