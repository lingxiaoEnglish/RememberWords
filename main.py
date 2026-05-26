# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : main.py
@Author  : lingxiao
@Date    : 2026-05-26 15:58
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

# ... existing code ...

import sys
import json
import re

from PyQt6.QtWidgets import (QApplication,QWidget, QVBoxLayout,QHBoxLayout,
                             QLabel, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt

class WordReviewApp(QWidget):
    def __init__(self, json_path):
        super().__init__()
        self.setWindowTitle("Review Words")
        self.json_path = json_path

if __name__ == "__main__":
    app = QApplication(sys.argv)

    json_path = "webhighlights-backup-20260425-162910.json"

    window = WordReviewApp(json_path)
    window.show()
    sys.exit(app.exec())


