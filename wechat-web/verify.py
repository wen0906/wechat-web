#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证脚本"""
import sys
sys.path.insert(0, '.')

# 测试核心模块导入
try:
    import importlib.util
    
    # 加载 formatter
    formatter_spec = importlib.util.spec_from_file_location('formatter', '../wechat-assistant/core/formatter.py')
    formatter = importlib.util.module_from_spec(formatter_spec)
    formatter_spec.loader.exec_module(formatter)
    ArticleFormatter = formatter.ArticleFormatter
    print('✅ ArticleFormatter 加载成功')
    print('   支持的风格:', ArticleFormatter.STYLES)
    
    # 加载 file_parser
    file_parser_spec = importlib.util.spec_from_file_location('file_parser', '../wechat-assistant/core/file_parser.py')
    file_parser = importlib.util.module_from_spec(file_parser_spec)
    file_parser_spec.loader.exec_module(file_parser)
    FileParser = file_parser.FileParser
    print('✅ FileParser 加载成功')
    
    # 加载 wechat_api
    wechat_api_spec = importlib.util.spec_from_file_location('wechat_api', '../wechat-assistant/core/wechat_api.py')
    wechat_api = importlib.util.module_from_spec(wechat_api_spec)
    wechat_api_spec.loader.exec_module(wechat_api)
    WeChatAPI = wechat_api.WeChatAPI
    print('✅ WeChatAPI 加载成功')
    
    print('\n🎉 所有核心模块加载成功！')
    
except Exception as e:
    print(f'❌ 加载失败: {e}')
    import traceback
    traceback.print_exc()
