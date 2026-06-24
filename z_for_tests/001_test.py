# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : test
@Author  : lingxiao
@Date    : 2026-06-24 10:06
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class ImageCardWidget(QWidget):
    def __init__(self, top_text, bottom_text, image_path=None, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 250)

        # 1. 底层：背景图片标签
        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, 200, 250)
        self.bg_label.setScaledContents(True)  # 让图片撑满标签
        if image_path:
            self.bg_label.setPixmap(QPixmap(image_path))
        else:
            self.bg_label.setStyleSheet("background-color: #ff0000; border-radius: 6px;")

        # 2. 顶层：控制文字位置的布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # 间距清零，使标题贴边

        # 顶部标题
        self.top_title = QLabel(top_text)
        self.top_title.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 适配 PyQt6
        self.top_title.setFixedHeight(35)
        self.top_title.setStyleSheet("""
            background-color: rgba(0, 0, 0, 130); 
            color: white; 
            font-weight: bold;
            font-size: 13px;
        """)

        # 底部标题
        self.bottom_title = QLabel(bottom_text)
        self.bottom_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bottom_title.setFixedHeight(35)
        self.bottom_title.setStyleSheet("""
            background-color: rgba(0, 0, 0, 130); 
            color: white; 
            font-weight: bold;
            font-size: 13px;
        """)

        # 组装布局
        main_layout.addWidget(self.top_title)
        main_layout.addStretch()  # 核心：弹簧将上下标题往两边推
        main_layout.addWidget(self.bottom_title)


# --- 使用示例 ---
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 实例化一个卡片
    card = ImageCardWidget("Header Title", "Footer Title")
    card.show()

    sys.exit(app.exec())