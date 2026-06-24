# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : 003_testWeb
@Author  : lingxiao
@Date    : 2026-06-24 13:37
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
import sys
import json
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QObject, pyqtSlot


class Bridge(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str)
    def onHighlightClick(self, data_json_str):
        data = json.loads(data_json_str)
        notes = data.get("notes", "无笔记")
        text = data.get("text", "")
        QMessageBox.information(None, "WebHighlights 笔记", f"高亮文本:\n{text}\n\n笔记内容:\n{notes}")


class FixedReaderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebHighlights 完美高亮修复版")
        self.setGeometry(100, 100, 1100, 850)

        self.original_url = "https://www.bbc.co.uk/learningenglish/english/features/6-minute-english_2026/ep-260212"

        # 你的核心高亮 JSON 数据
        self.highlight_data = {
            "text": "it's hard to get a respite from training.",
            "color": "#fdffb4",
            "notes": "<p>从训练中获得<br>喘息的机会是很难的。</p>"
        }

        # 记录当前是什么模式，防止 loadFinished 信号乱串
        self.current_mode = "normal"

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)

        btn_layout = QHBoxLayout()
        self.btn_normal = QPushButton("← 返回原始网页")
        self.btn_reader = QPushButton("✨ 进入 WebHighlights 纯净阅读模式")
        self.btn_normal.clicked.connect(self.load_normal)
        self.btn_reader.clicked.connect(self.switch_to_pure_reader_mode)
        btn_layout.addWidget(self.btn_normal)
        btn_layout.addWidget(self.btn_reader)
        layout.addLayout(btn_layout)

        self.browser = QWebEngineView()
        layout.addWidget(self.browser)
        self.setCentralWidget(main_widget)

        # 绑定统一的加载完成信号
        self.browser.loadFinished.connect(self.on_page_load_finished)

        # 初始化 WebChannel
        self.channel = QWebChannel()
        self.bridge = Bridge()
        self.channel.registerObject("pyBridge", self.bridge)
        self.browser.page().setWebChannel(self.channel)

        self.load_normal()

    def load_normal(self):
        self.current_mode = "normal"
        self.browser.setUrl(QUrl(self.original_url))

    def switch_to_pure_reader_mode(self):
        self.current_mode = "extracting"

        # 提取正文的 JS 逻辑
        pure_extract_js = """
        (function() {
            let title = document.title;
            let bestCandidate = null;
            let maxScore = 0;
            const paragraphs = document.getElementsByTagName('p');
            for (let p of paragraphs) {
                let parent = p.parentNode;
                if (!parent) continue;
                let score = parent.getElementsByTagName('p').length * 10;
                if (parent.className && /sidebar|comment|footer|nav|header|ads/i.test(parent.className)) score -= 150;
                if (parent.id && /sidebar|comment|footer|nav|header|ads/i.test(parent.id)) score -= 150;
                if (score > maxScore) { maxScore = score; bestCandidate = parent; }
            }
            let contentNode = bestCandidate ? bestCandidate.cloneNode(true) : (document.querySelector('article') || document.body).cloneNode(true);
            const unneeded = 'script, style, iframe, nav, header, footer, .sidebar, .ads, button, input, form, svg, noscript';
            contentNode.querySelectorAll(unneeded).forEach(el => el.remove());
            contentNode.querySelectorAll('a').forEach(link => {
                link.removeAttribute('href'); link.style.color = 'inherit'; link.style.textDecoration = 'none'; link.style.cursor = 'text';
                link.onclick = function(e) { e.preventDefault(); e.stopPropagation(); };
            });
            return { title: title, content: contentNode.innerHTML };
        })();
        """
        self.browser.page().runJavaScript(pure_extract_js, self.render_pure_view)

    def render_pure_view(self, result):
        if not result or not result.get("content"):
            return

        self.current_mode = "reader"  # 切换至阅读器状态
        title = result.get("title", "无标题")
        content = result.get("content", "")

        pure_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <style>
                body {{ background-color: #ffffff; color: #111111; font-family: -apple-system, BlinkMacSystemFont, Georgia, Serif; line-height: 1.9; margin: 0; padding: 60px 20px; display: flex; justify-content: center; }}
                .reader-main {{ max-width: 700px; width: 100%; }}
                h1 {{ font-size: 38px; line-height: 1.25; margin-bottom: 8px; color: #000000; font-weight: 700; }}
                .meta-info {{ font-size: 14px; color: #767676; margin-bottom: 40px; }}
                p {{ font-size: 19px; margin-bottom: 28px; word-break: break-word; }}
                img {{ max-width: 100%; height: auto; display: block; margin: 30px auto; }}
                mark.webhighlights-pure {{ background-color: #fdffb4; padding: 1px 2px; border-radius: 2px; cursor: pointer; border-bottom: 1px solid #fbdc6d; }}
            </style>
        </head>
        <body>
            <div class="reader-main">
                <h1>{title}</h1>
                <div class="meta-info">阅读模式 • 已净化跳转链接</div>
                <div class="article-core-content">{content}</div>
            </div>
        </body>
        </html>
        """
        self.browser.setHtml(pure_html, QUrl(self.original_url))

    def on_page_load_finished(self, success):
        """【关键核心】当网页真正完全加载完毕后，才触发注入高亮"""
        if not success or self.current_mode == "extracting":
            return

        # 核心恢复与模糊匹配 JavaScript 代码
        highlight_js_code = """
        (function() {
            // 初始化桥梁
            let pyBridge = null;
            if (typeof qt !== 'undefined') {
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    pyBridge = channel.objects.pyBridge;
                    window.pyBridge = pyBridge; 
                });
            }

            const data = %s; // 动态填入 Python 传来的 JSON

            const cleanText = (str) => str.replace(/[\\s\\n\\r]+/g, ' ').replace(/[‘’]/g, "'").replace(/[“”]/g, '"').trim();
            const targetTextClean = cleanText(data.text);

            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
            let textNode;

            while (textNode = walker.nextNode()) {
                const nodeTextClean = cleanText(textNode.nodeValue);
                const index = nodeTextClean.indexOf(targetTextClean);

                if (index !== -1) {
                    let realIndex = textNode.nodeValue.indexOf(data.text);
                    let matchLength = data.text.length;

                    if (realIndex === -1) {
                        // 尝试弯引号模糊匹配
                        realIndex = textNode.nodeValue.indexOf(data.text.replace("'", "’"));
                    }
                    if (realIndex === -1) {
                        realIndex = 0;
                        matchLength = textNode.nodeValue.length;
                    }

                    try {
                        const range = document.createRange();
                        range.setStart(textNode, realIndex);
                        range.setEnd(textNode, realIndex + matchLength);

                        const mark = document.createElement('mark');
                        mark.className = 'webhighlights-pure';
                        mark.style.backgroundColor = data.color || '#fdffb4';
                        mark.dataset.raw = JSON.stringify(data);

                        mark.onclick = function(e) {
                            e.stopPropagation();
                            if (window.pyBridge) {
                                window.pyBridge.onHighlightClick(this.dataset.raw);
                            }
                        };

                        range.surroundContents(mark);
                        break;
                    } catch (e) { console.error(e); }
                }
            }
        })();
        """ % json.dumps(self.highlight_data)

        # 使用 QTimer 延迟 200ms 执行，确保 DOM 节点已经生成完毕，彻底解决白屏不显示问题
        QTimer.singleShot(200, lambda: self.browser.page().runJavaScript(highlight_js_code))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FixedReaderWindow()
    window.show()
    sys.exit(app.exec())