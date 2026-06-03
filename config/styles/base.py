# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : base
@Author  : lingxiao
@Date    : 2026-06-01 16:10
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
from warnings import deprecated

# ... existing code ...
from config.theme import FONT_FAMILY
@deprecated("using qss instead")
def get_style(colors: dict) -> str:
    """全局最基础的原子样式"""
    return f"""
        QWidget {{
            font-family: {FONT_FAMILY};
            background-color: {colors["window_bg"]};
            color: {colors["text_main"]};
        }}
        QSplitter::handle {{
            background-color: {colors["border_color"]};
        }}
    """