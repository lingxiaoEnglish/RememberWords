# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : app
@Author  : lingxiao
@Date    : 2026-05-29 14:29
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

# ... existing code ...
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QListWidget,
                             QStackedWidget, QSplitter)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication



# 导入自定义解耦模块
from config.styles import generate_qss
from views.review_page import WordReviewPage
from views.stats_page import StatisticsPage
from views.settings_page import SettingsPage

from services.data_service import DataService

class AppWindow(QWidget):
    def __init__(self, json_path):
        super().__init__()
        self.nav_list = None
        self.right_stack = None
        self.page_review = None
        self.page_stats = None
        self.page_settings = None
        self.json_path = json_path
        # pages 数据源
        self.pages = None
        # total marks 数据源
        self.marks = None


        self.init_ui()
        self.load_data()

    def load_data(self):
        self.marks = DataService.load_marks_from_json(self.json_path)
        self.pages = DataService.load_pages_from_json(self.json_path)
        self.page_review.reload_cards(self.pages, self.marks)

    def switch_page(self, index):
        """核心路由控制：当左侧点击了第几项，右侧就切到对应的子视图"""
        if index < self.right_stack.count():
            self.right_stack.setCurrentIndex(index)

    def init_theme_listener(self):
        """主题切换监听"""
        style_hints = QGuiApplication.styleHints()
        style_hints.colorSchemeChanged.connect(self.on_system_theme_changed)

    def on_system_theme_changed(self, scheme):
        """当系统切主题时的响应"""
        self.apply_auto_theme()

    def init_ui(self):
        self.setWindowTitle("ZhiZhi")
        # self.resize(900, 600)
        self.setMinimumSize(900, 500)

        # 使用 QSplitter 实现侧边栏和主视图
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        # 分界线
        # main_splitter.setHandleWidth(1)

        # 左侧导航面板
        left_panel = QWidget()
        left_panel.setObjectName("LeftPanel") # 用于QSS样式绑定

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(12, 25, 12, 25)

        logo_label = QLabel("📋 Lenthew")
        logo_label.setObjectName("LogoLabel")
        left_layout.addWidget(logo_label)

        # 导航菜单
        self.nav_list = QListWidget()
        self.nav_list.setObjectName("NavList")
        self.nav_list.addItem("🔥 Review")
        self.nav_list.addItems(["📊 Statistics", "⚙️ General"])
        self.nav_list.setCurrentRow(0) # 默认高亮选中第一项
        left_layout.addWidget(self.nav_list)
        self.nav_list.currentRowChanged.connect(self.switch_page)


        # 右侧
        self.right_stack = QStackedWidget()
        self.right_stack.setObjectName("RightStack")

        self.page_review = WordReviewPage()
        self.page_stats = StatisticsPage()
        self.page_settings = SettingsPage()
        self.right_stack.addWidget(self.page_review)
        self.right_stack.addWidget(self.page_stats)
        self.right_stack.addWidget(self.page_settings)

        # 组装
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(self.right_stack)

        # 关键参数: 设置左右分栏初始宽度比例(180px : 720px)
        main_splitter.setSizes([180, 720])
        # 防止左右两侧被完全折叠
        main_splitter.setCollapsible(0, False)
        main_splitter.setCollapsible(1, False)

        # 将整体的分裂器放入最外层的主布局中
        window_layout = QHBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)  # 撑满整个窗口边缘
        window_layout.addWidget(main_splitter)

        self.apply_auto_theme()

    def apply_auto_theme(self):
        qss_str = generate_qss()
        self.setStyleSheet(qss_str)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow(json_path="webhighlights-backup-20260529-135026.json")
    window.show()
    sys.exit(app.exec())


