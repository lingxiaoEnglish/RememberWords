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

class WordReviewPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("🔥 今日复习 视图\n\n[子视图待开发：未来在此放置单词卡片、封面图、控制按钮等]")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 16px; color: #7F8C8D; line-height: 1.5;")
        layout.addWidget(label)

class StatisticsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("📊 学习统计 视图\n\n[子视图待开发：未来在此放置饼图、柱状图或打卡日历]")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 16px; color: #7F8C8D;")
        layout.addWidget(label)

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("⚙️ 设置 视图\n\n[子视图待开发：未来在此放置设置项]")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 16px; color: #7F8C8D;")
        layout.addWidget(label)


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.nav_list = None
        self.right_stack = None
        self.page_review = None
        self.page_stats = None
        self.page_settings = None
        self.init_ui()

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
        self.setWindowTitle("智能背单词系统")
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
        """核心修复：通过状态值判断，避免直接依赖 QColorScheme 类"""
        style_hints = QGuiApplication.styleHints()

        # Qt 内部机制中:
        # colorScheme().value 值为 2 或者通过强转枚举名包含 'Dark' 均代表暗黑模式
        # 这种写法完美避开了老版本 PyQt6 没有 QColorScheme 的问题
        current_scheme_str = str(style_hints.colorScheme())
        is_dark = "Dark" in current_scheme_str or getattr(style_hints.colorScheme(), "value", 0) == 2

        if is_dark:
            # 暗黑模式色彩变量
            colors = {
                "window_bg": "#121212",
                "left_panel_bg": "#1E1E1E",
                "right_stack_bg": "#121212",
                "border_color": "#2D2D2D",
                "text_main": "#E0E0E0",
                "text_muted": "#A0A0A0",
                "nav_item_hover": "#2C2C2C",
                "nav_item_active": "#3B82F6",
            }
        else:
            # 浅色模式色彩变量
            colors = {
                "window_bg": "#FFFFFF",
                "left_panel_bg": "#F8FAFC",
                "right_stack_bg": "#FFFFFF",
                "border_color": "#E2E8F0",
                "text_main": "#1E293B",
                "text_muted": "#64748B",
                "nav_item_hover": "#E2E8F0",
                "nav_item_active": "#3B82F6",
            }

        # 动态组装并渲染全局样式
        style_sheet = f"""
            QWidget {{
                font-family: "Helvetica Neue", "PingFang SC", "Microsoft YaHei", sans-serif;
                background-color: {colors["window_bg"]};
                color: {colors["text_main"]};
            }}
            QWidget#LeftPanel {{
                background-color: {colors["left_panel_bg"]};
            }}
            QLabel#LogoLabel {{
                font-size: 20px;
                font-weight: bold;
                color: {colors["text_main"]};
                margin-bottom: 20px;
                padding-left: 8px;
                background-color: transparent;
            }}
            QListWidget#NavList {{
                border: none;
                background-color: transparent;
            }}
            QListWidget#NavList::item {{
                padding: 12px 16px;
                font-size: 14px;
                color: {colors["text_muted"]};
                border-radius: 6px;
                margin-bottom: 6px;
                background-color: transparent;
            }}
            QListWidget#NavList::item:hover {{
                background-color: {colors["nav_item_hover"]};
                color: {colors["text_main"]};
            }}
            QListWidget#NavList::item:selected {{
                background-color: {colors["nav_item_active"]};
                color: #FFFFFF;
                font-weight: bold;
            }}
            QStackedWidget#RightStack {{
                background-color: {colors["right_stack_bg"]};
                border-left: 1px solid {colors["border_color"]};
            }}
            QStackedWidget#RightStack QLabel {{
                color: {colors["text_muted"]};
                background-color: transparent;
            }}
            QSplitter::handle {{
                background-color: {colors["border_color"]};
            }}
        """
        self.setStyleSheet(style_sheet)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())


