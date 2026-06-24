# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : preview_header_widget
@Author  : lingxiao
@Date    : 2026-06-24 11:03
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
from PyQt6.QtWidgets import QWidget


class PreviewHeaderWidget(QWidget):
    """
    The header widget of the preview page.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        pass

    def resizeEvent(self, a0):
        """
        Resize event handler.
        """
        super().resizeEvent(a0)
        print(f"{self}--resizeEvent")