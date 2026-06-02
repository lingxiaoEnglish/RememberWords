# -*- coding: utf-8 -*-
"""
@Project : RememberWords
@File    : lxUtil
@Author  : lingxiao
@Date    : 2026-06-02 13:44
@License : (C) Copyright 2026 Ling Xiao. All Rights Reserved.
"""
import sys
import os
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的临时解压路径
        path1 =  os.path.join(sys._MEIPASS, relative_path)
        # print(f'path1=={path1}')
        return path1

    # 正常开发环境路径：假设当前文件在项目的某子目录下，先退回项目根目录
    # 你也可以直接用 os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # print(f'base_dir=={base_dir}')
    return os.path.join(base_dir, relative_path)