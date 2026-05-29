# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : styles.py
@Author  : lingxiao
@Date    : 2026-05-29 16:50
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication

# 跨平台安全字体族：优先匹配 Mac/iOS 原生高清字体，Windows 自动降级匹配微软雅黑
FONT_FAMILY = '"Helvetica Neue", "PingFang SC", "Microsoft YaHei", sans-serif'


def get_theme_colors() -> dict:
    """动态分析底层操作系统调色板，返回自适应黑白双色变量字典"""
    style_hints = QGuiApplication.styleHints()

    # 结合底层 Scheme 字符串与调色板物理亮度实现双保险检测
    current_scheme_str = str(style_hints.colorScheme())
    is_dark_scheme = "Dark" in current_scheme_str or getattr(style_hints.colorScheme(), "value", 0) == 2

    window_color = QApplication.palette().window().color()
    is_dark_palette = window_color.lightness() < 128

    if is_dark_scheme or is_dark_palette:
        # === 暗黑模式核心色值 ===
        return {
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
        # === 浅色模式核心色值 ===
        return {
            "window_bg": "#FFFFFF",
            "left_panel_bg": "#F8FAFC",
            "right_stack_bg": "#FFFFFF",
            "border_color": "#E2E8F0",
            "text_main": "#1E293B",
            "text_muted": "#64748B",
            "nav_item_hover": "#E2E8F0",
            "nav_item_active": "#3B82F6",
        }


def generate_qss() -> str:
    """整合字体、颜色与 QSS 骨架，输出标准样式表"""
    colors = get_theme_colors()

    return f"""
        QWidget {{
            font-family: {FONT_FAMILY};
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