# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : word_models
@Author  : lingxiao
@Date    : 2026-06-01 10:51
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

from dataclasses import dataclass, field
# dataclass: A decorator that automatically generates special methods for classes
# field: A decorator that specifies the default value for a field


from typing import List, Optional

@dataclass
class Meta:
    parentTagName: str
    parentIndex: int
    textOffset:  int

@dataclass
class HighlightSource:
    startMeta: Meta
    endMeta: Meta
    text: str
    id: str

@dataclass
class Marks:
    createdAt: int
    updatedAt: int
    url: str
    tags: List[str] = field(default_factory=list)

    text: str = ""
    type: str = ""
    mediaType: str = ""
    color: str = ""

    highlightSource: Optional[HighlightSource] = None

    domElementOffsetTop: int = 0
    domElementOffsetLeft: int = 0
    _bookmark: str = ""
    notes: str = ""
    modifiedAt: int = 0
    _id: str = ""
    _objectStore: str = ""
    _user: str = ""



