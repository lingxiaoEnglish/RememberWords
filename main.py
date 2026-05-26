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

        self.words_list = []
        self.current_index = 0

        self.load_data()
        self.init_ui()

    def init_ui(self):
        pass

    def load_data(self):
        """
        prase json file
        """
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            marks = data.get('marks', [])
            for mark in marks:
                word = mark.get('text', '')
                notes_html = mark.get('notes', '')

                # clean html
                notes_text = self.clean_html__(notes_html) if notes_html else 'Empty Word'
                if word:
                    self.words_list.append({
                        'word': word,
                        'notes': notes_text
                    })

            print(f"total words number:{len(self.words_list)}")

        except Exception as e:
            print(f"Failed to load data: {e}")
            # QMessageBox.critical(self, "Error", f"Failed to load data: {e}")
            # return

    def clean_html__(self, html_str):
        """
        clean html simply:
        """
        # 将 <br> 或 </p><p> 替换为换行符
        html_str = re.sub(r'<br\s*/?>|</p>\s*<p>', '\n', html_str)
        # 去除其他所有HTML标签
        clean_text = re.compile('<.*?>')
        text = re.sub(clean_text, '', html_str)
        # 解码常见的HTML实体字符
        text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
        return text.strip()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    json_path = "webhighlights-backup-20260425-162910.json"

    window = WordReviewApp(json_path)
    window.show()
    sys.exit(app.exec())


