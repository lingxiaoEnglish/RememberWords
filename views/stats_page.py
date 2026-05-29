# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : stats_page
@Author  : lingxiao
@Date    : 2026-05-29 16:50
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

# ... existing code ...
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class StatisticsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("📊 学习统计 视图\n\n[子视图待开发：未来在此放置饼图、柱状图或打卡日历]")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 16px; color: #7F8C8D;")
        layout.addWidget(label)