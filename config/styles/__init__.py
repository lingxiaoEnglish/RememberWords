# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : __init__.py
@Author  : lingxiao
@Date    : 2026-06-01 16:09
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

from config.theme import get_theme_colors

# 💡 核心设计：在这里注册所有已经拆分好的子组件样式模块
from config.styles import base
from config.styles import navigation
from config.styles import word_card


def generate_qss() -> str:
    """
    整合器核心：动态获取当前系统颜色，
    并把所有解耦的子控件样式表拼接在一起，形成最终的全局样式。
    """
    colors = get_theme_colors()

    # 样式切片收集桶
    style_pieces = [
        base.get_style(colors),
        navigation.get_style(colors),
        word_card.get_style(colors)
        # 未来如果新增了统计、设置等子控件，直接在这追加即可：
        # stats_page.get_style(colors)
    ]

    # 将所有样式切片平滑合并为一个超大字符串返回
    return "\n".join(style_pieces)