#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章排版模块

功能：
- 将 Markdown/纯文本转换为公众号友好的 HTML
- 支持多种排版风格（simple/business/literary/tech）
"""

import re
from typing import Dict


class ArticleFormatter:
    """文章排版器"""
    
    # 排版风格模板
    TEMPLATES = {
        'simple': '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
            font-size: 16px;
            line-height: 1.8;
            color: #333;
            max-width: 677px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
        }}
        h1 {{
            font-size: 26px;
            text-align: center;
            margin: 30px 0 25px;
            color: #1a1a1a;
            font-weight: bold;
            border-bottom: 2px solid #333;
            padding-bottom: 15px;
        }}
        h2 {{
            font-size: 20px;
            margin: 30px 0 15px;
            color: #1a1a1a;
            font-weight: bold;
        }}
        h3 {{
            font-size: 18px;
            margin: 25px 0 12px;
            color: #333;
            font-weight: bold;
        }}
        p {{
            margin: 0 0 16px;
            text-indent: 2em;
        }}
        ul, ol {{
            margin: 0 0 16px;
            padding-left: 30px;
        }}
        li {{
            margin: 10px 0;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            padding: 12px 15px;
            margin: 20px 0;
            color: #666;
            background: #f8f8f8;
        }}
        code {{
            font-family: Consolas, Monaco, "Courier New", monospace;
            background: #f0f0f0;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 14px;
        }}
        pre {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 20px 0;
            border: 1px solid #e0e0e0;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        strong {{ color: #d32f2f; }}
        em {{ color: #666; font-style: italic; }}
        a {{ color: #007bff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        hr {{
            border: none;
            border-top: 1px dashed #ddd;
            margin: 30px 0;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 15px auto;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>''',

        'business': '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", Arial, sans-serif;
            font-size: 15px;
            line-height: 1.8;
            color: #2c3e50;
            max-width: 677px;
            margin: 0 auto;
            padding: 30px 20px;
            background: #fafafa;
        }}
        .article-container {{
            background: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        h1 {{
            font-size: 28px;
            text-align: center;
            margin: 0 0 30px;
            color: #1e3a5f;
            font-weight: bold;
            letter-spacing: 2px;
        }}
        h2 {{
            font-size: 20px;
            margin: 35px 0 18px;
            color: #1e3a5f;
            font-weight: bold;
            border-left: 4px solid #1e3a5f;
            padding-left: 12px;
        }}
        h3 {{
            font-size: 17px;
            margin: 25px 0 14px;
            color: #34495e;
            font-weight: bold;
        }}
        p {{
            margin: 0 0 16px;
            text-indent: 2em;
            color: #2c3e50;
        }}
        ul, ol {{
            margin: 0 0 16px;
            padding-left: 28px;
            color: #2c3e50;
        }}
        li {{
            margin: 10px 0;
        }}
        blockquote {{
            border-left: none;
            padding: 15px 20px;
            margin: 25px 0;
            color: #555;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 0 8px 8px 0;
            border-left: 4px solid #1e3a5f;
        }}
        code {{
            font-family: Consolas, Monaco, "Courier New", monospace;
            background: #f1f3f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 14px;
            color: #c7254e;
        }}
        pre {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 25px 0;
        }}
        pre code {{
            background: none;
            padding: 0;
            color: inherit;
        }}
        strong {{ color: #c7254e; font-weight: bold; }}
        em {{ color: #666; font-style: italic; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #ddd, transparent);
            margin: 35px 0;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border-radius: 5px;
        }}
        .data-highlight {{
            background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
            padding: 2px 8px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
<div class="article-container">
{content}
</div>
</body>
</html>''',

        'literary': '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: "STSong", "SimSun", "宋体", serif;
            font-size: 17px;
            line-height: 2;
            color: #3d3d3d;
            max-width: 620px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #fefdf8;
        }}
        h1 {{
            font-size: 26px;
            text-align: center;
            margin: 50px 0 40px;
            color: #2c2c2c;
            font-weight: normal;
            letter-spacing: 4px;
        }}
        h2 {{
            font-size: 20px;
            margin: 45px 0 20px;
            color: #2c2c2c;
            font-weight: normal;
            text-align: center;
        }}
        h3 {{
            font-size: 18px;
            margin: 35px 0 18px;
            color: #3d3d3d;
            font-weight: normal;
        }}
        p {{
            margin: 0 0 20px;
            text-indent: 2em;
            text-align: justify;
        }}
        ul, ol {{
            margin: 0 0 20px;
            padding-left: 35px;
        }}
        li {{
            margin: 12px 0;
            text-indent: 0;
        }}
        blockquote {{
            border: none;
            padding: 20px 30px;
            margin: 30px 0;
            color: #666;
            background: #f9f7f2;
            font-style: italic;
            text-align: center;
        }}
        blockquote::before,
        blockquote::after {{
            content: '"';
            font-size: 24px;
            color: #999;
        }}
        code {{
            font-family: "Courier New", monospace;
            background: #f5f5f5;
            padding: 2px 5px;
            border-radius: 2px;
            font-size: 14px;
        }}
        pre {{
            background: #f5f5f5;
            padding: 20px;
            border-radius: 3px;
            overflow-x: auto;
            margin: 25px 0;
            border-left: 3px solid #ccc;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        strong {{ font-weight: bold; color: #333; }}
        em {{ font-style: normal; color: #888; }}
        a {{ color: #8b7355; text-decoration: none; border-bottom: 1px dotted #8b7355; }}
        a:hover {{ border-bottom: 1px solid #8b7355; }}
        hr {{
            border: none;
            text-align: center;
            margin: 45px 0;
        }}
        hr::before {{
            content: '◆ ◆ ◆';
            color: #ccc;
            letter-spacing: 10px;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 25px auto;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>''',

        'tech': '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 15px;
            line-height: 1.8;
            color: #24292e;
            max-width: 720px;
            margin: 0 auto;
            padding: 25px;
            background: #fff;
        }}
        h1 {{
            font-size: 28px;
            text-align: center;
            margin: 30px 0 25px;
            color: #1f1f1f;
            font-weight: 600;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 15px;
        }}
        h2 {{
            font-size: 22px;
            margin: 35px 0 18px;
            color: #1f1f1f;
            font-weight: 600;
            border-left: 4px solid #2563eb;
            padding-left: 12px;
        }}
        h3 {{
            font-size: 18px;
            margin: 28px 0 14px;
            color: #374151;
            font-weight: 600;
        }}
        p {{
            margin: 0 0 16px;
        }}
        ul, ol {{
            margin: 0 0 16px;
            padding-left: 28px;
        }}
        li {{
            margin: 10px 0;
        }}
        blockquote {{
            border-left: 4px solid #10b981;
            padding: 12px 18px;
            margin: 22px 0;
            color: #374151;
            background: #f0fdf4;
            border-radius: 0 6px 6px 0;
        }}
        code {{
            font-family: "SF Mono", Consolas, Monaco, "Courier New", monospace;
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 14px;
            color: #dc2626;
        }}
        pre {{
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 18px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 22px 0;
            border: 1px solid #333;
        }}
        pre code {{
            background: none;
            padding: 0;
            color: inherit;
            font-size: 14px;
            line-height: 1.6;
        }}
        strong {{ color: #dc2626; font-weight: 600; }}
        em {{ color: #059669; font-style: normal; }}
        a {{ color: #2563eb; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
            margin: 35px 0;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 18px auto;
            border-radius: 6px;
        }}
        .tip-box {{
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 6px;
            padding: 14px 18px;
            margin: 20px 0;
        }}
        .warning-box {{
            background: #fef3c7;
            border: 1px solid #fcd34d;
            border-radius: 6px;
            padding: 14px 18px;
            margin: 20px 0;
        }}
        .code-title {{
            background: #2d2d2d;
            color: #ccc;
            padding: 8px 15px;
            border-radius: 6px 6px 0 0;
            font-size: 13px;
            margin-top: 22px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #e5e7eb;
            padding: 10px 15px;
            text-align: left;
        }}
        th {{
            background: #f9fafb;
            font-weight: 600;
        }}
        tr:nth-child(even) {{
            background: #f9fafb;
        }}
    </style>
</head>
<body>
{content}
</body>
</html>'''
    }
    
    # 支持的风格列表
    STYLES = list(TEMPLATES.keys())
    
    @classmethod
    def format(cls, content: str, title: str = "", style: str = "simple") -> str:
        """
        格式化文章内容
        
        参数：
            content: 文章内容（支持 Markdown）
            title: 文章标题
            style: 排版风格（simple/business/literary/tech）
            
        返回：
            HTML 格式的文章
        """
        if not title:
            title = "未命名文章"
        
        # 转换 Markdown 为 HTML
        html_content = cls._convert_to_html(content)
        
        # 应用模板
        if style in cls.TEMPLATES:
            template = cls.TEMPLATES[style]
        else:
            template = cls.TEMPLATES['simple']
        
        return template.format(title=title, content=html_content)
    
    @classmethod
    def _convert_to_html(cls, content: str) -> str:
        """
        将 Markdown/纯文本转换为 HTML
        
        参数：
            content: 原始内容
            
        返回：
            HTML 格式内容
        """
        lines = content.split('\n')
        html_parts = []
        in_code_block = False
        code_block_content = []
        
        for line in lines:
            # 处理代码块
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_content = []
                else:
                    # 代码块结束
                    code_text = '\n'.join(code_block_content)
                    code_text = cls._escape_html(code_text)
                    html_parts.append(f'<pre><code>{code_text}</code></pre>')
                    in_code_block = False
                continue
            
            if in_code_block:
                code_block_content.append(line)
                continue
            
            # 处理标题
            if line.strip().startswith('### '):
                html_parts.append(f'<h3>{cls._process_inline(line[4:])}</h3>')
            elif line.strip().startswith('## '):
                html_parts.append(f'<h2>{cls._process_inline(line[3:])}</h2>')
            elif line.strip().startswith('# '):
                html_parts.append(f'<h1>{cls._process_inline(line[2:])}</h1>')
            # 处理列表
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                html_parts.append(f'<li>{cls._process_inline(line[2:])}</li>')
            elif re.match(r'^\d+\.\s', line.strip()):
                match = re.match(r'^(\d+)\.\s(.*)', line.strip())
                if match:
                    html_parts.append(f'<li>{cls._process_inline(match.group(2))}</li>')
            # 处理引用
            elif line.strip().startswith('>'):
                quote_content = line.lstrip('>').strip()
                html_parts.append(f'<blockquote>{cls._process_inline(quote_content)}</blockquote>')
            # 处理分隔线
            elif line.strip() in ['---', '***', '___']:
                html_parts.append('<hr>')
            # 处理空行
            elif not line.strip():
                continue
            # 普通段落
            else:
                html_parts.append(f'<p>{cls._process_inline(line)}</p>')
        
        # 包装列表
        result = []
        in_ul = False
        in_ol = False
        
        for part in html_parts:
            if part.startswith('<li>'):
                if not in_ul and not in_ol:
                    # 判断是数字列表还是符号列表
                    if '<li>' in part and re.match(r'^\d+\.', part):
                        result.append('<ol>')
                        in_ol = True
                    else:
                        result.append('<ul>')
                        in_ul = True
                result.append(part)
            else:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                result.append(part)
        
        # 关闭未关闭的列表
        if in_ul:
            result.append('</ul>')
        if in_ol:
            result.append('</ol>')
        
        return '\n'.join(result)
    
    @classmethod
    def _process_inline(cls, text: str) -> str:
        """
        处理行内元素（粗体、斜体、链接等）
        
        参数：
            text: 原始文本
            
        返回：
            处理后的文本
        """
        # 转义 HTML
        text = cls._escape_html(text)
        
        # 处理粗体 **text**
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        
        # 处理斜体 *text*
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        
        # 处理行内代码 `code`
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        
        # 处理链接 [text](url)
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
        
        # 处理图片 ![alt](url)
        text = re.sub(r'!\[(.+?)\]\((.+?)\)', r'<img src="\2" alt="\1">', text)
        
        return text
    
    @staticmethod
    def _escape_html(text: str) -> str:
        """转义 HTML 特殊字符"""
        replacements = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    @classmethod
    def get_style_description(cls, style: str) -> str:
        """获取风格描述"""
        descriptions = {
            'simple': '简约风格，适合资讯通知、公告类文章',
            'business': '商务风格，适合行业报告、分析文章',
            'literary': '文艺风格，适合散文、故事、情感类文章',
            'tech': '科技风格，适合技术文档、教程、代码展示'
        }
        return descriptions.get(style, '')
