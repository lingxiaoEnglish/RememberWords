# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : 002_testWeb
@Author  : lingxiao
@Date    : 2026-06-24 11:28
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

# ... existing code ...
import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow
# 从独立的扩展库中导入 QWebEngineView
from PyQt6.QtWebEngineWidgets import QWebEngineView

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("PyQt6 网页加载示例")
        self.setGeometry(100, 100, 1024, 768)

        # 1. 创建浏览器组件
        self.browser = QWebEngineView()

        # 2. 核心：使用 QUrl 加载网页路径（必须带 http:// 或 https://）
        # self.browser.setUrl(QUrl("https://www.bbc.co.uk/learningenglish/english/features/6-minute-english_2026/ep-260212"))
        # https://html5test.com/
        self.browser.setUrl(QUrl("https://www.youtube.com/html5"))


        # 3. 将浏览器组件设置为窗口的中心控件
        self.setCentralWidget(self.browser)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebBrowser()
    window.show()
    sys.exit(app.exec())