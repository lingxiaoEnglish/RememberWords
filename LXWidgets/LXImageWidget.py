# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : LXImageWidget
@Author  : lingxiao
@Date    : 2026-06-02 15:42
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QImage, QColor
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QUrl, QRect, QSize
import resources_rc

class LXImageWidget(QLabel):
    """
    LXImageWidget: 高性能带圆角的图片控件（工业级完美版）
    内置全自动异步下载、深浅色模式占位图高精染色、多维圆角裁剪及双级缓存防抖机制。
    """
    load_finished = pyqtSignal(bool)

    def __init__(self, radius=None):
        """
        :param radius: 圆角半径，支持 int/float 或 tuple/list (左上, 右上, 右下, 左下)
        """
        super().__init__()
        self.radii = self._parse_radius(radius)

        # 激活背景色，保证没有图片下载成功前，QSS 中的背景色能正常渲染铺底
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.network_manager = None
        self.reply = None

        # --- 统一的图像核心缓存 ---
        self.raw_pixmap = None  # 原始高清图片缓存 (网络大图或占位大图)
        self.scaled_pixmap = None  # 直接用于 paintEvent 渲染的精确物理大小图片
        self.cached_path = None  # 矢量圆角裁剪路径 QPainterPath 缓存

        self.is_placeholder_active = False
        self.placeholder_name = "placeholder.png"

    def _parse_radius(self, radius):
        """解析多维圆角参数"""
        if radius is None or radius == 0:
            return [0.0, 0.0, 0.0, 0.0]
        if isinstance(radius, (int, float)):
            r = float(radius)
            return [r, r, r, r]
        if isinstance(radius, (tuple, list)) and len(radius) == 4:
            return [float(r) for r in radius]
        return [0.0, 0.0, 0.0, 0.0]

    def setRadius(self, radius):
        """动态改变圆角，清空矢量路径缓存"""
        if radius == self.radii:
            return
        self.radii = self._parse_radius(radius)
        self.cached_path = None
        self.update()

    def set_placeholder(self, image_name="placeholder.png"):
        """设置占位图，安全重置网络状态"""
        self.placeholder_name = image_name
        self.raw_pixmap = resources_rc.get_pixmap(image_name)

        if self.raw_pixmap and not self.raw_pixmap.isNull():
            self.is_placeholder_active = True
            self._update_scaled_pixmap()
        else:
            self.is_placeholder_active = False
            self.raw_pixmap = None
            self.scaled_pixmap = None
            print(f"[LXImageWidget] Failed to load placeholder image: {image_name}")

        self.update()

    def load_from_url(self, url_str: str, network_manager: QNetworkAccessManager = None):
        """高性能网络图片异步拉取"""
        if not url_str:
            return
        self.network_manager = network_manager or QNetworkAccessManager(self)

        # 【安全加固】断开旧连接，防止 abort() 触发 finished 信号导致状态错乱
        if self.reply:
            try:
                self.reply.finished.disconnect(self._on_download_finished)
            except (TypeError, RuntimeError):
                pass
            self.reply.abort()
            self.reply.deleteLater()
            self.reply = None

        # 先平滑切入本地占位图状态
        self.set_placeholder(self.placeholder_name)

        url = QUrl(url_str)
        request = QNetworkRequest(url)
        # 允许底层网络根据标准网络协议自动处理 301/302 重定向
        request.setAttribute(QNetworkRequest.Attribute.RedirectPolicyAttribute, True)

        self.reply = self.network_manager.get(request)
        self.reply.finished.connect(self._on_download_finished)

    def _on_download_finished(self):
        """网络下载完成后的核心处理链"""
        if not self.reply:
            return

        success = False
        if self.reply.error() == QNetworkReply.NetworkError.NoError:
            image_data = self.reply.readAll()
            image = QImage()
            if image.loadFromData(image_data):
                self.raw_pixmap = QPixmap.fromImage(image)
                self.is_placeholder_active = False  # 安全切换标志位
                self._update_scaled_pixmap()  # 仅在此处计算一次缩放缓存
                success = True
            else:
                print(f"[LXImageWidget] Failed to load image data from {self.reply.url().toString()}")
        else:
            # 过滤掉由于切歌或主动取消导致的异常 log 打印
            if self.reply.error() != QNetworkReply.NetworkError.OperationCanceledError:
                print(f"[LXImageWidget] Error downloading: {self.reply.errorString()}")

        self.reply.deleteLater()
        self.reply = None

        self.load_finished.emit(success) # noqa
        self.update()

    def setPixmap(self, pixmap: QPixmap):
        """兼容外部直接手动注入大图的情形"""
        self.raw_pixmap = pixmap
        self.is_placeholder_active = False
        self._update_scaled_pixmap()
        self.update()

    def resizeEvent(self, event):
        """尺寸变化时，让所有图形线段缓存、图像缩放缓存精准更新"""
        super().resizeEvent(event)
        self.cached_path = None
        self._update_scaled_pixmap()
        self.update()

    def _update_scaled_pixmap(self):
        """
        核心缓存屏障：将图像的所有密集型像素计算完全隔离在 paintEvent 之外
        """
        if self.raw_pixmap is None or self.raw_pixmap.isNull():
            self.scaled_pixmap = None
            return

        w_size = self.size()
        if w_size.width() <= 0 or w_size.height() <= 0:
            self.scaled_pixmap = None  # 边缘防御：防止不合理的初次零宽尺寸导致缓存残留
            return

        # 获取当前屏幕的物理像素比（Mac 一般为 2.0，Windows 可能是 1.25, 1.5, 2.0 等）
        dpr = self.devicePixelRatio()

        if self.is_placeholder_active:
            # --- 占位图居中且自适应染色逻辑 ---
            scale_factor = 0.8
            # 1. 计算出图标在当前屏幕下需要的【物理像素大小】
            logical_side = int(min(w_size.width(), w_size.height()) * scale_factor)
            physics_side = int(logical_side * dpr)

            if physics_side <= 0:
                self.scaled_pixmap = None
                return

            # 2. 直接对原始大图拉伸到【物理像素大小】，确保无论深浅模式，底图都是绝对高清的
            icon_scaled = self.raw_pixmap.scaled(
                QSize(physics_side, physics_side),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            # 判断深浅色模式
            bg_color = self.palette().color(self.backgroundRole())
            is_light_mode = bg_color.lightness() > 128

            # 如果是浅色模式，采用纯像素无损染色（直接对物理 QPixmap 进行染色，不经过二次坐标变换）
            if is_light_mode:
                tintED_pixmap = QPixmap(icon_scaled.size())
                tintED_pixmap.fill(Qt.GlobalColor.transparent)
                tp = QPainter(tintED_pixmap)
                tp.drawPixmap(0, 0, icon_scaled)
                # 采用 SourceIn 完美染色（冷灰色）
                tp.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
                tp.fillRect(tintED_pixmap.rect(), QColor("#8E8E93"))
                tp.end()
                icon_final = tintED_pixmap
            else:
                # 深色模式：保持原生纯白
                icon_final = icon_scaled

            # 3. 告诉 Qt 这个最终的图标已经具备 dpr 物理像素，还原它的逻辑尺寸
            icon_final.setDevicePixelRatio(dpr)

            # 4. 创建一张与物理 Widget 完全等大的透明底大画布
            final_physics_size = QSize(int(w_size.width() * dpr), int(w_size.height() * dpr))
            final_placeholder = QPixmap(final_physics_size)
            final_placeholder.fill(Qt.GlobalColor.transparent)
            final_placeholder.setDevicePixelRatio(dpr)  # 激活大画布的 DPR 映射机制

            # 5. 通过逻辑坐标进行绝对居中绘制，Qt 会自动进行完美的底片像素对齐
            p = QPainter(final_placeholder)
            p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

            # 这里 icon_final 内部由于正确设置了 dpr，其逻辑大小会自动适配
            icon_w = int(icon_final.width() / dpr)
            icon_h = int(icon_final.height() / dpr)
            target_rect = QRect(
                (w_size.width() - icon_w) // 2,
                (w_size.height() - icon_h) // 2,
                icon_w,
                icon_w
            )
            p.drawPixmap(target_rect, icon_final)
            p.end()

            self.scaled_pixmap = final_placeholder

        else:
            # --- 网络正式大图的平滑硬拉伸缩放 ---
            # physics_target_size = QSize(int(w_size.width() * dpr), int(w_size.height() * dpr))
            # self.scaled_pixmap = self.raw_pixmap.scaled(
            #     physics_target_size,
            #     Qt.AspectRatioMode.IgnoreAspectRatio,
            #     Qt.TransformationMode.SmoothTransformation
            # )
            # # 注入屏幕真实的像素比例，让 paintEvent 绘制时按 1:1 像素对齐，完全杜绝发虚
            # self.scaled_pixmap.setDevicePixelRatio(dpr)
            # 1. 计算出组件当前的物理像素宽高
            target_w = int(w_size.width() * dpr)
            target_h = int(w_size.height() * dpr)

            # print(f"----target_w:{target_w}")
            # print(f"----w_size.width():{w_size.width()}")

            # 2. 采用 KeepAspectRatioByExpanding (等比缩放至刚好完全覆盖目标区域)
            scaled_raw = self.raw_pixmap.scaled(
                QSize(target_w, target_h),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )

            # 3. 从等比缩放后的图中央，安全裁剪出与目标区域完全一致的物理像素切片
            crop_x = (scaled_raw.width() - target_w) // 2
            crop_y = (scaled_raw.height() - target_h) // 2

            # 4. 提取切片并注入屏幕真实的 DPR 像素比，确保绝对高清、杜绝虚化
            self.scaled_pixmap = scaled_raw.copy(crop_x, crop_y, target_w, target_h)
            self.scaled_pixmap.setDevicePixelRatio(dpr)

    def paintEvent(self, event):
        """
        极致轻量级的绘制：只有图层平铺，零数学运算
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        widget_rect = self.rect()
        is_rect_mode = all(r == 0.0 for r in self.radii)

        # 路径懒加载
        if not is_rect_mode and self.cached_path is None:
            self.cached_path = self._get_rounded_path()

        # 1. 绘制底色
        bg_color = self.palette().color(self.backgroundRole())
        if not is_rect_mode:
            painter.save()
            painter.setClipPath(self.cached_path)
            painter.fillRect(widget_rect, bg_color)
            painter.restore()
        else:
            painter.fillRect(widget_rect, bg_color)

        # 2. 直接倾泻缓存好的 Pixmap 像素，不带任何缩放损耗
        if self.scaled_pixmap and not self.scaled_pixmap.isNull():
            if not is_rect_mode:
                painter.save()
                painter.setClipPath(self.cached_path)
                painter.drawPixmap(widget_rect, self.scaled_pixmap)
                painter.restore()
            else:
                painter.drawPixmap(widget_rect, self.scaled_pixmap)

    def _get_rounded_path(self) -> QPainterPath:
        """根据当前标准化的 radii 勾勒高精度矢量封闭路径"""
        w, h = self.width(), self.height()
        tl, tr, br, bl = self.radii
        path = QPainterPath()

        path.moveTo(tl, 0)
        path.lineTo(w - tr, 0)
        if tr > 0:
            path.quadTo(w, 0, w, tr)
        else:
            path.lineTo(w, 0)

        path.lineTo(w, h - br)
        if br > 0:
            path.quadTo(w, h, w - br, h)
        else:
            path.lineTo(w, h)

        path.lineTo(bl, h)
        if bl > 0:
            path.quadTo(0, h, 0, h - bl)
        else:
            path.lineTo(0, h)

        path.lineTo(0, tl)
        if tl > 0:
            path.quadTo(0, 0, tl, 0)
        else:
            path.lineTo(0, 0)

        path.closeSubpath()
        return path