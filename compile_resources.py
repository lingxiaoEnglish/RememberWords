# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : compile_resources
@Author  : lingxiao
@Date    : 2026-06-03 08:50
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""


"""
把图片的二进制数据转成 Base64 写进 .py 文件
"""

import base64
import os

# 配置图片所在的文件夹路径
IMAGES_DIR = "resources/images"
OUTPUT_PY = "resources_rc.py"
# 支持的图片格式
VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')


def compile_all_images():
    if not os.path.exists(IMAGES_DIR):
        print(f"❌ 找不到图片文件夹: {IMAGES_DIR}")
        return

    # 用于暂存所有图片的 base64 数据
    image_dict = {}

    # 遍历文件夹下的所有文件
    for file_name in os.listdir(IMAGES_DIR):
        if file_name.lower().endswith(VALID_EXTENSIONS):
            file_path = os.path.join(IMAGES_DIR, file_name)

            with open(file_path, "rb") as img_file:
                # 转码为 base64
                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
                # 以文件名作为 key 存入字典（例如 "default_loading.png"）
                image_dict[file_name] = encoded_string
                print(f"📸 已转码: {file_name}")

    if not image_dict:
        print("⚠️ 文件夹内未发现有效图片文件！")
        return

    # 生成资源 Python 文件
    with open(OUTPUT_PY, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("# 自动生成的多资源文件，请勿手动修改\n")
        f.write("from PyQt6.QtGui import QPixmap, QImage\n")
        f.write("import base64\n\n")

        # 写入大字典
        f.write("RESOURCES_MAP = {\n")
        for name, data in image_dict.items():
            f.write(f"    '{name}': '{data}',\n")
        f.write("}\n\n")

        # 写入通用的动态获取函数
        CODE_TEMPLATE = """
def get_pixmap(resource_name: str) -> QPixmap:
    \"\"\" 根据文件名获取对应的 QPixmap \"\"\"
    if resource_name not in RESOURCES_MAP:
         print(f"[Error] 资源字典中找不到图片: {resource_name}")
         return QPixmap()

    image = QImage()
    base64_data = RESOURCES_MAP[resource_name]
    image.loadFromData(base64.b64decode(base64_data.encode('utf-8')))
    return QPixmap.fromImage(image)
"""
        f.write(CODE_TEMPLATE.strip() + "\n")

    print(f"\n✅ 批量编译成功！共打包 {len(image_dict)} 张图片 -> 已生成: {OUTPUT_PY}")


if __name__ == "__main__":
    compile_all_images()