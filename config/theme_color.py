# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : theme_color
@Author  : lingxiao
@Date    : 2026-06-03 16:10
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

from enum import Enum

class ThemeColor(Enum):
    """
    统一主题颜色枚举。
    每个成员的值为元组：(浅色哈希值, 深色哈希值)
    """
    window_bg = ("#FFFFFF", "#121212")
    left_panel_bg = ("#F8FAFC", "#1E1E1E")
    right_stack_bg = ("#FFFFFF", "#121212")  # 如果多个枚举成员具有完全相同的值（Value），后声明的成员会被视为先声明成员的“别名（Alias）
    border_color = ("#E2E8F0", "#2D2D2D")
    text_main = ("#1E293B", "#E0E0E0")
    text_muted = ("#64748B", "#A0A0A0")
    nav_item_hover = ("#E2E8F0", "#2C2C2C")
    nav_item_active = ("#3B82F6", "#3B82F6")
    card_bg = ("#FFFFFF", "#1E1E1E")
    cover_bg = ("#F1F5F9", "#252525")

    @classmethod
    def get_theme_dict(cls, is_light_mode: bool = True) -> dict:
        """一键转换为用于 QSS 替换的平铺字典"""
        idx = 0 if is_light_mode else 1
        # 将枚举名转为小写（例如 WINDOW_BG -> 'window_bg'），完美契合你原本的 QSS 规范
        # colors = {color.name: color.value[idx] for color in cls}
        # 遍历 __members__ 从而完整保留 window_bg 和 right_stack_bg
        colors = {name: color.value[idx] for name, color in cls.__members__.items()}
        return colors