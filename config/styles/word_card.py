# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : word_card
@Author  : lingxiao
@Date    : 2026-06-01 16:10
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
from warnings import deprecated


# ... existing code ...
@deprecated("use qss instead")
def get_style(colors: dict) -> str:
    """复习卡片与网络封面的原子样式"""
    is_dark = colors["window_bg"] == "#121212"
    card_bg = "#1E1E1E" if is_dark else "#FFFFFF"
    cover_bg = "#252525" if is_dark else "#F1F5F9"

    return f"""
        /* 核心单张卡片容器 */
        QFrame#WordCard {{
            background-color: {card_bg};
            border: 1px solid {colors["border_color"]};
            border-radius: 12px;
        }}

        /* 封面图标签 */
        QLabel#CardCover {{
            border-top-left-radius: 11px;
            border-top-right-radius: 11px;
            background-color: {cover_bg};
        }}

        /* 补充：单词卡片内部的文本精细微调（可选，利于未来单独调卡片字号） */
        QLabel#CardTag {{
            font-size: 11px;
            color: {colors["nav_item_active"]};
            font-weight: bold;
            background: transparent;
        }}
        QLabel#CardWord {{
            font-size: 18px;
            font-weight: bold;
            color: {colors["text_main"]};
            background: transparent;
        }}
        QLabel#CardNote {{
            font-size: 13px;
            color: {colors["text_muted"]};
            background: transparent;
        }}
    """