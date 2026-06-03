# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : preview_page
@Author  : lingxiao
@Date    : 2026-06-03 13:24
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGridLayout
from models.page_models import Page
import qtawesome as qta
from LXWidgets.LXImageWidget import LXImageWidget

class PreviewPage(QWidget):

    signal_close = pyqtSignal()

    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 1. 创建一个网格布局作为复合容器
        cover_grid = QGridLayout()
        cover_grid.setContentsMargins(0, 0, 0, 0)
        cover_grid.setSpacing(0)

        # 2. 底层大图
        self.cover_img = LXImageWidget()
        self.cover_img.setFixedHeight(200)
        self.cover_img.load_from_url(url_str=self.page.meta.image.url)
        # 重点：让图片占据 (0,0) 的格子，行跨度1，列跨度1
        cover_grid.addWidget(self.cover_img, 0, 0, 1, 1)
        # 🚀 3 & 4 重新整合：创建一个完全铺满大图的顶层叠加容器
        overlay_container = QWidget()
        overlay_container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 核心垂直布局：上边管顶部阴影，下边管标题阴影
        overlay_vbox = QVBoxLayout(overlay_container)
        overlay_vbox.setContentsMargins(0, 0, 0, 0)
        overlay_vbox.setSpacing(0)

        # ------------------- 🆕 顶部：遮罩层 -------------------
        top_mask = QWidget()
        top_mask.setFixedHeight(50)  # 阴影高度可以根据需要调整，50px 足以衬托按钮
        top_mask.setStyleSheet("""
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0,0,0,0.6), stop:1 rgba(0,0,0,0));
                """)
        overlay_vbox.addWidget(top_mask)

        # ------------------- 🛹 中间：弹簧 -------------------
        # 把顶部阴影和底部标题完全推开到两端
        overlay_vbox.addStretch(1)

        # ------------------- 底部：标题层 -------------------
        title_label = QLabel(self.page.title)
        title_label.setStyleSheet("""
                    color: white; font-size: 18px; font-weight: bold;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0,0,0,0), stop:1 rgba(0,0,0,0.6));
                    padding: 12px 10px 10px 10px;
                """)
        title_label.setWordWrap(True)
        overlay_vbox.addWidget(title_label)

        # 🚀 重点1：把铺满的叠加容器塞入网格 (不加任何 Alignment，让它横向纵向都完全拉伸)
        cover_grid.addWidget(overlay_container, 0, 0, 1, 1)

        # ------------------- 🎯 关闭按钮 -------------------
        # 按钮作为独立的覆盖层放进网格，并通过对齐方式精确锁死在右上角。
        # 此时它会完美叠加在 top_mask 的渐变阴影之上，点击事件和视觉效果都是完美的。
        close_btn = QPushButton()
        close_btn.setObjectName("CloseBtn")
        close_btn.setIcon(qta.icon("mdi.close", color="#FFFFFF"))
        close_btn.setFixedSize(26, 26)
        close_btn.clicked.connect(self.signal_close.emit)  # noqa

        # 通过右边距和顶边距微调按钮在阴影区里的位置 (可选，这里保留 10px 的系统边缘美感)
        cover_grid.addWidget(close_btn, 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeading)

        # 将网格组合布局放入主布局
        main_layout.addLayout(cover_grid)
        main_layout.addStretch(1)

