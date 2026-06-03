# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : review_page
@Author  : lingxiao
@Date    : 2026-05-29 16:50
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
from PyQt6.QtNetwork import QNetworkAccessManager
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal

from views.Pages.word_card import WordCard
from models.mark_models import *
from models.page_models import *
from typing_extensions import List


# ... existing code ...
class WordReviewPage(QWidget):

    signal_clicked = pyqtSignal(Page)

    def __init__(self):
        super().__init__()
        self.network_manager = QNetworkAccessManager(self)
        self.init_page_ui()

    def reload_cards(self, pages: List[Page]):
        self._clear_cards()
        COLUMNS = 4  # 标准三列排布瀑布流
        for index, item in enumerate(pages):

            card = WordCard(page=item,
                            network_manager=self.network_manager)
            card.signal_clicked.connect(self.signal_clicked.emit) # noqa
            row = index // COLUMNS
            col = index % COLUMNS
            self.grid_layout.addWidget(card, row, col)

        # 防止网格拉伸的兜底弹簧
        self.grid_layout.setRowStretch(self.grid_layout.rowCount(), 1)

    def _clear_cards(self):
        # 倒序遍历，安全抽离
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.takeAt(i)  # takeAt 会把条目直接从布局中彻底移除
            if item:
                widget = item.widget()
                if widget:  # 确保是控件后再处理
                    # 显式断开所有信号连接，防止内存泄漏
                    try:
                        widget.signal_clicked.disconnect()  # noqa
                    except (TypeError, RuntimeError):
                        pass

                    widget.setParent(None)
                    widget.deleteLater()  # 异步销毁内存

    def init_page_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(15)

        title_label = QLabel("🔥 Page Lists")
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



