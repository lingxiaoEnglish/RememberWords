# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : preview_page
@Author  : lingxiao
@Date    : 2026-06-03 13:24
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from models.mark_models import Mark
from models.page_models import Page


class PreviewPage(QWidget):
    def __init__(self, page: Page, mark: Mark):
        super().__init__()
        self.page = page
        self.mark = mark
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title_label = QLabel(self.page.title)
        layout.addWidget(title_label)