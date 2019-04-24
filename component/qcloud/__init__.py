# -*- coding: utf-8 -*-
import os

__author__ = 'Blueking Team'

# 尝试从 __init__.py 同目录下读取 version_number 文件来获取模块当前版本号
try:
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(cur_dir, 'version_number'), 'r') as fp:
        __version__ = fp.read().strip()
except:
    __version__ = 'unknown'
