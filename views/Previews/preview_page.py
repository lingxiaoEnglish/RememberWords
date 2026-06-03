# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : preview_page
@Author  : lingxiao
@Date    : 2026-06-03 13:24
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from models.mark_models import Mark
from models.page_models import Page


class PreviewPage(QWidget):

    signal_close = pyqtSignal()

    def __init__(self, page: Page, mark: Mark):
        super().__init__()
        self.page = page
        self.mark = mark
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 2. 顶部工具栏加一个关闭按钮
        top_bar = QHBoxLayout()
        close_btn = QPushButton("❌ Close Preview")
        close_btn.setFixedWidth(120)
        # 点击按钮时触发自定义信号
        close_btn.clicked.connect(self.signal_close.emit)
        top_bar.addStretch()
        top_bar.addWidget(close_btn)
        layout.addLayout(top_bar)

        title_label = QLabel(self.page.title)
        layout.addWidget(title_label)
