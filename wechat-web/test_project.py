#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目完整性检查脚本

检查所有必要文件和模块是否完整
"""

import os
import sys
from pathlib import Path


def check_project_structure():
    """检查项目结构"""
    print("=" * 50)
    print("📁 检查项目结构")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    required_files = [
        'app.py',
        'config.json',
        'requirements.txt',
        'README.md',
        'start.sh',
        'start.bat',
        'install.py',
        'core/__init__.py',
        'core/wechat_api.py',
        'templates/index.html',
        'templates/preview.html',
        'static/css/style.css',
        'static/js/main.js',
    ]
    
    all_ok = True
    for file in required_files:
        path = project_root / file
        status = "✅" if path.exists() else "❌"
        if not path.exists():
            all_ok = False
        print(f"  {status} {file}")
    
    return all_ok


def check_core_modules():
    """检查核心模块"""
    print("\n" + "=" * 50)
    print("🔧 检查核心模块")
    print("=" * 50)
    
    try:
        import importlib.util
        
        # 检查 formatter
        formatter_spec = importlib.util.spec_from_file_location(
            'formatter', 
            '../wechat-assistant/core/formatter.py'
        )
        formatter = importlib.util.module_from_spec(formatter_spec)
        formatter_spec.loader.exec_module(formatter)
        ArticleFormatter = formatter.ArticleFormatter
        
        print(f"  ✅ ArticleFormatter - 支持风格: {ArticleFormatter.STYLES}")
        
        # 检查 file_parser
        file_parser_spec = importlib.util.spec_from_file_location(
            'file_parser', 
            '../wechat-assistant/core/file_parser.py'
        )
        file_parser = importlib.util.module_from_spec(file_parser_spec)
        file_parser_spec.loader.exec_module(file_parser)
        FileParser = file_parser.FileParser
        
        print(f"  ✅ FileParser - 支持格式: {FileParser.SUPPORTED_EXTENSIONS}")
        
        # 检查 wechat_api
        wechat_api_spec = importlib.util.spec_from_file_location(
            'wechat_api', 
            '../wechat-assistant/core/wechat_api.py'
        )
        wechat_api = importlib.util.module_from_spec(wechat_api_spec)
        wechat_api_spec.loader.exec_module(wechat_api)
        WeChatAPI = wechat_api.WeChatAPI
        
        print(f"  ✅ WeChatAPI - 基础 API 类")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 核心模块检查失败: {e}")
        return False


def check_templates():
    """检查模板文件"""
    print("\n" + "=" * 50)
    print("📝 检查模板文件")
    print("=" * 50)
    
    try:
        from pathlib import Path
        project_root = Path(__file__).parent
        
        # 读取 index.html
        index_html = (project_root / 'templates' / 'index.html').read_text()
        checks = [
            ('上传区域', 'upload-area' in index_html),
            ('风格选择', 'style-grid' in index_html),
            ('编辑器', 'article-content' in index_html),
            ('配置模态框', 'config-modal' in index_html),
        ]
        
        for name, ok in checks:
            print(f"  {'✅' if ok else '❌'} index.html - {name}")
        
        # 读取 preview.html
        preview_html = (project_root / 'templates' / 'preview.html').read_text()
        checks = [
            ('预览内容', 'preview-content' in preview_html),
            ('发布按钮', 'publish' in preview_html.lower()),
            ('复制HTML', 'copyHtml' in preview_html),
        ]
        
        for name, ok in checks:
            print(f"  {'✅' if ok else '❌'} preview.html - {name}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 模板检查失败: {e}")
        return False


def main():
    print("\n🔍 微信公众号文章排版发布工具 - 项目检查")
    
    structure_ok = check_project_structure()
    core_ok = check_core_modules()
    templates_ok = check_templates()
    
    print("\n" + "=" * 50)
    print("📊 检查结果汇总")
    print("=" * 50)
    print(f"  {'✅' if structure_ok else '❌'} 项目结构: {'完整' if structure_ok else '不完整'}")
    print(f"  {'✅' if core_ok else '❌'} 核心模块: {'正常' if core_ok else '异常'}")
    print(f"  {'✅' if templates_ok else '❌'} 模板文件: {'正常' if templates_ok else '异常'}")
    
    if structure_ok and core_ok and templates_ok:
        print("\n🎉 项目检查通过！")
        print("\n🚀 启动方式:")
        print("   1. 安装依赖: python install.py")
        print("   2. 启动服务: python app.py")
        print("   3. 访问: http://127.0.0.1:5000")
    else:
        print("\n⚠️ 项目检查发现问题，请修复后再试")
    
    print()


if __name__ == '__main__':
    main()
