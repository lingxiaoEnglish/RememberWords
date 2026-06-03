# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : data_service
@Author  : lingxiao
@Date    : 2026-06-01 11:18
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

# ... existing code ...
import json
import os
from collections import defaultdict
from typing import List, ClassVar, Any, Dict, Optional
from warnings import deprecated

from models.marks_model_deprecated import *
from models.mark_models import *

from models.page_models import *

class DataService:

    # RAW_DATA: ClassVar[dict[str, Any]] = None
    RAW_DATA: ClassVar[Optional[Dict[str, Any]]] = None

    @staticmethod
    def load_pages_from_json(json_path: str, marks: List[Mark] = None) -> List[Page]:
        """
        load raw data via json path
        :param json_path:
        :param marks: all word items
        :return:
        """
        if not DataService.load_raw_data_from_json__(json_path):
            print("Fail to load marks data")
            return []
        bookmarks = DataService.RAW_DATA.get("bookmarks", [])
        if not bookmarks:
            return []

        # 针对大数据量预索引优化
        # 使用 defaultdict(list) 自动处理 key 不存在的情况
        marks_by_bookmark = defaultdict(list)
        if marks:
            for mark in marks:
                marks_by_bookmark[mark.bookmark].append(mark)
                print("")



        bookmarks_datas = []
        for index, item in enumerate(bookmarks):
            try:
                page = Page.model_validate(item)
                page_id = page.id
                page.marks = marks_by_bookmark.get(page_id, [])
                bookmarks_datas.append(page)
            except Exception as e:
                print(f"解析单个 Page 数据失败: {e}, 略过该条数据")
                continue

        # 根据createAt降序
        bookmarks_datas.sort(key=lambda x: x.createdAt, reverse=True)
        return bookmarks_datas


    @staticmethod
    def load_marks_from_json(json_path: str) -> List[Mark]:
        """
        load raw data via json path
        :param json_path:
        :return: marks data sources
        """

        if not DataService.load_raw_data_from_json__(json_path):
            print("Fail to load marks data")
            return []

        marks = DataService.RAW_DATA.get("marks", [])
        mark_datas = []
        for index, item in enumerate(marks):
            mark = Mark.model_validate(item)
            mark_datas.append(mark)

        print(len(mark_datas))
        print("-----")
        return mark_datas



    @staticmethod
    @deprecated("load_marks_from_json instead")
    def load_marks_data_deprecated(json_path: str):
        """
        deprecated function. using load_marks_from_json instead
        :param json_path:
        :return:
        """
        if not DataService.load_raw_data_from_json__(json_path):
            print("Fail to load marks data")
            return

        marks = DataService.RAW_DATA.get("marks", [])
        mark_datas = []
        for index, item in enumerate(marks):

            mark_ele = Marks(createdAt=item['createdAt'],
                             updatedAt=item['updatedAt'],
                             url=item['url'],
                             tags=item["tags"],
                             text=item["text"],
                             type=item["type"],
                             mediaType=item["mediaType"],
                             color=item["color"],
                             highlightSource=HighlightSource(
                                 startMeta=Meta(
                                     parentTagName=item['highlightSource']['startMeta']['parentTagName'],
                                     parentIndex=item['highlightSource']['startMeta']['parentIndex'],
                                     textOffset=item['highlightSource']['startMeta']['textOffset']
                                 ),
                                 endMeta=Meta(
                                     parentTagName=item['highlightSource']['endMeta']['parentTagName'],
                                     parentIndex=item['highlightSource']['endMeta']['parentIndex'],
                                     textOffset=item['highlightSource']['endMeta']['textOffset']
                                 ),
                                 text=item['highlightSource']["text"],
                                 id=item['highlightSource']["id"],
                             ),
                             domElementOffsetTop=item["domElementOffsetTop"],
                             domElementOffsetLeft=item["domElementOffsetLeft"],
                             _bookmark=item["_bookmark"],
                             notes=item.get("notes", ""),
                             modifiedAt=item.get("modifiedAt", 0),
                             _id=item["_id"],
                             _objectStore=item["_objectStore"],
                             _user=item["_user"]
                             )
            mark_datas.append(mark_ele)

        print(len(mark_datas))
        print("-----")


    @staticmethod
    def load_raw_data_from_json__(json_path: str):
        """
        load raw data via json path
        :param json_path:
        :return: True: load data success, otherwise, fail
        """

        if DataService.RAW_DATA:
            return True

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                DataService.RAW_DATA = data
                return True
        except Exception as e:
            DataService.RAW_DATA = None
            print(f"Failed to load data: {e}")
            return False