# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : 005_testWeb
@Author  : lingxiao
@Date    : 2026-06-24 14:22
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : 004_testWeb
@Author  : lingxiao
@Date    : 2026-06-24 14:12
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWebChannel import QWebChannel

# 高亮数据（硬编码，实际可从文件读取）
HIGHLIGHT_MARKS = [
    {
        "createdAt": 1772868384651,
        "updatedAt": 1772868387706,
        "url": "https://www.bbc.co.uk/learningenglish/english/features/6-minute-english_2026/ep-260212",
        "tags": [],
        "text": "it's hard to get a respite from training.",
        "type": "normal",
        "mediaType": "blockquote",
        "color": "#fdffb4",
        "highlightSource": {
            "startMeta": {"parentTagName": "P", "parentIndex": 12, "textOffset": 4137},
            "endMeta": {"parentTagName": "P", "parentIndex": 12, "textOffset": 4178},
            "text": "it's hard to get a respite from training.",
            "id": "70f020c8-77f9-48ae-8f37-632a0b227fd7"
        },
        "notes": "<p>从训练中获得<br>喘息的机会是很难的。</p>",
        "_id": "69abd320844393862cb2bb47"
    },
    {
        "createdAt": 1772866025815,
        "updatedAt": 1772868459807,
        "url": "https://www.bbc.co.uk/learningenglish/english/features/6-minute-english_2026/ep-260212",
        "tags": [],
        "text": "upside down",
        "type": "normal",
        "mediaType": "blockquote",
        "color": "#a7e8c8",
        "highlightSource": {
            "startMeta": {"parentTagName": "P", "parentIndex": 12, "textOffset": 632},
            "endMeta": {"parentTagName": "P", "parentIndex": 12, "textOffset": 643},
            "text": "upside down",
            "id": "7d7415c8-5c39-433b-9059-90e154ffef63"
        },
        "notes": "<p>颠倒的、倒过来的、上下翻转的</p>",
        "_id": "69abc9e9844393862cb2bb3f"
    },
    {
        "createdAt": 1772867670280,
        "updatedAt": 1772868459807,
        "url": "https://www.bbc.co.uk/learningenglish/english/features/6-minute-english_2026/ep-260212",
        "tags": [],
        "text": "over",
        "type": "normal",
        "mediaType": "blockquote",
        "color": "#fdffb4",
        "highlightSource": {
            "startMeta": {"parentTagName": "P", "parentIndex": 12, "textOffset": 1380},
            "endMeta": {"parentTagName": "P", "parentIndex": 12, "textOffset": 1384},
            "text": "over",
            "id": "67e708db-e372-4f3d-96ee-823df977d64a"
        },
        "notes": "<p>over ; prep, means 超过，多于</p>",
        "_id": "69abd056844393862cb2bb40"
    }
]

