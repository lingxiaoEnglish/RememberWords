# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : review_page
@Author  : lingxiao
@Date    : 2026-05-29 16:50
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
import json
import os

from PyQt6.QtNetwork import QNetworkAccessManager
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout
from PyQt6.QtCore import Qt

from views.word_card import WordCard


# ... existing code ...
class WordReviewPage(QWidget):
    def __init__(self):
        super().__init__()
        # layout = QVBoxLayout(self)
        # label = QLabel("🔥 今日复习 视图\n\n[子视图待开发：未来在此放置单词卡片、封面图、控制按钮等]")
        # label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # label.setStyleSheet("font-size: 16px; color: #7F8C8D; line-height: 1.5;")
        # layout.addWidget(label)
        self.network_manager = QNetworkAccessManager(self)
        self.init_page_ui()
        self.load_cards_from_json()

    def init_page_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(15)

        title_label = QLabel("🔥 今日复习卡片墙")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; background: transparent;")
        main_layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setObjectName("ReviewScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        scroll_content.setObjectName("ScrollContent")

        self.grid_layout = QGridLayout(scroll_content)
        self.grid_layout.setContentsMargins(5, 5, 5, 5)
        self.grid_layout.setSpacing(18)

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

    def load_cards_from_json(self):
        # json_path = "../webhighlights-backup-20260529-135026.json"
        json_path = "/Users/lingxiao/.personal/english/RememberWords/webhighlights-backup-20260529-135026.json"
        bookmarks = []


        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                bookmarks = data.get("bookmarks", [])
        else:
            print(f"JSON file '{json_path}' does not exist.")

        COLUMNS = 4  # 标准三列排布瀑布流
        for index, item in enumerate(bookmarks):
            meta = item.get("meta")
            image = meta.get("image")
            image_url = image.get("url")
            title = item.get("title")
            highlights = "10"
            notes = "5"
            source_url = item.get("origin")
            create_time = item.get("createdAt")
            card = WordCard(img_url=image_url,
                            title=title,
                            highlights=highlights,
                            notes=notes,
                            source_url=source_url,
                            create_time=create_time,
                            network_manager=self.network_manager)

            row = index // COLUMNS
            col = index % COLUMNS
            self.grid_layout.addWidget(card, row, col)

        # 防止网格拉伸的兜底弹簧
        self.grid_layout.setRowStretch(self.grid_layout.rowCount(), 1)



