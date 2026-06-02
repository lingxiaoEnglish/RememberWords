# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : styles_qss
@Author  : lingxiao
@Date    : 2026-06-01 16:44
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
import os
from warnings import deprecated
from config.theme import FONT_FAMILY, get_theme_colors
from lxUtils.lxUtil import get_resource_path

def load_qss(qss_names: list[str], parent_path: str = "config/qss" ) -> str:
    """
    核心装配引擎：读取 .qss 模板并动态替换变量
    """
    # 1. 安全计算路径（防止打包成 exe 后找不到文件）
    qss_paths = [get_resource_path(f"{parent_path}/{name}.qss") for name in qss_names]

    template_content = ''
    # 2. 获取当前系统所需的颜色字典
    context = get_theme_colors()
    context["FONT_FAMILY"] = FONT_FAMILY  # 别忘了把字体放进去

    for qss_path in qss_paths:
        if not os.path.exists(qss_path):
            print(f"[QSS 警告] 未找到模板文件: {qss_path}，转为安全空样式。")
            continue
        try:
            sub_qss_content = ''
            with open(qss_path, "r", encoding="utf-8") as f:
                sub_qss_content = f.read()

            template_content += sub_qss_content

            # 3. 核心印染：全自动替换占位符
            for key, value in context.items():
                # placeholder = f"'{{{{{key}}}}}'"  # 生成 {{variable}} 的形式
                placeholder = "{{" + key + "}}"
                # print(f'placeholder={placeholder}')
                template_content = template_content.replace(placeholder, value)
        except Exception as e:
            print(f"[QSS 异常] 印染样式表失败: {e}")
            continue

    return template_content


@deprecated("use load_qss function instead")
def generate_qss() -> str:
    """
    核心装配引擎：读取 .qss 模板并动态替换变量
    """
    # 1. 安全计算路径（防止打包成 exe 后找不到文件）
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    qss_path = os.path.join(base_dir, "resources", "style.qss")

    if not os.path.exists(qss_path):
        print(f"[QSS 警告] 未找到模板文件: {qss_path}，转为安全空样式。")
        return ""
    try:
        template_content = ''
        with open(qss_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        # 2. 获取当前系统所需的颜色字典
        context = get_theme_colors()
        context["FONT_FAMILY"] = FONT_FAMILY  # 别忘了把字体放进去

        # 3. 核心印染：全自动替换占位符
        for key, value in context.items():
            placeholder = f"'{{{{{key}}}}}'"  # 生成 {{variable}} 的形式
            template_content = template_content.replace(placeholder, value)

        return template_content

    except Exception as e:
        print(f"[QSS 异常] 印染样式表失败: {e}")
        return ""