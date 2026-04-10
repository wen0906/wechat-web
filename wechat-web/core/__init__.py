#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web 版微信公众号文章排版发布工具 - 核心模块

提供与 wechat-assistant/core 兼容的接口
"""

import sys
import os
from pathlib import Path

# 获取 wechat-assistant 的绝对路径
_script_dir = Path(__file__).resolve().parent
_wechat_assistant_dir = _script_dir.parent.parent / 'wechat-assistant'

if _wechat_assistant_dir.exists():
    # 确保 wechat-assistant 的 core 目录在 Python 路径中
    _core_dir = _wechat_assistant_dir / 'core'
    if str(_core_dir) not in sys.path:
        sys.path.insert(0, str(_wechat_assistant_dir.parent))
    
    # 尝试导入原有核心模块
    try:
        from wechat_assistant.core.formatter import ArticleFormatter
        from wechat_assistant.core.file_parser import FileParser
        from wechat_assistant.core.wechat_api import WeChatAPI
    except ImportError:
        # 尝试直接导入（如果 wechat-assistant 被作为包安装）
        try:
            from core.formatter import ArticleFormatter
            from core.file_parser import FileParser
            from core.wechat_api import WeChatAPI
        except ImportError:
            # 最后尝试从父级目录导入
            sys.path.insert(0, str(_wechat_assistant_dir))
            from core.formatter import ArticleFormatter
            from core.file_parser import FileParser
            from core.wechat_api import WeChatAPI
else:
    # 如果 wechat-assistant 不存在，使用相对导入
    from .wechat_api_standalone import WeChatAPI
    # 定义占位符
    class ArticleFormatter:
        STYLES = ['simple', 'business', 'literary', 'tech']
        TEMPLATES = {}
        @classmethod
        def format(cls, content, title='', style='simple'):
            return f'<html><body><h1>{title}</h1><p>{content}</p></body></html>'
        @classmethod
        def get_style_description(cls, style):
            return ''
    class FileParser:
        SUPPORTED_EXTENSIONS = ['.docx', '.md', '.txt']
        @classmethod
        def parse(cls, path):
            return '标题', '内容'
        @classmethod
        def validate_file(cls, path):
            return True, ''

# 导入 Web 版 API
from .wechat_api import WeChatWebAPI

__all__ = ['ArticleFormatter', 'FileParser', 'WeChatAPI', 'WeChatWebAPI']
