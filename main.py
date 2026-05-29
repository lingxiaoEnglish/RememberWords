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
        self.json_path = json_path

        self.words_list = []
        self.current_index = 0

        self.load_data()
        self.init_ui()

    def toggle_notes(self):
        """toggle notes"""
        """切换显示/隐藏释义"""
        if self.notes_label.isHidden():
            self.notes_label.show()
            self.show_btn.setText("隐藏释义")
            self.show_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #E67E22; color: white; border-radius: 5px;")
        else:
            self.notes_label.hide()
            self.show_btn.setText("显示释义")
            self.show_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #3498DB; color: white; border-radius: 5px;")

    def prev_word(self):
        """previous word"""
        if self.words_list:
            self.current_index = (self.current_index - 1) % len(self.words_list)
            self.update_card()

    def next_word(self):
        """next word"""
        if self.words_list:
            self.current_index = (self.current_index + 1) % len(self.words_list)
            self.update_card()

    def update_card(self):
        """update card"""
        if not self.words_list:
            self.word_label.setText("Empty Word")
            self.notes_label.setText("")
            self.show_btn.setEnabled(False)
            return

        current_item = self.words_list[self.current_index]
        self.word_label.setText(current_item['word'])
        self.notes_label.setText(current_item['notes'])

        # 每次切换新单词时，隐藏释义
        self.notes_label.hide()
        self.show_btn.setText("显示释义")
        self.show_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #3498DB; color: white; border-radius: 5px;")


    def init_ui(self):
        self.setWindowTitle("我的Web Highlights单词卡")
        # self.setFixedSize(450, 350)
        self.setMinimumSize(450, 350)

        # main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        # 1. 单词显示区域(大字母)
        self.word_label= QLabel()
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #2c3e50; margin-top: 20px")

        # 2. 释义,笔记显示区域
        self.notes_label = QLabel()
        self.notes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.notes_label.setWordWrap(True)
        self.notes_label.setStyleSheet("font-size: 16px; color: #7F8C8D; background-color: #F8F9F9; border-radius: 8px; padding: 10px;")

        # 3. 控制按钮
        self.show_btn = QPushButton("显示释义")
        self.show_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #3498DB; color: white; border-radius: 5px;")
        self.show_btn.clicked.connect(self.toggle_notes)

        # 底部翻页按钮布局
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("上一个")
        self.next_btn = QPushButton("下一个")

        btn_style = "padding: 8px; font-size: 14px; background-color: #BDC3C7; border-radius: 5px;"
        self.prev_btn.setStyleSheet(btn_style)
        self.next_btn.setStyleSheet(btn_style)

        self.prev_btn.clicked.connect(self.prev_word)
        self.next_btn.clicked.connect(self.next_word)

        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)

        main_layout.addWidget(self.word_label)
        main_layout.addWidget(self.notes_label)
        main_layout.addWidget(self.show_btn)
        main_layout.addLayout(nav_layout)

        self.setLayout(main_layout)

        # 显示第一个单词
        self.update_card()


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

    json_path = "webhighlights-backup-20260529-135026_formatter.json"

    window = WordReviewApp(json_path)
    window.show()
    sys.exit(app.exec())


