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
from PyQt6.QtCore import Qt, pyqtSignal, QUrl, QRect
import resources_rc


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

        self.reply = None
        self.raw_pixmap = None  # 缓存原始图片，用于后续缩放或重绘
        self.network_manager = None
        # 标记当前内存中的 pixmap 是否是占位图
        self.is_placeholder_active = False

    def set_placeholder(self, image_name="placeholder.png"):
        """
        通过图片文件名直接从内存加载
        :param image_name: placeholder.png
        """
        # 直接根据名字从字典里捞 QPixmap
        placeholder_pixmap = resources_rc.get_pixmap(image_name)

        if not placeholder_pixmap.isNull():
            self.is_placeholder_active = True
            self.setPixmap(placeholder_pixmap)
        else:
            self.is_placeholder_active = False
            print(f"[LXImageWidget] Failed to load placeholder image from resources")

    def load_from_url(self, url_str:str, network_manager: QNetworkAccessManager=None):
        """
        load 图片，并自动渲染
        """
        if not url_str:
            return
        self.network_manager = network_manager or QNetworkAccessManager(self)

        if self.reply:
            try:
                self.reply.disconnect()
            except TypeError:
                pass
            self.reply.abort()
            self.reply = None

        url = QUrl(url_str)
        request = QNetworkRequest(url)
        self.set_placeholder()
        # self.reply = self.network_manager.get(request)
        # self.reply.finished.connect(self._on_download_finished)

    def _on_download_finished(self):
        success = False
        if self.reply and self.reply.error() == QNetworkReply.NetworkError.NoError:
            image_data = self.reply.readAll()
            image = QImage()
            if image.loadFromData(image_data):
                self.raw_pixmap = QPixmap.fromImage(image)
                self.is_placeholder_active = False  # 切换为正式网络图
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
        # super().paintEvent(a0)
        # 注意：这里千万不要调用 super().paintEvent(a0)，因为我们要完全托管绘制
        # 如果调用父类，QLabel 内部会用直角原生的方式再画一次图片，破坏圆角裁剪效果
        #托管绘制，不调用super().paintEvent(event) 避免直角底色冲突

        painter = QPainter(self)
        """
            在 QPainter 的绘制逻辑中，painter.restore() 与 painter.save() 是必须成对出现的黄金搭档。
            它们的核心作用是：通过内部维护的一个栈（Stack），来保护、备份和恢复 QPainter 的绘制状态。
        """


        # 开启顶级硬件级抗锯齿与像素平滑变换，保障边缘锐利无毛刺
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        # check all radius are zero
        is_rect_mode = all(r == 0.0 for r in self.radii)
        widget_rect = self.rect()

        # 自动获取当前系统的 QSS 背景色或主题底色进行铺底
        bg_color = self.palette().color(self.backgroundRole())
        # 💡 核心算法：通过判断底色的亮度（Lightness）来自动化识别深浅色模式
        # bg_color.lightness() 范围是 0-255，值越大说明底色越亮（浅色模式）
        is_light_mode = bg_color.lightness() > 128

        # --- 1. 绘制底色带安全圆角裁剪（适配深色/浅色模式） ---
        # 如果我们在 QSS 里为 LXImageWidget 设置了 background-color，
        # 如果不先画底色，裁剪网络图时边缘可能会漏出大片空白，或者占位图四周会透明。
        painter.save()
        if not is_rect_mode:
            path = self._get_rounded_path()
            painter.setClipPath(path) #设置裁剪区域
        painter.fillRect(widget_rect, bg_color)
        painter.restore()

        # --- 2. 绘制图片 ---
        if self.pixmap and not self.pixmap.isNull():
            painter.save()

            # 如果不是直角模式，开启安全圆角边界裁剪
            if not is_rect_mode:
                path = self._get_rounded_path()
                painter.setClipPath(path)

            if self.is_placeholder_active:
                # 💡 占位图专属逻辑：计算居中正方形且不拉伸
                # 限制占位图的最大高宽不超过容器宽高的 50%（或者你可以随意调整这个比例系数）
                scale_factor = 0.8
                side_len = min(widget_rect.width(), widget_rect.height()) * scale_factor

                # 建立正方形目标区域
                target_rect = QRect(
                    int((widget_rect.width() - side_len) / 2),
                    int((widget_rect.height() - side_len) / 2),
                    int(side_len),
                    int(side_len)
                )

                # 🎨 【核心魔法】如果是浅色模式，动态将白色图案染色成高质感灰色
                if is_light_mode:
                    # 1. 先把白色占位图绘制到一层临时画布（Layer）上
                    buffer = QPixmap(self.pixmap.size())
                    buffer.fill(Qt.GlobalColor.transparent)  # 保持透明底
                    buffer_painter = QPainter(buffer)
                    buffer_painter.drawPixmap(0, 0, self.pixmap)

                    # 2. 启用 SourceAtop 混合模式（只在有图像像素的地方覆盖颜色）
                    buffer_painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceAtop)

                    # 3. 泼上一层优雅的灰色（这里用 #8E8E93，即苹果经典的系统冷灰）
                    buffer_painter.fillRect(buffer.rect(), QColor("#8E8E93"))
                    buffer_painter.end()

                    # 4. 绘制染色后的灰色占位图
                    painter.drawPixmap(target_rect, buffer)
                else:
                    # 深色模式：保持原汁原味的白色透明图
                    painter.drawPixmap(target_rect, self.pixmap)
            else:
                # 💡 正式网络图逻辑：保持原本的铺满/拉伸裁剪模式
                painter.drawPixmap(widget_rect, self.pixmap)

            painter.restore()

        painter.end() # 关闭绘制设备，并立即将所有缓存的绘制指令“冲刷”（Flush）到硬件屏幕上
        """
            1. 触发真正的硬件渲染（Flush 机制）
                为了提高性能，QPainter 在执行 drawPixmap、fillRect 等方法时，并不是每调用一次就立刻去刷一次屏幕（这样会导致严重的掉帧和卡顿）。
                它会把这些指令暂时攒在内存缓存区里。
                当你调用 painter.end() 时，Qt 会收到信号，将缓存中的所有图形和指令批量打包一次性发送给底层的操作系统图形引擎（如 macOS 的 Metal 或 Windows 的 Direct3D），
                在屏幕上真正把画面呈显出来。

            2. 解除设备锁定（Release Device）
                当一个 QPainter 激活在某个控件（如 LXImageWidget）上时，该控件的重绘系统就会进入锁定状态，不允许其他地方同时对其自绘。
                end() 会释放这个绘制设备的控制权，让控件重新回归正常的系统流中。

            3. 释放底层 C++ 资源
                QPainter 极其依赖底层的 C++ 原生句柄和内存。
                调用 end() 会立即释放对应的系统画笔、画刷句柄，避免潜在的内存泄漏或图形句柄耗尽。
        """



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
