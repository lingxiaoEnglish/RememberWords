# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : LXImageWidget
@Author  : lingxiao
@Date    : 2026-06-02 15:42
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QImage
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QUrl


class LXImageWidget(QLabel):
    """
    LXImageWidget: 带圆角的图片控件
    """
    load_finished = pyqtSignal(bool)


    def __init__(self, radius=None):
        """
        :param radius: 圆角半径,可以是以下几种格式:
                       - None 或 0: 完全直角，无圆角
                       - int / float: 四个角拥有相同的圆角半径 (例如: 11)
                       - tuple / list (len=4): 分别指定 (左上, 右上, 右下, 左下) 的半径
                                              (例如顶栏卡片常用: (11, 11, 0, 0))
        """
        super().__init__()
        self.pixmap = None
        self.radii = self._parse_radius(radius)
        # 激活背景色，保证没有图片下载成功前，QSS 中的背景色(cover_bg)能正常渲染占位
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.replay = None
        self.raw_pixmap = None  # 缓存原始图片，用于后续缩放或重绘
        self.network_manager = None

    def load_from_url(self, url_str:str, network_manager: QNetworkAccessManager=None):
        """
        load 图片，并自动渲染
        """
        if not url_str:
            return
        self.network_manager = network_manager or QNetworkAccessManager(self)

        if self.replay:
            self.replay.disconnect()
            self.replay.abort()
            self.replay = None

        url = QUrl(url_str)
        request = QNetworkRequest(url)
        self.reply = self.network_manager.get(request)
        self.reply.finished.connect(self._on_download_finished)

    def _on_download_finished(self):
        success = False
        if self.reply and self.reply.error() == QNetworkReply.NetworkError.NoError:
            image_data = self.reply.readAll()
            image = QImage()
            if image.loadFromData(image_data):
                self.raw_pixmap = QPixmap.fromImage(image)
                # 直接渲染
                self.setPixmap(self.raw_pixmap)
                success = True
            else:
                print(f"[LXImageWidget] Failed to load image data from {self.reply.url().toString()}")
        else:
            if self.reply:
                print(f"[LXImageWidget] Error downloading: {self.reply.errorString()}")

        if self.reply:
            self.reply.deleteLater()
            self.reply = None

        self.load_finished.emit(success)

    def _parse_radius(self, radius):
        if radius is None or radius == 0:
            return [0.0, 0.0, 0.0, 0.0]

        if isinstance(radius, (int, float)):
            r = float(radius)
            return [r, r, r, r]

        if isinstance(radius, (tuple, list)) and len(radius) == 4:
            return [float(r) for r in radius]

        return [0.0, 0.0, 0.0, 0.0]

    def setPixmap(self, pixmap: QPixmap):
        """
        注入原始高清图并更新画布
        :param pixmap: 原始高清图片
        """
        self.pixmap = pixmap
        """
        调用 self.update() 不会立刻去画图，而是向 Qt 的事件循环（Event Loop）发送一个重绘请求（Paint Event）。
        Qt 收到请求后，会在极短的时间内（通常是几毫秒内）自动去调用该控件的 paintEvent(self, event) 方法。
        """
        self.update()

    def setRadius(self, radius):
        """
        设置圆角半径
        :param radius: 圆角半径
        """
        self.radii = self._parse_radius(radius)
        self.update()

    def paintEvent(self, a0):
        super().paintEvent(a0)

        painter = QPainter(self)
        # 开启顶级硬件级抗锯齿与像素平滑变换，保障边缘锐利无毛刺
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # check all radius are zero
        is_rect_mode = all(r == 0.0 for r in self.radii)

        # 1. 占位阶段：无图片时，绘制纯色背景
        if not self.pixmap or self.pixmap.isNull():
            if not is_rect_mode:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(Qt.GlobalColor.transparent)
                path = self._get_rounded_path()
                painter.drawPath(path)
            return

        if is_rect_mode:
            painter.drawPixmap(self.rect(), self.pixmap)
        else:
            path = self._get_rounded_path()
            painter.setClipPath(path) # 开启安全边界裁剪
            painter.drawPixmap(self.rect(), self.pixmap)

        painter.end()



    def _get_rounded_path(self) -> QPainterPath:
        """根据当前标准化的 [tl, tr, br, bl] 独立勾勒高精度封闭路径"""
        w, h = self.width(), self.height()
        tl, tr, br, bl = self.radii
        path = QPainterPath()

        # 1. 从左上角圆角终点出发 (x=tl, y=0)
        path.moveTo(tl, 0)

        # 2. 绘制顶部横线 -> 右上角圆角
        path.lineTo(w - tr, 0)
        if tr > 0:
            # 二次贝塞尔曲线
            path.quadTo(w, 0, w, tr)
        else:
            path.lineTo(w, 0)

        # 3. 绘制右侧竖线 -> 右下角圆角
        path.lineTo(w, h - br)
        if br > 0:
            path.quadTo(w, h, w - br, h)
        else:
            path.lineTo(w, h)

        # 4. 绘制底部横线 -> 左下角圆角
        path.lineTo(bl, h)
        if bl > 0:
            path.quadTo(0, h, 0, h - bl)
        else:
            path.lineTo(0, h)

        # 5. 绘制左侧竖线 -> 回到左上角圆角起点完成封闭
        path.lineTo(0, tl)
        if tl > 0:
            path.quadTo(0, 0, tl, 0)
        else:
            path.lineTo(0, 0)

        path.closeSubpath()
        return path
