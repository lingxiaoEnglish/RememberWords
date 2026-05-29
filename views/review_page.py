# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : review_page
@Author  : lingxiao
@Date    : 2026-05-29 16:50
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
# ... existing code ...
class WordReviewPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("🔥 今日复习 视图\n\n[子视图待开发：未来在此放置单词卡片、封面图、控制按钮等]")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 16px; color: #7F8C8D; line-height: 1.5;")
        layout.addWidget(label)