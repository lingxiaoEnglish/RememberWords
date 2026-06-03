# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : app
@Author  : lingxiao
@Date    : 2026-05-29 14:29
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

# ... existing code ...
import sys
from PyQt6.QtWidgets import QApplication
from views.AppWindow import AppWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow(json_path="webhighlights-backup-20260529-135026.json")
    window.show()
    sys.exit(app.exec())


