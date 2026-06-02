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
import platform

# 跨平台安全字体族：优先匹配 Mac/iOS 原生高清字体，Windows 自动降级匹配微软雅黑
# FONT_FAMILY = '"Helvetica Neue", "PingFang SC", "Microsoft YaHei", sans-serif'

def get_platform_font__():
    """根据操作系统动态返回唯一存在的标准高清晰度字体"""
    sys_plat = platform.system()
    if sys_plat == "Windows":
        return "Microsoft YaHei"
    elif sys_plat == "Darwin":  # macOS
        return "Helvetica Neue"
    else:
        return "sans-serif"

FONT_FAMILY = get_platform_font__()

def get_theme_colors() -> dict:
    """动态分析底层操作系统调色板，返回自适应黑白双色变量字典"""
    is_dard_mode = get_appearance_mode__()
    if is_dard_mode:
        # === 暗黑模式核心色值 ===
        return get_dark_model_colors__()
    else:
        # === 浅色模式核心色值 ===
        return get_light_model_colors__()

def get_appearance_mode__() -> bool:
    """获取当前系统外观模式，返回布尔值"""
    style_hints = QGuiApplication.styleHints()
    print(f'style_hints=={style_hints}')
    # 结合底层 Scheme 字符串与调色板物理亮度实现双保险检测
    current_scheme_str = str(style_hints.colorScheme())
    print(f'current_scheme_str=={current_scheme_str}')
    is_dark_scheme = "Dark" in current_scheme_str or getattr(style_hints.colorScheme(), "value", 0) == 2

    window_color = QApplication.palette().window().color()
    is_dark_palette = window_color.lightness() < 128

    if is_dark_scheme or is_dark_palette:
        return True
    else:
        return False


def get_dark_model_colors__() -> dict:
    """get dark model colors"""
    return {
        "window_bg": "#121212",
        "left_panel_bg": "#1E1E1E",
        "right_stack_bg": "#121212",
        "border_color": "#2D2D2D",
        "text_main": "#E0E0E0",
        "text_muted": "#A0A0A0",
        "nav_item_hover": "#2C2C2C",
        "nav_item_active": "#3B82F6",
        "card_bg": "#1E1E1E",
        "cover_bg": "#252525"
    }


def get_light_model_colors__() -> dict:
    """get light model colors"""
    return {
        "window_bg": "#FFFFFF",
        "left_panel_bg": "#F8FAFC",
        "right_stack_bg": "#FFFFFF",
        "border_color": "#E2E8F0",
        "text_main": "#1E293B",
        "text_muted": "#64748B",
        "nav_item_hover": "#E2E8F0",
        "nav_item_active": "#3B82F6",
        "card_bg": "#FFFFFF",
        "cover_bg": "#F1F5F9"
    }
