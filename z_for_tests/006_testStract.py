# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : 006_testStract
@Author  : lingxiao
@Date    : 2026-06-24 15:24
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""

import requests
from bs4 import BeautifulSoup
import re


def get_bbc_audio_url(page_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(page_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # 策略：寻找所有 href 包含 .mp3 结尾的 a 标签
        # BBC 页面上通常有一个 class 为 'download' 或含有 download 字样的按钮
        mp3_links = soup.find_all('a', href=re.compile(r'\.mp3$'))

        if mp3_links:
            # 找到第一个符合条件的链接
            audio_url = mp3_links[0]['href']
            # 有时 BBC 使用的是相对路径或不带协议头，进行补全
            if audio_url.startswith('//'):
                audio_url = 'https:' + audio_url
            return audio_url

        print("未在页面中找到 MP3 下载链接")
        return None

    except Exception as e:
        print(f"解析出错: {e}")
        return None


# 测试解析
if __name__ == "__main__":
    test_url = "https://www.bbc.co.uk/learningenglish/english/features/6-minute-english_2026/ep-260212"
    mp3_url = get_bbc_audio_url(test_url)
    print(f"成功提取到音频直链: {mp3_url}")