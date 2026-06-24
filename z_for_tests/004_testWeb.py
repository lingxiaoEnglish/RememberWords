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
from PyQt6.QtCore import QUrl, QTimer

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Highlight Reader")
        self.resize(1200, 800)

        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建 WebEngine 视图
        self.webview = QWebEngineView()
        # 允许 JavaScript 和本地存储
        settings = self.webview.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        layout.addWidget(self.webview)

        # 页面加载完成后执行高亮和阅读模式
        self.webview.loadFinished.connect(self.on_load_finished)

        # 加载目标 URL
        target_url = "https://www.bbc.co.uk/learningenglish/english/features/6-minute-english_2026/ep-260212"
        self.webview.load(QUrl(target_url))

    def on_load_finished(self, success):
        """页面加载完成后注入 JavaScript 实现阅读模式和高亮"""
        if not success:
            print("页面加载失败")
            return

        # 将 marks 转为 JSON 字符串，安全嵌入 JS
        marks_json = json.dumps(HIGHLIGHT_MARKS, ensure_ascii=False)

        # JavaScript 脚本：阅读模式 + 高亮
        js_code = f"""
        (function() {{
            // ========== 1. 阅读模式：隐藏干扰元素，调整样式 ==========
            function applyReadingMode() {{
                // 添加阅读模式样式
                const style = document.createElement('style');
                style.id = 'reading-mode-style';
                style.textContent = `
                    /* 隐藏头部、导航、侧栏、页脚、广告等 */
                    header, footer, nav, aside, .ad, .advertisement,
                    .share, .social, .related, .recommend,
                    #bbcle-header, #bbcle-footer, .top-nav, .sidebar,
                    .comments, .meta, .tags, .breadcrumb, .print-hide {{
                        display: none !important;
                    }}
                    /* 让主要内容居中、加宽、调整字体 */
                    body {{
                        background: #f5f5f5 !important;
                    }}
                    article, main, .bbcle-body, .article__body, .story-body,
                    .content-body, #main-content {{
                        max-width: 800px !important;
                        margin: 20px auto !important;
                        padding: 30px !important;
                        background: white !important;
                        box-shadow: 0 0 10px rgba(0,0,0,0.1) !important;
                        font-size: 18px !important;
                        line-height: 1.8 !important;
                        color: #333 !important;
                        font-family: Georgia, 'Times New Roman', serif !important;
                    }}
                    /* 如果没有特定容器，则使用 body 本身 */
                    body.reading-mode {{
                        max-width: 800px !important;
                        margin: 20px auto !important;
                        padding: 30px !important;
                        background: white !important;
                        box-shadow: 0 0 10px rgba(0,0,0,0.1) !important;
                        font-size: 18px !important;
                        line-height: 1.8 !important;
                    }}
                    /* 高亮标注的基础样式 */
                    .web-highlight {{
                        cursor: pointer;
                        border-radius: 2px;
                        padding: 0 2px;
                        transition: background 0.2s;
                        position: relative;
                    }}
                    .web-highlight:hover {{
                        filter: brightness(0.95);
                    }}
                    /* 笔记 tooltip */
                    .web-highlight-note {{
                        visibility: hidden;
                        background: #333;
                        color: #fff;
                        padding: 8px 12px;
                        border-radius: 6px;
                        position: absolute;
                        z-index: 9999;
                        bottom: 125%;
                        left: 50%;
                        transform: translateX(-50%);
                        white-space: normal;
                        max-width: 300px;
                        font-size: 14px;
                        line-height: 1.4;
                        text-align: left;
                    }}
                    .web-highlight:hover .web-highlight-note {{
                        visibility: visible;
                    }}
                `;
                document.head.appendChild(style);

                // 尝试找到主要内容容器，若无则给 body 添加类
                const selectors = ['article', 'main', '.bbcle-body', '.article__body', '.story-body', '.content-body', '#main-content'];
                let found = false;
                for (const sel of selectors) {{
                    const el = document.querySelector(sel);
                    if (el) {{
                        el.style.cssText = `max-width: 800px !important; margin: 20px auto !important;
                                            padding: 30px !important; background: white !important;
                                            box-shadow: 0 0 10px rgba(0,0,0,0.1) !important;
                                            font-size: 18px !important; line-height: 1.8 !important;`;
                        found = true;
                        break;
                    }}
                }}
                if (!found) {{
                    document.body.classList.add('reading-mode');
                }}
            }}

            // ========== 2. 高亮功能 ==========
            function applyHighlights(marks) {{
                marks.forEach(mark => {{
                    if (!mark.highlightSource) return;

                    const source = mark.highlightSource;
                    const startMeta = source.startMeta;
                    const endMeta = source.endMeta;
                    const color = mark.color || '#ffff00';
                    const notes = mark.notes || '';

                    try {{
                        // 根据 parentTagName 和 parentIndex 定位父元素
                        const tag = startMeta.parentTagName.toLowerCase();
                        const index = startMeta.parentIndex;
                        const elements = document.querySelectorAll(tag);
                        if (index >= elements.length) {{
                            console.warn('索引超出范围:', tag, index);
                            return;
                        }}
                        const parentEl = elements[index];

                        // 获取该元素下的所有文本节点
                        const textNodes = [];
                        const walker = document.createTreeWalker(
                            parentEl,
                            NodeFilter.SHOW_TEXT,
                            null,
                            false
                        );
                        while (walker.nextNode()) {{
                            textNodes.push(walker.currentNode);
                        }}

                        // 计算文本偏移量，找到开始和结束节点
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
                            console.warn('未找到对应文本节点');
                            // 回退：全文搜索文本
                            fallbackHighlight(mark);
                            return;
                        }}

                        // 创建 Range 并包裹高亮 span
                        const range = document.createRange();
                        range.setStart(startNode, startNodeOffset);
                        range.setEnd(endNode, endNodeOffset);

                        const span = document.createElement('span');
                        span.className = 'web-highlight';
                        span.style.backgroundColor = color;
                        span.title = notes.replace(/<[^>]*>/g, ''); // 纯文本 title

                        // 如果 notes 有内容，添加 tooltip
                        if (notes.trim()) {{
                            const tooltip = document.createElement('span');
                            tooltip.className = 'web-highlight-note';
                            tooltip.innerHTML = notes;
                            span.appendChild(tooltip);
                        }}

                        range.surroundContents(span);
                    }} catch (e) {{
                        console.error('高亮定位失败，尝试全文回退', e);
                        fallbackHighlight(mark);
                    }}
                }});
            }}

            // 回退方案：在整页文本中搜索并高亮第一个匹配
            function fallbackHighlight(mark) {{
                if (!mark.text) return;
                const text = mark.text;
                const color = mark.color || '#ffff00';
                const notes = mark.notes || '';

                // 使用 TreeWalker 遍历所有文本节点
                const walker = document.createTreeWalker(
                    document.body,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );
                const textNodes = [];
                while (walker.nextNode()) textNodes.push(walker.currentNode);

                // 拼合全文并查找
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

                // 定位到节点
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
                if (notes.trim()) {{
                    const tooltip = document.createElement('span');
                    tooltip.className = 'web-highlight-note';
                    tooltip.innerHTML = notes;
                    span.appendChild(tooltip);
                }}
                try {{
                    range.surroundContents(span);
                }} catch (e) {{
                    console.warn('回退高亮失败', e);
                }}
            }}

            // 先应用阅读模式
            applyReadingMode();
            // 再应用高亮（延迟一点确保样式生效，但不必须）
            const marks = {marks_json};
            applyHighlights(marks);
        }})();
        """

        # 注入脚本
        self.webview.page().runJavaScript(js_code)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
