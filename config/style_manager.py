# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : style_manager
@Author  : lingxiao
@Date    : 2026-06-02 13:39
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
from config.styles_qss import load_qss
# ... existing code ...
class StyleManager:
    @staticmethod
    def load_global_qss() -> str:
        """
        load global qt style sheet
        """
        global_qss = [
            "common",
            "navigation",
            "scroll_bar",
        ]
        # print(global_qss)
        return load_qss(global_qss)

    @staticmethod
    def load_word_card_css() -> str:
        """
        load word card qt style sheet
        """
        qss_str = load_qss(["word_card"])
        # print(qss_str)
        return qss_str