# Python 端接收回调的处理器
class Backend(QObject):
    # 信号：传递高亮 ID 和笔记内容
    highlightClicked = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str, str)          # 关键：声明该方法为槽，以便 QWebChannel 暴露给 JS
    def on_highlight_clicked(self, mark_id, notes):
        print(f"高亮被点击: ID={mark_id}, notes={notes}")
        self.highlightClicked.emit(mark_id, notes)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Highlight Click Demo")
        self.resize(1200, 800)

        # ----- 新增：设置 User-Agent -----
        from PyQt6.QtWebEngineCore import QWebEngineProfile
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        # --------------------------------

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.webview = QWebEngineView()
        settings = self.webview.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)

        # ----- 新增：取消播放需用户手势限制 -----
        settings.setAttribute(QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        # -----------------------------------

        layout.addWidget(self.webview)

        # 设置 WebChannel 用于 JavaScript 与 Python 通信
        self.channel = QWebChannel()
        self.backend = Backend()
        self.channel.registerObject("backend", self.backend)
        self.webview.page().setWebChannel(self.channel)

        # 页面加载完成后执行高亮
        self.webview.loadFinished.connect(self.on_load_finished)

        # 加载目标 URL
        target_url = "https://www.bbc.co.uk/learningenglish/english/features/6-minute-english_2026/ep-260212"
        self.webview.load(QUrl(target_url))

    def on_load_finished(self, success):
        if not success:
            print("页面加载失败")
            return

        marks_json = json.dumps(HIGHLIGHT_MARKS, ensure_ascii=False)

        # JavaScript 脚本：连接 WebChannel + 高亮 + 点击回调
        js_code = f"""
        (function() {{
            // 初始化 QWebChannel 连接
            function initWebChannel() {{
                // 动态加载 qwebchannel.js
                var script = document.createElement('script');
                script.src = 'qrc:///qtwebchannel/qwebchannel.js';
                script.onload = function() {{
                    new QWebChannel(qt.webChannelTransport, function(channel) {{
                        window.backend = channel.objects.backend;
                        console.log('WebChannel connected');
                        console.log('backend methods:', Object.keys(window.backend)); // 调试输出
                        // 连接成功后执行高亮
                        applyHighlights({marks_json});
                    }});
                }};
                document.head.appendChild(script);
            }}

            // 高亮功能（只添加背景色和点击事件，不改变任何原有样式）
            function applyHighlights(marks) {{
                marks.forEach(mark => {{
                    if (!mark.highlightSource) return;
                    const source = mark.highlightSource;
                    const startMeta = source.startMeta;
                    const endMeta = source.endMeta;
                    const color = mark.color || '#ffff00';
                    const markId = mark._id || '';
                    const notes = mark.notes || '';

                    try {{
                        const tag = startMeta.parentTagName.toLowerCase();
                        const index = startMeta.parentIndex;
                        const elements = document.querySelectorAll(tag);
                        if (index >= elements.length) {{
                            console.warn('索引超出范围:', tag, index);
                            return;
                        }}
                        const parentEl = elements[index];

                        const textNodes = [];
                        const walker = document.createTreeWalker(parentEl, NodeFilter.SHOW_TEXT, null, false);
                        while (walker.nextNode()) textNodes.push(walker.currentNode);

                        let currentOffset = 0;
                        let startNode = null, startNodeOffset = 0;
                        let endNode = null, endNodeOffset = 0;
                        for (const node of textNodes) {{
                            const len = node.textContent.length;
                            if (!startNode && currentOffset + len > startMeta.textOffset) {{
                                startNode = node;
                                startNodeOffset = startMeta.textOffset - currentOffset;
                            }}
                            if (!endNode && currentOffset + len >= endMeta.textOffset) {{
                                endNode = node;
                                endNodeOffset = endMeta.textOffset - currentOffset;
                                break;
                            }}
                            currentOffset += len;
                        }}

                        if (!startNode || !endNode) {{
                            console.warn('未找到对应文本节点，使用回退');
                            fallbackHighlight(mark);
                            return;
                        }}

                        const range = document.createRange();
                        range.setStart(startNode, startNodeOffset);
                        range.setEnd(endNode, endNodeOffset);

                        const span = document.createElement('span');
                        span.className = 'web-highlight';
                        span.style.backgroundColor = color;
                        span.style.cursor = 'pointer';
                        span.title = notes.replace(/<[^>]*>/g, '');

                        // 点击事件：调用 Python 端的方法
                        span.addEventListener('click', function() {{
                            if (window.backend && typeof window.backend.on_highlight_clicked === 'function') {{
                                window.backend.on_highlight_clicked(markId, notes);
                            }} else {{
                                console.warn('Backend not ready or method missing');
                                console.log('window.backend:', window.backend);
                            }}
                        }});

                        range.surroundContents(span);
                    }} catch (e) {{
                        console.error('高亮定位失败，尝试全文回退', e);
                        fallbackHighlight(mark);
                    }}
                }});
            }}

            // 回退方案：全文搜索并高亮第一个匹配
            function fallbackHighlight(mark) {{
                if (!mark.text) return;
                const text = mark.text;
                const color = mark.color || '#ffff00';
                const markId = mark._id || '';
                const notes = mark.notes || '';

                const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
                const textNodes = [];
                while (walker.nextNode()) textNodes.push(walker.currentNode);

                let fullText = '';
                const nodeMap = [];
                textNodes.forEach(node => {{
                    const startIdx = fullText.length;
                    fullText += node.textContent;
                    const endIdx = fullText.length;
                    nodeMap.push({{ node, startIdx, endIdx }});
                }});
                const matchIndex = fullText.indexOf(text);
                if (matchIndex === -1) return;

                let startNode, startOffset, endNode, endOffset;
                for (const item of nodeMap) {{
                    if (!startNode && item.endIdx > matchIndex) {{
                        startNode = item.node;
                        startOffset = matchIndex - item.startIdx;
                    }}
                    if (!endNode && item.endIdx >= matchIndex + text.length) {{
                        endNode = item.node;
                        endOffset = matchIndex + text.length - item.startIdx;
                        break;
                    }}
                }}
                if (!startNode || !endNode) return;

                const range = document.createRange();
                range.setStart(startNode, startOffset);
                range.setEnd(endNode, endOffset);
                const span = document.createElement('span');
                span.className = 'web-highlight';
                span.style.backgroundColor = color;
                span.style.cursor = 'pointer';
                span.addEventListener('click', function() {{
                    if (window.backend && typeof window.backend.on_highlight_clicked === 'function') {{
                        window.backend.on_highlight_clicked(markId, notes);
                    }} else {{
                        console.warn('Backend not ready or method missing');
                    }}
                }});
                try {{
                    range.surroundContents(span);
                }} catch (e) {{
                    console.warn('回退高亮失败', e);
                }}
            }}

            // 启动 WebChannel 初始化
            initWebChannel();
        }})();
        """

        self.webview.page().runJavaScript(js_code)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())