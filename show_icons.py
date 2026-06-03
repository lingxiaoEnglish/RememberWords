# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : show_icons
@Author  : lingxiao
@Date    : 2026-06-03 15:24
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

# show_icons.py
import sys
from PyQt6.QtWidgets import QApplication
from qtawesome.icon_browser import IconBrowser


def main():
    app = QApplication(sys.argv)

    # 🌟 实例化组件并展示
    browser = IconBrowser()
    browser.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()