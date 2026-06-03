# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : preview_page
@Author  : lingxiao
@Date    : 2026-06-03 13:24
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from models.page_models import Page
import qtawesome as qta


class PreviewPage(QWidget):

    signal_close = pyqtSignal()

    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # 2. 顶部工具栏加一个关闭按钮
        top_bar = QHBoxLayout()
        close_btn = QPushButton()
        close_btn.setObjectName("CloseBtn")
        close_btn.setIcon(qta.icon("mdi.close"))
        close_btn.setIconSize(QSize(20, 20))
        # 点击按钮时触发自定义信号
        close_btn.clicked.connect(self.signal_close.emit) # noqa
        top_bar.addStretch()
        top_bar.addWidget(close_btn)
        layout.addLayout(top_bar)

        title_label = QLabel(self.page.title)
        layout.addWidget(title_label)
