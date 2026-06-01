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
from models.mark_models import *
from models.page_models import *
from typing_extensions import List


# ... existing code ...
class WordReviewPage(QWidget):
    def __init__(self):
        super().__init__()
        self.network_manager = QNetworkAccessManager(self)
        self.init_page_ui()

    def reload_cards(self, pages: List[Page], marks: List[Mark]):
        print(f"pages,count {len( pages)}")
        print(f"marks,count {len( marks)}")
        COLUMNS = 4  # 标准三列排布瀑布流
        for index, item in enumerate(pages):

            card = WordCard(page=item,
                            network_manager=self.network_manager)
            row = index // COLUMNS
            col = index % COLUMNS
            self.grid_layout.addWidget(card, row, col)

        # 防止网格拉伸的兜底弹簧
        self.grid_layout.setRowStretch(self.grid_layout.rowCount(), 1)

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



