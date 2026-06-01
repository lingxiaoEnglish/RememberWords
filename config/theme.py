# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : theme
@Author  : lingxiao
@Date    : 2026-06-01 16:09
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