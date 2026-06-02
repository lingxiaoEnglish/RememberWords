# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : word_card
@Author  : lingxiao
@Date    : 2026-06-01 08:49
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

from PyQt6.QtWidgets import (QWidget, QFrame, QVBoxLayout, QLabel, QHBoxLayout)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtNetwork import QNetworkRequest, QNetworkReply
from PyQt6.QtGui import QImage, QPixmap, QPainter, QPainterPath
from models.page_models import *
from config.style_manager import StyleManager

class WordCard(QFrame):
    def __init__(self, page: Page, network_manager=None):
        """
        init word card widget
        :param page: 数据源
        """
        super().__init__()
        self.setObjectName("WordCard")
        self.page = page
        self.network_manager = network_manager
        ######
        self.card_layout=None
        self.cover_img=None
        self.raw_pixmap = None # 用于缓存下载好的原始图片，以便在缩放时重新渲染
        self.init_ui()
        self.start_image_download()
        print(f"-------current_width:{self.width()}")

    def start_image_download(self):
        """
        start image download
        :return:
        """
        url = QUrl(self.page.meta.image.url)
        request = QNetworkRequest(url)
        # 发起异步网络请求
        self.reply = self.network_manager.get(request)
        self.reply.finished.connect(self.on_image_downloaded)

    def on_image_downloaded(self):
        if self.reply and self.reply.error() == QNetworkReply.NetworkError.NoError:
            image_data = self.reply.readAll()
            image = QImage()
            if image.loadFromData(image_data):
                # 缓存原始 Pixmap
                self.raw_pixmap = QPixmap.fromImage(image)
                self.update_cover_image()

            else:
                print("Failed to load image.")
        else:
            print("Error:", self.reply.errorString())

        if self.reply:
            self.reply.deleteLater()
            self.reply = None

    def update_cover_image(self):
        """🛠️ 新增：根据当前卡片宽度，按照 68/120 的比例精准裁剪并缩放图片"""
        if not self.raw_pixmap or self.raw_pixmap.isNull():
            return
        # 1. 计算目标尺寸（宽度等于当前父视图/卡片除去边距后的可用宽度）

        # print(f"-------current_width:{self.width()}")

        current_width = self.width()
        current_height = int(current_width * (68 / 120))
        # 2. 设置 QLabel 的高度，使其在垂直布局中完美卡死 68/120 比例
        self.cover_img.setFixedHeight(current_height)
        # 3. 按最新计算出来的动态尺寸进行裁切填充（Expanding），确保不变形
        """
        QLabel 通过 setPixmap 绘制进去的图片（QPixmap）是一个矩形;
        它在底层渲染时，会直接无情地覆盖掉 QLabel 自身的 QSS 圆角边框，把圆角给“撑破”并遮挡住了。
        """
        scaled_pixmap = self.raw_pixmap.scaled(
            current_width,
            current_height,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        # set radius
        rounded_pixmap = QPixmap(scaled_pixmap.size())
        # set 透明 背景色
        rounded_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) # 开启抗锯齿，边缘不会有锯齿毛边
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # 创建裁剪路径：只有左上和右上是圆角，左下右下是直角 (半径 11px)
        radius = 11.0
        path = QPainterPath()
        # 绘制带顶部圆角的特殊路径 (用画笔顺时针勾勒)
        path.moveTo(0, current_height)  # 左下角 (直角)
        path.lineTo(0, radius)  # 向上画到左上圆角起点
        path.quadTo(0, 0, radius, 0)  # 画左上圆角
        path.lineTo(current_width - radius, 0)  # 向右画到右上圆角起点
        path.quadTo(current_width, 0, current_width, radius)  # 画右上圆角
        path.lineTo(current_width, current_height)  # 向下画到右下角 (直角)
        path.closeSubpath()  # 封闭底部直角边
        painter.setClipPath(path)  # 开启裁剪蒙版！
        painter.drawPixmap(0, 0, scaled_pixmap)  # 把图片画入蒙版中
        painter.end()
        self.cover_img.setPixmap(rounded_pixmap)

    def init_ui(self):
        self.setFixedWidth(240)
        # use vertical layout flow
        self.card_layout = QVBoxLayout(self)
        self.card_layout.setContentsMargins(0, 0, 0, 0)
        self.card_layout.setSpacing(10)

        # cover img
        self.cover_img = QLabel()
        self.cover_img.setObjectName("CardCover")
        # self.cover_img.setFixedSize(120, 68)
        # self.cover_img.setFixedHeight(120)
        # self.cover_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_layout.addWidget(self.cover_img)

        # text container
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(10, 0, 10, 0)
        text_layout.setSpacing(8)

        # title
        title_label = QLabel(self.page.title)
        title_label.setObjectName("CardTitle")
        title_label.setWordWrap(True)
        text_layout.addWidget(title_label)

        # highlights and notes
        highlight_notes_layout = QHBoxLayout()
        hightlight_label = QLabel(f"Highlights: {10}")
        hightlight_label.setObjectName("CardHighlight")
        highlight_notes_layout.addWidget(hightlight_label)

        notes_label = QLabel(f"Notes: {20}")
        notes_label.setObjectName("CardNotes")
        highlight_notes_layout.addWidget(notes_label)

        text_layout.addLayout(highlight_notes_layout)

        source_time_layout = QHBoxLayout()
        source_label = QLabel(self.page.origin)
        source_label.setObjectName("CardSource")
        source_time_layout.addWidget(source_label)
        time_label = QLabel(f"{self.page.created_date}")
        time_label.setObjectName("CardTime")
        source_time_layout.addWidget(time_label)
        text_layout.addLayout(source_time_layout)
        self.card_layout.addWidget(text_container)
        self.setStyleSheet(StyleManager.load_word_card_css())








