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
from LXWidgets.LXImageWidget import LXImageWidget

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
        self.reply = None
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
                # self.update_cover_image()
                self.cover_img.setPixmap(self.raw_pixmap)
            else:
                print("Failed to load image.")
        else:
            print("Error:", self.reply.errorString())

        if self.reply:
            self.reply.deleteLater()
            self.reply = None

    def init_ui(self):
        self.setFixedWidth(240)
        # use vertical layout flow
        self.card_layout = QVBoxLayout(self)
        self.card_layout.setContentsMargins(0, 0, 0, 0)
        self.card_layout.setSpacing(10)

        # cover img
        self.cover_img = LXImageWidget(radius=(11, 11, 0, 0))
        self.cover_img.setObjectName("CardCover")
        self.cover_img.setFixedSize(240, 136)
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








