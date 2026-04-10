#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章排版发布 Web 工具

Flask 主程序
"""

import os
import sys
import json
import uuid
import base64
import importlib.util
from pathlib import Path
from datetime import datetime

from flask import (
    Flask, render_template, request, jsonify, 
    send_from_directory, session
)
from werkzeug.utils import secure_filename

# 获取核心模块路径
_script_dir = Path(__file__).resolve().parent
_core_dir = _script_dir / 'core'

# 动态加载核心模块
def load_core_module(module_name):
    """加载 core 目录下的模块"""
    module_path = _core_dir / f'{module_name}.py'
    if not module_path.exists():
        raise ImportError(f"核心模块不存在: {module_path}")
    
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# 加载核心模块
_formatter = load_core_module('formatter')
_file_parser = load_core_module('file_parser')
_wechat_api = load_core_module('wechat_api')

ArticleFormatter = _formatter.ArticleFormatter
FileParser = _file_parser.FileParser

# Web 版 API
class WeChatWebAPI(_wechat_api.WeChatAPI):
    """Web 版微信公众号 API"""
    
    def publish_news(self, title: str, content: str):
        """
        一键发布图文消息到公众号草稿箱
        """
        # 调用父类的 upload_news 方法
        success, result = self.upload_news(title, content)
        
        if not success:
            return False, result
        
        if isinstance(result, dict):
            return True, {
                'media_id': result.get('media_id', ''),
                'url': result.get('url', ''),
                'message': '文章已保存到草稿箱，请前往公众号后台编辑并发布'
            }
        
        return True, result


# 创建 Flask 应用
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 最大文件大小
app.config['UPLOAD_FOLDER'] = 'uploads'

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'docx', 'md', 'txt'}

# 配置文件路径
CONFIG_FILE = 'config.json'


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置失败: {e}")
    return {
        'appid': '',
        'appsecret': '',
        'default_style': 'simple'
    }


def save_config(config):
    """保存配置文件"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"保存配置失败: {e}")
        return False


# ==================== 路由 ====================

@app.route('/')
def index():
    """主页"""
    config = load_config()
    return render_template('index.html', 
                           config=config,
                           styles=ArticleFormatter.STYLES,
                           style_descriptions={
                               'simple': '适合资讯通知、公告类文章',
                               'business': '适合行业报告、分析文章',
                               'literary': '适合散文、故事、情感类文章',
                               'tech': '适合技术文档、教程、代码展示'
                           })


@app.route('/preview')
def preview():
    """预览页面"""
    html_content = request.args.get('html', '')
    title = request.args.get('title', '预览')
    return render_template('preview.html', 
                          html=html_content, 
                          title=title)


# ==================== API 接口 ====================

@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """获取或设置配置"""
    if request.method == 'GET':
        config = load_config()
        # 不返回 AppSecret 的完整内容
        if config.get('appsecret'):
            config['appsecret'] = config['appsecret'][:4] + '****' + config['appsecret'][-4:]
        return jsonify({'success': True, 'data': config})
    
    # POST - 保存配置
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '无效的请求数据'})
    
    config = load_config()
    
    # 更新配置
    if 'appid' in data:
        config['appid'] = data['appid'].strip()
    if 'appsecret' in data:
        config['appsecret'] = data['appsecret'].strip()
    if 'default_style' in data:
        config['default_style'] = data['default_style']
    
    if save_config(config):
        return jsonify({'success': True, 'message': '配置已保存'})
    else:
        return jsonify({'success': False, 'message': '保存配置失败'})


@app.route('/api/upload', methods=['POST'])
def api_upload():
    """上传文件"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '没有上传文件'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': '请选择文件'})
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': '不支持的文件格式，支持：docx, md, txt'})
    
    try:
        # 保存文件
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # 解析文件
        title, content = FileParser.parse(filepath)
        
        # 清理临时文件
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'data': {
                'title': title,
                'content': content
            }
        })
        
    except FileNotFoundError as e:
        return jsonify({'success': False, 'message': str(e)})
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)})
    except ImportError as e:
        return jsonify({'success': False, 'message': str(e)})
    except Exception as e:
        return jsonify({'success': False, 'message': f'处理文件失败: {str(e)}'})


@app.route('/api/format', methods=['POST'])
def api_format():
    """排版文章"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': '无效的请求数据'})
    
    content = data.get('content', '').strip()
    title = data.get('title', '').strip()
    style = data.get('style', 'simple')
    
    if not content:
        return jsonify({'success': False, 'message': '文章内容不能为空'})
    
    if style not in ArticleFormatter.STYLES:
        style = 'simple'
    
    try:
        html = ArticleFormatter.format(content, title, style)
        
        return jsonify({
            'success': True,
            'data': {
                'html': html,
                'title': title
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'排版失败: {str(e)}'})


@app.route('/api/publish', methods=['POST'])
def api_publish():
    """发布到公众号"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': '无效的请求数据'})
    
    html_content = data.get('html', '').strip()
    title = data.get('title', '未命名文章').strip()
    
    if not html_content:
        return jsonify({'success': False, 'message': '文章内容不能为空'})
    
    # 加载配置
    config = load_config()
    
    if not config.get('appid') or not config.get('appsecret'):
        return jsonify({
            'success': False, 
            'message': '请先配置微信公众号凭证（AppID 和 AppSecret）'
        })
    
    try:
        # 初始化 API
        wechat_api = WeChatWebAPI(config['appid'], config['appsecret'])
        
        # 发布图文消息
        success, result = wechat_api.publish_news(title, html_content)
        
        if success:
            return jsonify({
                'success': True,
                'message': '发布成功',
                'data': result
            })
        else:
            return jsonify({
                'success': False,
                'message': result  # 错误消息
            })
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'发布失败: {str(e)}'})


@app.route('/api/styles', methods=['GET'])
def api_styles():
    """获取支持的排版风格"""
    styles = []
    for style in ArticleFormatter.STYLES:
        styles.append({
            'id': style,
            'name': get_style_display_name(style),
            'description': ArticleFormatter.get_style_description(style)
        })
    
    return jsonify({'success': True, 'data': styles})


def get_style_display_name(style):
    """获取风格显示名称"""
    names = {
        'simple': '简约风格',
        'business': '商务风格',
        'literary': '文艺风格',
        'tech': '科技风格'
    }
    return names.get(style, style)


@app.route('/api/health', methods=['GET'])
def api_health():
    """健康检查"""
    return jsonify({
        'success': True,
        'message': '服务正常运行',
        'time': datetime.now().isoformat()
    })


# ==================== 静态文件 ====================

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """访问上传的文件"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ==================== 启动 ====================

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 50)
    print("🚀 微信公众号文章排版发布工具")
    print("=" * 50)
    print(f"📍 访问地址: http://127.0.0.1:{port}")
    print(f"📍 或访问: http://localhost:{port}")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # 生产环境关闭 debug
    )
