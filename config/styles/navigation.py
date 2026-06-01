# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : navigation
@Author  : lingxiao
@Date    : 2026-06-01 16:10
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

def get_style(colors: dict) -> str:
    """导航栏与主侧边栏的原子样式"""
    return f"""
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
    """