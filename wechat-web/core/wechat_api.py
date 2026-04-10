#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号 API 封装模块

功能：
- 获取 access_token
- 上传图文素材
- 发布/群发文章
"""

import json
import time
import hashlib
import base64
import io
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import urllib.request
import urllib.parse
import urllib.error

# 尝试导入 PIL，用于生成默认封面
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class WeChatAPI:
    """微信公众号 API 封装类"""
    
    BASE_URL = "https://api.weixin.qq.com/cgi-bin"
    
    def __init__(self, appid: str = "", appsecret: str = ""):
        """
        初始化 API 客户端
        
        参数：
            appid: 微信公众号 AppID
            appsecret: 微信公众号 AppSecret
        """
        self.appid = appid
        self.appsecret = appsecret
        self.access_token = ""
        self.token_expires_at = 0
    
    def set_credentials(self, appid: str, appsecret: str):
        """设置凭证"""
        self.appid = appid
        self.appsecret = appsecret
    
    def is_configured(self) -> bool:
        """检查是否已配置凭证"""
        return bool(self.appid and self.appsecret)
    
    def get_access_token(self, force_refresh: bool = False) -> Tuple[bool, str]:
        """
        获取 access_token
        
        参数：
            force_refresh: 是否强制刷新
            
        返回：
            (是否成功, token或错误消息)
        """
        if not self.is_configured():
            return False, "请先配置 AppID 和 AppSecret"
        
        # 检查缓存的 token 是否有效
        if not force_refresh and self.access_token and time.time() < self.token_expires_at:
            return True, self.access_token
        
        # 调用 API 获取 token
        url = f"{self.BASE_URL}/token?grant_type=client_credential&appid={self.appid}&secret={self.appsecret}"
        
        try:
            response = self._http_request(url)
            
            if 'access_token' in response:
                self.access_token = response['access_token']
                expires_in = response.get('expires_in', 7200)
                # 提前 5 分钟过期
                self.token_expires_at = time.time() + expires_in - 300
                return True, self.access_token
            else:
                errcode = response.get('errcode', 0)
                errmsg = response.get('errmsg', '未知错误')
                return False, f"获取 access_token 失败 [{errcode}]: {errmsg}"
                
        except Exception as e:
            return False, f"网络请求失败：{str(e)}"
    
    def _create_default_thumb(self) -> Optional[bytes]:
        """
        创建默认封面图片（900x500 深灰色背景）
        
        返回：
            图片二进制数据，失败返回 None
        """
        if not HAS_PIL:
            return None
        
        try:
            # 创建 900x500 的图片（微信推荐封面尺寸）
            img = Image.new('RGB', (900, 500), color='#4a5568')
            draw = ImageDraw.Draw(img)
            
            # 绘制简单的装饰
            draw.rectangle([0, 0, 900, 500], outline='#2d3748', width=3)
            
            # 转换为字节
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            return buffer.getvalue()
        except Exception:
            return None
    
    def _upload_permanent_image(self, image_data: bytes, filename: str = "default_cover.jpg") -> Tuple[bool, str]:
        """
        上传永久素材图片
        
        参数：
            image_data: 图片二进制数据
            filename: 文件名
            
        返回：
            (是否成功, media_id或错误消息)
        """
        success, token = self.get_access_token()
        if not success:
            return False, token
        
        # 使用永久素材上传接口
        url = f"{self.BASE_URL}/material/add_material?access_token={token}&type=image"
        
        try:
            # 构建 multipart/form-data 请求
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
            
            header = f'--{boundary}\r\nContent-Disposition: form-data; name="media"; filename="{filename}"\r\nContent-Type: image/jpeg\r\n\r\n'
            footer = f'\r\n--{boundary}--\r\n'
            
            body = header.encode('utf-8') + image_data + footer.encode('utf-8')
            
            req = urllib.request.Request(url, data=body)
            req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            if 'media_id' in result:
                return True, result['media_id']
            else:
                errcode = result.get('errcode', 0)
                errmsg = result.get('errmsg', '未知错误')
                return False, f"上传封面失败 [{errcode}]: {errmsg}"
                
        except Exception as e:
            return False, f"上传封面失败：{str(e)}"
    
    def upload_content_image(self, image_data: bytes, filename: str = "content.jpg") -> Tuple[bool, str]:
        """
        上传图文消息内的图片，获取微信服务器的 URL
        
        参数：
            image_data: 图片二进制数据
            filename: 文件名
            
        返回：
            (是否成功, 图片URL或错误消息)
        """
        success, token = self.get_access_token()
        if not success:
            return False, token
        
        # 使用图文消息内图片上传接口
        url = f"{self.BASE_URL}/media/uploadimg?access_token={token}"
        
        try:
            # 构建 multipart/form-data 请求
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
            
            header = f'--{boundary}\r\nContent-Disposition: form-data; name="media"; filename="{filename}"\r\nContent-Type: image/jpeg\r\n\r\n'
            footer = f'\r\n--{boundary}--\r\n'
            
            body = header.encode('utf-8') + image_data + footer.encode('utf-8')
            
            req = urllib.request.Request(url, data=body)
            req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            if 'url' in result:
                return True, result['url']
            else:
                errcode = result.get('errcode', 0)
                errmsg = result.get('errmsg', '未知错误')
                return False, f"上传内容图片失败 [{errcode}]: {errmsg}"
                
        except Exception as e:
            return False, f"上传内容图片失败：{str(e)}"
    
    def upload_news(self, title: str, content: str, thumb_media_id: str = "", thumb_image_path: str = "") -> Tuple[bool, Dict[str, Any]]:
        """
        上传图文素材（新建草稿）
        
        参数：
            title: 文章标题
            content: 文章内容（HTML）
            thumb_media_id: 封面图片 media_id（可选，优先使用）
            thumb_image_path: 封面图片路径（可选）
            
        返回：
            (是否成功, 结果或错误信息)
        """
        success, token = self.get_access_token()
        if not success:
            return False, token
        
        # 如果没有提供 thumb_media_id，需要上传封面图片
        if not thumb_media_id:
            if thumb_image_path and Path(thumb_image_path).exists():
                # 使用用户提供的封面图片
                with open(thumb_image_path, 'rb') as f:
                    image_data = f.read()
                success, result = self._upload_permanent_image(image_data, Path(thumb_image_path).name)
                if success:
                    thumb_media_id = result
                else:
                    return False, f"封面图片上传失败：{result}"
            else:
                # 自动生成默认封面
                if HAS_PIL:
                    image_data = self._create_default_thumb()
                    if image_data:
                        success, result = self._upload_permanent_image(image_data)
                        if success:
                            thumb_media_id = result
                        else:
                            return False, f"默认封面上传失败：{result}"
                    else:
                        return False, "无法创建默认封面图片，请手动提供封面图片"
                else:
                    return False, "未安装 PIL 库，无法自动生成封面。请安装 Pillow：pip install Pillow，或手动提供封面图片路径"
        
        # 清理内容中的外部链接（微信只接受微信服务器的图片链接）
        # 移除所有外部图片链接
        import re
        # 移除 img 标签中的外部 src
        content = re.sub(r'<img[^>]+src=["\']https?://(?!mmbiz\.qpic\.cn|mmbiz\.cdn\.weixin\.qq\.com)[^"\']+["\'][^>]*>', '', content)
        # 移除其他外部链接
        content = re.sub(r'<a[^>]+href=["\']https?://(?!mp\.weixin\.qq\.com)[^"\']+["\']', '<a href="#">', content)
        
        # 使用草稿接口（而不是永久素材接口）
        url = f"{self.BASE_URL}/draft/add?access_token={token}"
        
        # 构建图文消息
        article = {
            "title": title,
            "author": "",
            "digest": "",  # 摘要
            "content": content,
            "content_source_url": "",  # 原文链接，留空
            "thumb_media_id": thumb_media_id,
            "need_open_comment": 0,  # 关闭评论
            "only_fans_can_comment": 0
        }
        
        data = {
            "articles": [article]
        }
        
        try:
            response = self._http_request(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
            
            if 'media_id' in response:
                return True, {
                    'media_id': response['media_id'],
                    'url': response.get('url', '')
                }
            else:
                errcode = response.get('errcode', 0)
                errmsg = response.get('errmsg', '未知错误')
                return False, f"上传图文素材失败 [{errcode}]: {errmsg}"
                
        except Exception as e:
            return False, f"网络请求失败：{str(e)}"
    
    def publish_news(self, media_id: str) -> Tuple[bool, str]:
        """
        发布图文消息
        
        参数：
            media_id: 图文素材 media_id
            
        返回：
            (是否成功, 消息或错误)
        """
        success, token = self.get_access_token()
        if not success:
            return False, token
        
        url = f"{self.BASE_URL}/freepublish/submit?access_token={token}"
        
        data = {
            "media_id": media_id
        }
        
        try:
            response = self._http_request(url, data=json.dumps(data).encode('utf-8'))
            
            errcode = response.get('errcode', 0)
            if errcode == 0:
                msg_id = response.get('msg_id', '')
                return True, f"发布成功，消息ID：{msg_id}"
            else:
                errmsg = response.get('errmsg', '未知错误')
                return False, f"发布失败 [{errcode}]: {errmsg}"
                
        except Exception as e:
            return False, f"网络请求失败：{str(e)}"
    
    def upload_thumb_image(self, image_path: str) -> Tuple[bool, Dict[str, Any]]:
        """
        上传封面图片
        
        参数：
            image_path: 图片路径
            
        返回：
            (是否成功, 结果或错误信息)
        """
        success, token = self.get_access_token()
        if not success:
            return False, token
        
        url = f"{self.BASE_URL}/media/upload?access_token={token}&type=image"
        
        try:
            # 读取图片文件
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # 构建 multipart/form-data 请求
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
            
            header = f'--{boundary}\r\nContent-Disposition: form-data; name="media"; filename="{Path(image_path).name}"\r\nContent-Type: image/jpeg\r\n\r\n'
            footer = f'\r\n--{boundary}--\r\n'
            
            body = header.encode('utf-8') + image_data + footer.encode('utf-8')
            
            req = urllib.request.Request(url, data=body)
            req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            if 'media_id' in result:
                return True, {
                    'media_id': result['media_id'],
                    'url': result.get('url', '')
                }
            else:
                errcode = result.get('errcode', 0)
                errmsg = result.get('errmsg', '未知错误')
                return False, f"上传封面图片失败 [{errcode}]: {errmsg}"
                
        except Exception as e:
            return False, f"上传封面图片失败：{str(e)}"
    
    def get_followers_count(self) -> Tuple[bool, Any]:
        """获取粉丝数量"""
        success, token = self.get_access_token()
        if not success:
            return False, token
        
        url = f"{self.BASE_URL}/user/get?access_token={token}"
        
        try:
            response = self._http_request(url)
            
            if 'count' in response:
                return True, response['count']
            else:
                return False, response.get('errmsg', '获取失败')
                
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def _http_request(url: str, data: bytes = None, method: str = None) -> Dict[str, Any]:
        """
        发送 HTTP 请求
        
        参数：
            url: 请求URL
            data: 请求数据
            method: 请求方法
            
        返回：
            响应 JSON 数据
        """
        if method is None:
            method = 'POST' if data else 'GET'
        
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('Accept', 'application/json')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: str = None):
        """
        初始化配置管理器
        
        参数：
            config_path: 配置文件路径，默认使用程序目录下的 config.json
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.json"
        self.config_path = Path(config_path)
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception:
                self.config = {}
        else:
            self.config = {}
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            return False, str(e)
        return True
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置项"""
        self.config[key] = value
    
    def get_credentials(self) -> Tuple[str, str]:
        """获取凭证"""
        return self.get('appid', ''), self.get('appsecret', '')
    
    def set_credentials(self, appid: str, appsecret: str):
        """设置凭证"""
        self.set('appid', appid)
        self.set('appsecret', appsecret)
    
    def is_configured(self) -> bool:
        """检查是否已配置"""
        appid, appsecret = self.get_credentials()
        return bool(appid and appsecret)
